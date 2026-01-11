from acbf.config import load_config
from acbf.service import BlockchainService


def interact_with_contract(contract_address, sender="demo"):
    config = load_config()
    service = BlockchainService(config.blockchain)
    result = service.call_contract(contract_address, sender, "set", ["example", 123])
    print(f"Set Data Result: {result}")
    result = service.call_contract(contract_address, sender, "get", ["example"])
    print(f"Stored Data: {result}")


def main():
    config = load_config()
    service = BlockchainService(config.blockchain)
    contract = service.deploy_contract("storage")
    interact_with_contract(contract["address"])


if __name__ == "__main__":
    main()
