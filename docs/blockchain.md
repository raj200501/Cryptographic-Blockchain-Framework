# Blockchain Simulation

## Purpose

The ACBF blockchain is a local, deterministic simulation intended for demos and
unit testing. It is not connected to any public chain.

## Core Concepts

### Transactions

Transactions are represented by `acbf.blockchain.core.Transaction` and include:

- `sender` and `recipient` addresses (strings).
- `amount` (float).
- `timestamp` (Unix time).
- `metadata` (arbitrary key/value data).

### Blocks

Blocks include a list of transactions, a previous hash, and a proof-of-work
nonce. Hashes are computed via SHA-256 to create a deterministic chain.

### Proof of Work

The `Blockchain` class performs a simple proof-of-work by requiring the hash to
start with `difficulty` zeros. You can configure the difficulty in
`config/blockchain_config.yaml`.

### Mining Rewards

When a block is mined, the miner receives a reward transaction. This is
configured via `mining_reward`.

### Metrics

`acbf.metrics.collect_metrics` aggregates chain statistics such as total
transactions, unique addresses, and reward totals. The API exposes these via
`GET /metrics` and the CLI via `python -m acbf.cli metrics`.

## Example Usage

```python
from acbf.blockchain import Blockchain, Transaction

chain = Blockchain(difficulty=2, mining_reward=10)
chain.add_transaction(Transaction("alice", "bob", 5))
chain.mine_pending_transactions("miner")

print(chain.get_balance("bob"))
```

## API Equivalents

These core actions map to the backend API:

- `POST /transaction` -> submit transaction
- `POST /mine` -> mine pending transactions
- `GET /balance?address=...` -> retrieve balance
- `GET /chain` -> inspect full chain
- `GET /metrics` -> chain statistics

## Validation Notes

The chain enforces positive amounts and non-empty sender/recipient strings.
Additional validation occurs at the API layer to ensure reasonable input.
