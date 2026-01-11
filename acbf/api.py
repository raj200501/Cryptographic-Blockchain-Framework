"""HTTP API for the ACBF demo backend (standard library only)."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, Tuple
from urllib.parse import parse_qs, urlparse

from acbf.config import AppConfig, load_config
from acbf.service import BlockchainService
from acbf.validation import normalize_address, normalize_amount


class ACBFServer(ThreadingHTTPServer):
    def __init__(self, server_address: Tuple[str, int], config: AppConfig) -> None:
        super().__init__(server_address, ACBFRequestHandler)
        self.config = config
        self.service = BlockchainService(config.blockchain)


def _json_response(handler: BaseHTTPRequestHandler, payload: Dict[str, Any], status: int = 200) -> None:
    data = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def _error(handler: BaseHTTPRequestHandler, message: str, status: int = 400) -> None:
    _json_response(handler, {"status": "error", "message": message}, status=status)


def _parse_json(handler: BaseHTTPRequestHandler) -> Dict[str, Any]:
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return {}
    raw = handler.rfile.read(length)
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON payload") from exc


class ACBFRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self) -> None:  # noqa: N802
        _json_response(self, {"status": "ok"}, status=200)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        service = self.server.service  # type: ignore[attr-defined]

        if path == "/health":
            _json_response(self, {"status": "ok", "chain_id": self.server.config.blockchain.chain_id})
            return

        if path == "/balance":
            address = query.get("address", [None])[0]
            if not address:
                _error(self, "address query parameter is required")
                return
            try:
                address = normalize_address(address)
            except ValueError as exc:
                _error(self, str(exc))
                return
            _json_response(self, {"address": address, "balance": service.get_balance(address)})
            return

        if path == "/chain":
            _json_response(self, service.blockchain.to_dict())
            return

        if path == "/metrics":
            _json_response(self, service.metrics().to_dict())
            return

        if path == "/contracts":
            _json_response(self, service.list_contracts())
            return

        _error(self, "Not found", status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        service = self.server.service  # type: ignore[attr-defined]

        try:
            payload = _parse_json(self)
        except ValueError as exc:
            _error(self, str(exc))
            return

        if path == "/wallet":
            wallet = service.create_wallet()
            _json_response(self, wallet.to_dict())
            return

        if path == "/transaction":
            sender = payload.get("sender")
            recipient = payload.get("recipient")
            amount = payload.get("amount")
            if sender is None or recipient is None or amount is None:
                _error(self, "sender, recipient, and amount are required")
                return
            try:
                sender = normalize_address(str(sender))
                recipient = normalize_address(str(recipient))
                amount = normalize_amount(amount)
                result = service.submit_transaction(
                    sender=sender,
                    recipient=recipient,
                    amount=amount,
                    metadata=payload.get("metadata", {}),
                )
            except (ValueError, TypeError) as exc:
                _error(self, str(exc))
                return
            _json_response(
                self,
                {
                    "transaction": result.transaction.to_dict(),
                    "pending_transactions": result.pending_count,
                },
            )
            return

        if path == "/mine":
            miner_address = payload.get("miner_address")
            if not miner_address:
                _error(self, "miner_address is required")
                return
            try:
                miner_address = normalize_address(str(miner_address))
                result = service.mine(miner_address)
            except (RuntimeError, ValueError) as exc:
                _error(self, str(exc))
                return
            _json_response(
                self,
                {
                    "block_hash": result.block_hash,
                    "block_index": result.block_index,
                    "transactions": result.transaction_count,
                },
            )
            return

        if path == "/contracts/deploy":
            contract_type = payload.get("contract_type")
            if not contract_type:
                _error(self, "contract_type is required")
                return
            try:
                contract = service.deploy_contract(contract_type=str(contract_type), **payload.get("params", {}))
            except (ValueError, TypeError) as exc:
                _error(self, str(exc))
                return
            _json_response(self, {"contract": contract})
            return

        if path == "/contracts/call":
            address = payload.get("address")
            sender = payload.get("sender")
            method = payload.get("method")
            args = payload.get("args", [])
            if not address or not sender or not method:
                _error(self, "address, sender, and method are required")
                return
            try:
                address = normalize_address(str(address))
                sender = normalize_address(str(sender))
                result = service.call_contract(
                    address=address,
                    sender=sender,
                    method=str(method),
                    args=list(args),
                )
            except (KeyError, ValueError, TypeError) as exc:
                _error(self, str(exc))
                return
            _json_response(self, {"result": result})
            return

        _error(self, "Not found", status=HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: object) -> None:
        return


def create_server(config: AppConfig | None = None) -> ACBFServer:
    config = config or load_config()
    return ACBFServer((config.backend.host, config.backend.port), config)


def main() -> None:
    config = load_config()
    server = create_server(config)
    print(f"ACBF API running on http://{config.backend.host}:{config.backend.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
