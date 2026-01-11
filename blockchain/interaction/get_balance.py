from acbf.config import load_config
from acbf.service import BlockchainService


def get_balance(address: str) -> float:
    config = load_config()
    service = BlockchainService(config.blockchain)
    return service.get_balance(address)


def main():
    address = "demo-address"
    balance = get_balance(address)
    print(f"Balance: {balance} ACBF")


if __name__ == "__main__":
    main()
