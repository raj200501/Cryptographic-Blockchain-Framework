"""Core blockchain implementation used for local simulation."""

from __future__ import annotations

import dataclasses
import json
import time
from typing import Dict, List, Optional

from acbf.crypto.hashing import sha256_hexdigest


@dataclasses.dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float
    timestamp: float = dataclasses.field(default_factory=lambda: time.time())
    metadata: Dict[str, str] = dataclasses.field(default_factory=dict)

    def to_dict(self) -> Dict[str, object]:
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }

    def hash(self) -> str:
        return sha256_hexdigest(json.dumps(self.to_dict(), sort_keys=True))


@dataclasses.dataclass
class Block:
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    nonce: int = 0
    hash: str = ""

    def to_dict(self) -> Dict[str, object]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
        }

    def compute_hash(self) -> str:
        block_string = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "transactions": [tx.to_dict() for tx in self.transactions],
                "previous_hash": self.previous_hash,
                "nonce": self.nonce,
            },
            sort_keys=True,
        )
        return sha256_hexdigest(block_string)


class Blockchain:
    """A simple proof-of-work blockchain for local simulation."""

    def __init__(self, difficulty: int = 3, mining_reward: int = 50) -> None:
        self.difficulty = difficulty
        self.mining_reward = mining_reward
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0",
        )
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def latest_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction) -> None:
        if transaction.amount <= 0:
            raise ValueError("Transaction amount must be positive")
        if not transaction.sender or not transaction.recipient:
            raise ValueError("Transaction must include sender and recipient")
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address: str) -> Block:
        if not self.pending_transactions:
            raise RuntimeError("No transactions to mine")
        reward_tx = Transaction(
            sender="SYSTEM",
            recipient=miner_address,
            amount=self.mining_reward,
            metadata={"type": "mining_reward"},
        )
        transactions = self.pending_transactions + [reward_tx]
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=transactions,
            previous_hash=self.latest_block.hash,
        )
        self._proof_of_work(block)
        self.chain.append(block)
        self.pending_transactions = []
        return block

    def _proof_of_work(self, block: Block) -> None:
        block.nonce = 0
        computed_hash = block.compute_hash()
        target = "0" * self.difficulty
        while not computed_hash.startswith(target):
            block.nonce += 1
            computed_hash = block.compute_hash()
        block.hash = computed_hash

    def get_balance(self, address: str) -> float:
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.recipient == address:
                    balance += tx.amount
        for tx in self.pending_transactions:
            if tx.sender == address:
                balance -= tx.amount
        return balance

    def is_valid(self) -> bool:
        for index in range(1, len(self.chain)):
            current = self.chain[index]
            previous = self.chain[index - 1]
            if current.previous_hash != previous.hash:
                return False
            if current.compute_hash() != current.hash:
                return False
        return True

    def to_dict(self) -> Dict[str, object]:
        return {
            "difficulty": self.difficulty,
            "mining_reward": self.mining_reward,
            "length": len(self.chain),
            "pending_transactions": [tx.to_dict() for tx in self.pending_transactions],
            "chain": [block.to_dict() for block in self.chain],
        }

    def find_transaction(self, tx_hash: str) -> Optional[Transaction]:
        for block in self.chain:
            for tx in block.transactions:
                if tx.hash() == tx_hash:
                    return tx
        for tx in self.pending_transactions:
            if tx.hash() == tx_hash:
                return tx
        return None
