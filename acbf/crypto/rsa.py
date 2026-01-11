"""Pure Python RSA helper utilities for educational use."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import secrets


def _egcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    g, y, x = _egcd(b % a, a)
    return g, x - (b // a) * y, y


def _modinv(a: int, m: int) -> int:
    g, x, _ = _egcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    return x % m


def _is_probable_prime(n: int, k: int = 5) -> bool:
    if n in (2, 3):
        return True
    if n <= 1 or n % 2 == 0:
        return False

    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _generate_prime(bits: int) -> int:
    while True:
        candidate = secrets.randbits(bits) | 1 | (1 << (bits - 1))
        if _is_probable_prime(candidate):
            return candidate


@dataclass(frozen=True)
class RSAKeyPair:
    private_key: Tuple[int, int]
    public_key: Tuple[int, int]

    def serialize_private(self) -> str:
        n, d = self.private_key
        return f"{n}:{d}"

    def serialize_public(self) -> str:
        n, e = self.public_key
        return f"{n}:{e}"


def generate_rsa_keypair(key_size: int = 512) -> RSAKeyPair:
    if key_size < 256:
        raise ValueError("Key size too small for demo")
    p = _generate_prime(key_size // 2)
    q = _generate_prime(key_size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = _modinv(e, phi)
    return RSAKeyPair(private_key=(n, d), public_key=(n, e))


def rsa_encrypt(public_key: Tuple[int, int], plaintext: bytes) -> bytes:
    n, e = public_key
    message_int = int.from_bytes(plaintext, byteorder="big")
    if message_int >= n:
        raise ValueError("Message too large for RSA key")
    cipher_int = pow(message_int, e, n)
    length = (n.bit_length() + 7) // 8
    return cipher_int.to_bytes(length, byteorder="big")


def rsa_decrypt(private_key: Tuple[int, int], ciphertext: bytes) -> bytes:
    n, d = private_key
    cipher_int = int.from_bytes(ciphertext, byteorder="big")
    message_int = pow(cipher_int, d, n)
    length = (n.bit_length() + 7) // 8
    return message_int.to_bytes(length, byteorder="big").lstrip(b"\x00")


def demo_encrypt_decrypt(message: str) -> Tuple[bytes, bytes]:
    keypair = generate_rsa_keypair()
    ciphertext = rsa_encrypt(keypair.public_key, message.encode("utf-8"))
    plaintext = rsa_decrypt(keypair.private_key, ciphertext)
    return ciphertext, plaintext
