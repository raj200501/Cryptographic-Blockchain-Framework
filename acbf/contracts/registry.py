"""Registry for simulated smart contracts."""

from __future__ import annotations

import uuid
from typing import Dict

from acbf.contracts.base import ContractCall, SmartContract
from acbf.contracts.storage import SimpleStorageContract
from acbf.contracts.token import TokenContract


class ContractRegistry:
    """Keeps track of deployed contracts in-memory."""

    def __init__(self) -> None:
        self._contracts: Dict[str, SmartContract] = {}

    def deploy(self, contract_type: str, **kwargs: object) -> SmartContract:
        address = uuid.uuid4().hex
        if contract_type == "token":
            contract = TokenContract(address=address, **kwargs)
        elif contract_type == "storage":
            contract = SimpleStorageContract(address=address)
        else:
            raise ValueError(f"Unsupported contract type: {contract_type}")
        self._contracts[address] = contract
        return contract

    def get(self, address: str) -> SmartContract:
        if address not in self._contracts:
            raise KeyError(f"Contract not found: {address}")
        return self._contracts[address]

    def call(self, address: str, call: ContractCall) -> Dict[str, object]:
        contract = self.get(address)
        return contract.execute(call)

    def list_contracts(self) -> Dict[str, object]:
        return {address: contract.describe() for address, contract in self._contracts.items()}
