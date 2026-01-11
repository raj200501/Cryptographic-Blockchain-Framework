"""Generate a metrics report after seeding demo transactions."""

from acbf.blockchain import Transaction
from acbf.config import load_config
from acbf.metrics import collect_metrics
from acbf.service import BlockchainService


def seed_chain(service: BlockchainService) -> None:
    service.submit_transaction("alice", "bob", 3)
    service.submit_transaction("bob", "carol", 1.5)
    service.submit_transaction("alice", "dave", 2)
    service.mine("miner-01")

    service.submit_transaction("carol", "alice", 0.75)
    service.submit_transaction("dave", "bob", 0.5)
    service.mine("miner-02")


def main() -> None:
    config = load_config()
    service = BlockchainService(config.blockchain)
    seed_chain(service)

    metrics = collect_metrics(service.blockchain)
    print("Metrics report")
    for key, value in metrics.to_dict().items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
