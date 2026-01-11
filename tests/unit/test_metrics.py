from acbf.blockchain import Blockchain, Transaction
from acbf.metrics import collect_metrics


def test_collect_metrics():
    chain = Blockchain(difficulty=1, mining_reward=5)
    chain.add_transaction(Transaction("alice", "bob", 2))
    chain.mine_pending_transactions("miner")

    metrics = collect_metrics(chain)
    assert metrics.block_count == 2
    assert metrics.transaction_count == 2
    assert metrics.pending_transactions == 0
    assert metrics.unique_addresses >= 3
    assert metrics.total_supply == 5
    assert metrics.mining_rewards == 5
    assert metrics.chain_valid is True
