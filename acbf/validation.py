"""Validation helpers for ACBF inputs."""

from __future__ import annotations

import re
from typing import Any

ADDRESS_PATTERN = re.compile(r"^[a-z0-9-]{3,64}$")


def normalize_address(address: str) -> str:
    if not isinstance(address, str):
        raise ValueError("Address must be a string")
    address = address.strip().lower()
    if not address:
        raise ValueError("Address cannot be empty")
    if not ADDRESS_PATTERN.match(address):
        raise ValueError("Address must be 3-64 chars (letters, numbers, dashes)")
    return address


def normalize_amount(amount: Any) -> float:
    try:
        value = float(amount)
    except (TypeError, ValueError) as exc:
        raise ValueError("Amount must be numeric") from exc
    if value <= 0:
        raise ValueError("Amount must be positive")
    return value
