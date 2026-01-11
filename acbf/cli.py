"""Command-line interface for ACBF."""

from __future__ import annotations

import argparse
import json
import sys
from typing import List

from acbf.config import load_config
from acbf.crypto.aes import AESCipher
from acbf.crypto.rsa import demo_encrypt_decrypt
from acbf.crypto.hashing import sha256_hexdigest
from acbf.service import BlockchainService


def _print(data: object) -> None:
    print(json.dumps(data, indent=2))


def _crypto_demo(message: str) -> None:
    aes_key = AESCipher.generate_key()
    aes_cipher = AESCipher(aes_key)
    bundle = aes_cipher.encrypt(message.encode("utf-8"))
    decrypted = aes_cipher.decrypt(bundle).decode("utf-8")

    rsa_ciphertext, rsa_plain = demo_encrypt_decrypt(message)

    _print(
        {
            "sha256": sha256_hexdigest(message),
            "aes": {
                "key_hex": aes_key.hex(),
                "ciphertext_hex": bundle.as_bytes().hex(),
                "decrypted": decrypted,
            },
            "rsa": {
                "ciphertext_hex": rsa_ciphertext.hex(),
                "decrypted": rsa_plain.decode("utf-8"),
            },
        }
    )


def _parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ACBF CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("wallet", help="Generate a new wallet")

    balance_parser = subparsers.add_parser("balance", help="Get wallet balance")
    balance_parser.add_argument("address")

    tx_parser = subparsers.add_parser("transfer", help="Submit a transaction")
    tx_parser.add_argument("sender")
    tx_parser.add_argument("recipient")
    tx_parser.add_argument("amount", type=float)

    mine_parser = subparsers.add_parser("mine", help="Mine pending transactions")
    mine_parser.add_argument("miner_address")

    subparsers.add_parser("chain", help="Show the blockchain")
    subparsers.add_parser("metrics", help="Show chain metrics")

    deploy_parser = subparsers.add_parser("deploy", help="Deploy a smart contract")
    deploy_parser.add_argument("contract_type", choices=["token", "storage"])
    deploy_parser.add_argument("--symbol", default="ACBF")
    deploy_parser.add_argument("--decimals", type=int, default=2)

    call_parser = subparsers.add_parser("call", help="Call a smart contract")
    call_parser.add_argument("address")
    call_parser.add_argument("sender")
    call_parser.add_argument("method")
    call_parser.add_argument("args", nargs="*")

    crypto_parser = subparsers.add_parser("crypto", help="Run crypto demo")
    crypto_parser.add_argument("message")

    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    args = _parse_args(argv or sys.argv[1:])
    config = load_config()
    service = BlockchainService(config.blockchain)

    if args.command == "wallet":
        wallet = service.create_wallet()
        _print(wallet.to_dict())
        return

    if args.command == "balance":
        _print({"address": args.address, "balance": service.get_balance(args.address)})
        return

    if args.command == "transfer":
        result = service.submit_transaction(args.sender, args.recipient, args.amount)
        _print({"transaction": result.transaction.to_dict(), "pending": result.pending_count})
        return

    if args.command == "mine":
        result = service.mine(args.miner_address)
        _print(
            {
                "block_hash": result.block_hash,
                "block_index": result.block_index,
                "transactions": result.transaction_count,
            }
        )
        return

    if args.command == "chain":
        _print(service.blockchain.to_dict())
        return

    if args.command == "metrics":
        _print(service.metrics().to_dict())
        return

    if args.command == "deploy":
        params = {}
        if args.contract_type == "token":
            params = {"symbol": args.symbol, "decimals": args.decimals}
        contract = service.deploy_contract(args.contract_type, **params)
        _print(contract)
        return

    if args.command == "call":
        result = service.call_contract(args.address, args.sender, args.method, list(args.args))
        _print(result)
        return

    if args.command == "crypto":
        _crypto_demo(args.message)
        return


if __name__ == "__main__":
    main()
