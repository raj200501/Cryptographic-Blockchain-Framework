from acbf.config import load_config
from acbf.service import BlockchainService


def send_transaction(sender: str, recipient: str, amount: float):
    config = load_config()
    service = BlockchainService(config.blockchain)
    return service.submit_transaction(sender, recipient, amount)


def main():
    sender = "demo-sender"
    recipient = "demo-recipient"
    amount = 5.0
    result = send_transaction(sender, recipient, amount)
    print(f"Submitted transaction: {result.transaction.to_dict()}")


if __name__ == "__main__":
    main()
