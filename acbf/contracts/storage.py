"""Simple storage contract simulation."""

from __future__ import annotations

from typing import Dict

from acbf.contracts.base import ContractCall, SmartContract


class SimpleStorageContract(SmartContract):
    """Stores a single value per key."""

    def __init__(self, address: str) -> None:
        super().__init__(address)
        self.storage: Dict[str, object] = {}

    def set_value(self, key: str, value: object) -> Dict[str, object]:
        self.storage[key] = value
        return {"key": key, "value": value}

    def get_value(self, key: str) -> Dict[str, object]:
        return {"key": key, "value": self.storage.get(key)}

    def execute(self, call: ContractCall) -> Dict[str, object]:
        if call.method == "set":
            key, value = call.args
            return self.set_value(str(key), value)
        if call.method == "get":
            key = call.args[0]
            return self.get_value(str(key))
        raise ValueError(f"Unknown method: {call.method}")
