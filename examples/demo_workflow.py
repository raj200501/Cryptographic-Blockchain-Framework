"""Example workflow for the ACBF service layer.

Run with:
    python examples/demo_workflow.py
"""

from acbf.config import load_config
from acbf.service import BlockchainService


def main() -> None:
    config = load_config()
    service = BlockchainService(config.blockchain)

    alice = service.create_wallet()
    bob = service.create_wallet()

    print("Wallets")
    print(alice.to_dict())
    print(bob.to_dict())

    print("\nSubmitting transaction...")
    result = service.submit_transaction(alice.address, bob.address, 12.5)
    print(result.transaction.to_dict())

    print("\nMining block...")
    mined = service.mine(alice.address)
    print({"block": mined.block_index, "hash": mined.block_hash})

    print("\nBalances")
    print({"alice": service.get_balance(alice.address)})
    print({"bob": service.get_balance(bob.address)})

    print("\nDeploying token contract")
    token = service.deploy_contract("token", symbol="ACBF", decimals=2)
    print(token)

    print("\nMinting tokens")
    service.call_contract(token["address"], alice.address, "mint", [alice.address, 100])
    print(service.call_contract(token["address"], alice.address, "balance_of", [alice.address]))

    print("\nChain metrics")
    print(service.metrics().to_dict())


if __name__ == "__main__":
    main()
