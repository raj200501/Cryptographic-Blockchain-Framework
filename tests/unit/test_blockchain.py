import pytest

from acbf.blockchain import Blockchain, Transaction


def test_blockchain_mining_and_balance():
    chain = Blockchain(difficulty=2, mining_reward=10)
    tx = Transaction(sender="alice", recipient="bob", amount=5)
    chain.add_transaction(tx)
    mined_block = chain.mine_pending_transactions("miner")
    assert mined_block.hash.startswith("0" * chain.difficulty)
    assert chain.get_balance("alice") == -5
    assert chain.get_balance("bob") == 5
    assert chain.get_balance("miner") == 10
    assert chain.is_valid()


def test_transaction_amount_validation():
    chain = Blockchain()
    with pytest.raises(ValueError):
        chain.add_transaction(Transaction(sender="alice", recipient="bob", amount=0))
