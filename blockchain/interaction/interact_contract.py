from acbf.config import load_config
from acbf.service import BlockchainService


def interact_contract(address: str, sender: str, method: str, args):
    config = load_config()
    service = BlockchainService(config.blockchain)
    return service.call_contract(address, sender, method, args)


def main():
    contract = "demo-contract"
    result = interact_contract(contract, "demo-sender", "balance_of", ["demo-sender"])
    print(f"Contract result: {result}")


if __name__ == "__main__":
    main()
