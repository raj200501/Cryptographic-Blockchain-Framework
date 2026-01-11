"""Metrics for the local blockchain."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set

from acbf.blockchain import Blockchain

SYSTEM_ADDRESS = "SYSTEM"


@dataclass(frozen=True)
class ChainMetrics:
    block_count: int
    transaction_count: int
    pending_transactions: int
    unique_addresses: int
    total_supply: float
    mining_rewards: float
    average_transactions_per_block: float
    chain_valid: bool

    def to_dict(self) -> Dict[str, object]:
        return {
            "block_count": self.block_count,
            "transaction_count": self.transaction_count,
            "pending_transactions": self.pending_transactions,
            "unique_addresses": self.unique_addresses,
            "total_supply": self.total_supply,
            "mining_rewards": self.mining_rewards,
            "average_transactions_per_block": self.average_transactions_per_block,
            "chain_valid": self.chain_valid,
        }


def collect_metrics(chain: Blockchain) -> ChainMetrics:
    addresses: Set[str] = set()
    transaction_count = 0
    mining_rewards = 0.0

    for block in chain.chain:
        for tx in block.transactions:
            addresses.update([tx.sender, tx.recipient])
            transaction_count += 1
            if tx.metadata.get("type") == "mining_reward":
                mining_rewards += tx.amount

    tracked_addresses = {address for address in addresses if address != SYSTEM_ADDRESS}
    total_supply = sum(chain.get_balance(address) for address in tracked_addresses)

    average_tx = 0.0
    if chain.chain:
        average_tx = transaction_count / len(chain.chain)

    return ChainMetrics(
        block_count=len(chain.chain),
        transaction_count=transaction_count,
        pending_transactions=len(chain.pending_transactions),
        unique_addresses=len(tracked_addresses),
        total_supply=total_supply,
        mining_rewards=mining_rewards,
        average_transactions_per_block=average_tx,
        chain_valid=chain.is_valid(),
    )
