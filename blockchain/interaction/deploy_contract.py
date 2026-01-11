from acbf.config import load_config
from acbf.service import BlockchainService


def deploy_contract(contract_type: str = "token"):
    config = load_config()
    service = BlockchainService(config.blockchain)
    return service.deploy_contract(contract_type)


def main():
    contract = deploy_contract()
    print(f"Deployed contract: {contract}")


if __name__ == "__main__":
    main()
