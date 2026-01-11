import json

from acbf.config import load_config
from acbf.service import BlockchainService


def deploy_contract(compiled_contract, contract_type: str = "storage"):
    config = load_config()
    service = BlockchainService(config.blockchain)
    return service.deploy_contract(contract_type)


def main():
    with open("compiled_contract.json", "r", encoding="utf-8") as file:
        compiled_contract = json.load(file)

    contract = deploy_contract(compiled_contract)
    print(f"Contract deployed at address: {contract['address']}")


if __name__ == "__main__":
    main()
