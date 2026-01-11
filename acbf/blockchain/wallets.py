"""Wallet utilities for the local blockchain."""

from __future__ import annotations

import dataclasses
import secrets
from typing import Dict

from acbf.crypto.hashing import sha256_hexdigest


@dataclasses.dataclass
class Wallet:
    address: str
    secret: str

    def to_dict(self) -> Dict[str, str]:
        return {"address": self.address, "secret": self.secret}


def generate_wallet() -> Wallet:
    secret = secrets.token_hex(16)
    address = sha256_hexdigest(secret)[:32]
    return Wallet(address=address, secret=secret)
