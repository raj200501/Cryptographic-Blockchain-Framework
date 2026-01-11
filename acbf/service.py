"""High-level service for the ACBF backend."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from acbf.blockchain import Blockchain, Transaction
from acbf.blockchain.wallets import Wallet, generate_wallet
from acbf.config import BlockchainConfig
from acbf.contracts import ContractCall, ContractRegistry
from acbf.metrics import ChainMetrics, collect_metrics


@dataclass
class TransactionResult:
    transaction: Transaction
    pending_count: int


@dataclass
class MiningResult:
    block_hash: str
    block_index: int
    transaction_count: int


class BlockchainService:
    """Orchestrates blockchain operations and contract registry."""

    def __init__(self, config: BlockchainConfig) -> None:
        self.blockchain = Blockchain(
            difficulty=config.difficulty,
            mining_reward=config.mining_reward,
        )
        self.contracts = ContractRegistry()

    def create_wallet(self) -> Wallet:
        return generate_wallet()

    def submit_transaction(
        self,
        sender: str,
        recipient: str,
        amount: float,
        metadata: Dict[str, str] | None = None,
    ) -> TransactionResult:
        tx = Transaction(sender=sender, recipient=recipient, amount=amount, metadata=metadata or {})
        self.blockchain.add_transaction(tx)
        return TransactionResult(transaction=tx, pending_count=len(self.blockchain.pending_transactions))

    def mine(self, miner_address: str) -> MiningResult:
        block = self.blockchain.mine_pending_transactions(miner_address)
        return MiningResult(
            block_hash=block.hash, block_index=block.index, transaction_count=len(block.transactions)
        )

    def get_balance(self, address: str) -> float:
        return self.blockchain.get_balance(address)

    def deploy_contract(self, contract_type: str, **kwargs: object) -> Dict[str, object]:
        contract = self.contracts.deploy(contract_type, **kwargs)
        return contract.describe()

    def call_contract(self, address: str, sender: str, method: str, args: List[object]) -> Dict[str, object]:
        call = ContractCall(sender=sender, method=method, args=args)
        return self.contracts.call(address, call)

    def list_contracts(self) -> Dict[str, object]:
        return self.contracts.list_contracts()

    def metrics(self) -> ChainMetrics:
        return collect_metrics(self.blockchain)
