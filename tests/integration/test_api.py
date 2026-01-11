import json
import threading
from http.client import HTTPConnection

from acbf.api import ACBFServer
from acbf.config import AppConfig, BackendConfig, BlockchainConfig, FrontendConfig


def _start_server():
    config = AppConfig(
        blockchain=BlockchainConfig(difficulty=2, mining_reward=5, chain_id="test"),
        backend=BackendConfig(host="127.0.0.1", port=0, debug=False),
        frontend=FrontendConfig(port=3000),
    )
    server = ACBFServer((config.backend.host, config.backend.port), config)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    return server, host, port


def _request_json(host, port, method, path, payload=None):
    conn = HTTPConnection(host, port)
    headers = {}
    body = None
    if payload is not None:
        body = json.dumps(payload)
        headers["Content-Type"] = "application/json"
    conn.request(method, path, body=body, headers=headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    conn.close()
    return response.status, json.loads(data)


def test_health_endpoint():
    server, host, port = _start_server()
    try:
        status, data = _request_json(host, port, "GET", "/health")
        assert status == 200
        assert data["chain_id"] == "test"
    finally:
        server.shutdown()


def test_wallet_transaction_mining_flow():
    server, host, port = _start_server()
    try:
        status, wallet = _request_json(host, port, "POST", "/wallet")
        assert status == 200
        assert "address" in wallet

        status, _ = _request_json(
            host,
            port,
            "POST",
            "/transaction",
            {"sender": "alice", "recipient": wallet["address"], "amount": 10},
        )
        assert status == 200

        status, _ = _request_json(host, port, "POST", "/mine", {"miner_address": wallet["address"]})
        assert status == 200

        status, balance = _request_json(host, port, "GET", f"/balance?address={wallet['address']}")
        assert balance["balance"] == 15

        status, metrics = _request_json(host, port, "GET", "/metrics")
        assert metrics["transaction_count"] == 2
    finally:
        server.shutdown()


def test_contract_deploy_and_call():
    server, host, port = _start_server()
    try:
        status, payload = _request_json(host, port, "POST", "/contracts/deploy", {"contract_type": "storage"})
        contract = payload["contract"]

        status, _ = _request_json(
            host,
            port,
            "POST",
            "/contracts/call",
            {"address": contract["address"], "sender": "alice", "method": "set", "args": ["k", "v"]},
        )
        assert status == 200

        status, result = _request_json(
            host,
            port,
            "POST",
            "/contracts/call",
            {"address": contract["address"], "sender": "alice", "method": "get", "args": ["k"]},
        )
        assert result["result"]["value"] == "v"
    finally:
        server.shutdown()
