"""Hash utilities."""

from __future__ import annotations

import hashlib
from typing import Union


def sha256_digest(data: Union[str, bytes]) -> bytes:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).digest()


def sha256_hexdigest(data: Union[str, bytes]) -> str:
    return sha256_digest(data).hex()
