"""Base classes for simulated smart contracts."""

from __future__ import annotations

import dataclasses
from typing import Dict, List


@dataclasses.dataclass
class ContractCall:
    sender: str
    method: str
    args: List[object]


class SmartContract:
    """Base class for simulated smart contracts."""

    def __init__(self, address: str) -> None:
        self.address = address

    def describe(self) -> Dict[str, object]:
        return {"address": self.address, "type": self.__class__.__name__}

    def execute(self, call: ContractCall) -> Dict[str, object]:
        raise NotImplementedError
