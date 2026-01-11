"""Token contract simulation."""

from __future__ import annotations

from typing import Dict

from acbf.contracts.base import ContractCall, SmartContract


class TokenContract(SmartContract):
    """Simple token contract with mint and transfer."""

    def __init__(self, address: str, symbol: str = "ACBF", decimals: int = 2) -> None:
        super().__init__(address)
        self.symbol = symbol
        self.decimals = decimals
        self.balances: Dict[str, float] = {}

    def mint(self, recipient: str, amount: float) -> Dict[str, object]:
        if amount <= 0:
            raise ValueError("Mint amount must be positive")
        self.balances[recipient] = self.balances.get(recipient, 0.0) + amount
        return {"recipient": recipient, "amount": amount}

    def transfer(self, sender: str, recipient: str, amount: float) -> Dict[str, object]:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if self.balances.get(sender, 0.0) < amount:
            raise ValueError("Insufficient token balance")
        self.balances[sender] -= amount
        self.balances[recipient] = self.balances.get(recipient, 0.0) + amount
        return {"sender": sender, "recipient": recipient, "amount": amount}

    def balance_of(self, address: str) -> Dict[str, object]:
        return {"address": address, "balance": self.balances.get(address, 0.0)}

    def describe(self) -> Dict[str, object]:
        base = super().describe()
        base.update({"symbol": self.symbol, "decimals": self.decimals})
        return base

    def execute(self, call: ContractCall) -> Dict[str, object]:
        if call.method == "mint":
            recipient, amount = call.args
            return self.mint(recipient, float(amount))
        if call.method == "transfer":
            recipient, amount = call.args
            return self.transfer(call.sender, recipient, float(amount))
        if call.method == "balance_of":
            address = call.args[0]
            return self.balance_of(address)
        raise ValueError(f"Unknown method: {call.method}")
