import pytest

from acbf.contracts import ContractCall, ContractRegistry


def test_token_contract_mint_transfer():
    registry = ContractRegistry()
    contract = registry.deploy("token")
    address = contract.address

    registry.call(address, ContractCall(sender="SYSTEM", method="mint", args=["alice", 25]))
    balance = registry.call(address, ContractCall(sender="alice", method="balance_of", args=["alice"]))
    assert balance["balance"] == 25

    registry.call(address, ContractCall(sender="alice", method="transfer", args=["bob", 5]))
    balance_alice = registry.call(address, ContractCall(sender="alice", method="balance_of", args=["alice"]))
    balance_bob = registry.call(address, ContractCall(sender="bob", method="balance_of", args=["bob"]))
    assert balance_alice["balance"] == 20
    assert balance_bob["balance"] == 5


def test_storage_contract_set_get():
    registry = ContractRegistry()
    contract = registry.deploy("storage")
    address = contract.address

    registry.call(address, ContractCall(sender="alice", method="set", args=["key", 123]))
    result = registry.call(address, ContractCall(sender="alice", method="get", args=["key"]))
    assert result["value"] == 123


def test_unknown_contract_type():
    registry = ContractRegistry()
    with pytest.raises(ValueError):
        registry.deploy("unknown")
