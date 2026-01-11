"""Pure Python AES-128 implementation for educational purposes.

This implementation supports CBC mode with PKCS7 padding and is intended for
local demos. It is not optimized for performance.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Tuple

BLOCK_SIZE = 16

S_BOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]

INV_S_BOX = [0] * 256
for i, value in enumerate(S_BOX):
    INV_S_BOX[value] = i

RCON = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
]


def _xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(i ^ j for i, j in zip(a, b))


def _pad(data: bytes) -> bytes:
    padding_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([padding_len] * padding_len)


def _unpad(data: bytes) -> bytes:
    if not data:
        raise ValueError("Invalid padding")
    padding_len = data[-1]
    if padding_len < 1 or padding_len > BLOCK_SIZE:
        raise ValueError("Invalid padding length")
    if data[-padding_len:] != bytes([padding_len] * padding_len):
        raise ValueError("Invalid padding bytes")
    return data[:-padding_len]


def _sub_bytes(state: List[int]) -> None:
    for i in range(16):
        state[i] = S_BOX[state[i]]


def _inv_sub_bytes(state: List[int]) -> None:
    for i in range(16):
        state[i] = INV_S_BOX[state[i]]


def _shift_rows(state: List[int]) -> None:
    rows = [state[i::4] for i in range(4)]
    for i in range(4):
        rows[i] = rows[i][i:] + rows[i][:i]
    state[:] = [rows[i % 4][i // 4] for i in range(16)]


def _inv_shift_rows(state: List[int]) -> None:
    rows = [state[i::4] for i in range(4)]
    for i in range(4):
        rows[i] = rows[i][-i:] + rows[i][:-i]
    state[:] = [rows[i % 4][i // 4] for i in range(16)]


def _xtime(a: int) -> int:
    return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else (a << 1)


def _mix_single_column(column: List[int]) -> List[int]:
    t = column[0] ^ column[1] ^ column[2] ^ column[3]
    u = column[0]
    column[0] ^= t ^ _xtime(column[0] ^ column[1])
    column[1] ^= t ^ _xtime(column[1] ^ column[2])
    column[2] ^= t ^ _xtime(column[2] ^ column[3])
    column[3] ^= t ^ _xtime(column[3] ^ u)
    return column


def _mix_columns(state: List[int]) -> None:
    for i in range(4):
        column = state[i * 4:(i + 1) * 4]
        state[i * 4:(i + 1) * 4] = _mix_single_column(column)


def _inv_mix_columns(state: List[int]) -> None:
    for i in range(4):
        column = state[i * 4:(i + 1) * 4]
        u = _xtime(_xtime(column[0] ^ column[2]))
        v = _xtime(_xtime(column[1] ^ column[3]))
        column[0] ^= u
        column[1] ^= v
        column[2] ^= u
        column[3] ^= v
        state[i * 4:(i + 1) * 4] = _mix_single_column(column)


def _add_round_key(state: List[int], round_key: List[int]) -> None:
    for i in range(16):
        state[i] ^= round_key[i]


def _expand_key(key: bytes) -> List[List[int]]:
    key_symbols = list(key)
    if len(key_symbols) != 16:
        raise ValueError("AES-128 key must be 16 bytes")
    round_keys = [key_symbols[i:i + 4] for i in range(0, len(key_symbols), 4)]
    for i in range(4, 44):
        temp = round_keys[i - 1].copy()
        if i % 4 == 0:
            temp = temp[1:] + temp[:1]
            temp = [S_BOX[b] for b in temp]
            temp[0] ^= RCON[(i // 4) - 1]
        new_word = [round_keys[i - 4][j] ^ temp[j] for j in range(4)]
        round_keys.append(new_word)
    return [sum(round_keys[i:i + 4], []) for i in range(0, len(round_keys), 4)]


def _encrypt_block(block: bytes, round_keys: List[List[int]]) -> bytes:
    state = list(block)
    _add_round_key(state, round_keys[0])
    for round_index in range(1, 10):
        _sub_bytes(state)
        _shift_rows(state)
        _mix_columns(state)
        _add_round_key(state, round_keys[round_index])
    _sub_bytes(state)
    _shift_rows(state)
    _add_round_key(state, round_keys[10])
    return bytes(state)


def _decrypt_block(block: bytes, round_keys: List[List[int]]) -> bytes:
    state = list(block)
    _add_round_key(state, round_keys[10])
    for round_index in range(9, 0, -1):
        _inv_shift_rows(state)
        _inv_sub_bytes(state)
        _add_round_key(state, round_keys[round_index])
        _inv_mix_columns(state)
    _inv_shift_rows(state)
    _inv_sub_bytes(state)
    _add_round_key(state, round_keys[0])
    return bytes(state)


@dataclass(frozen=True)
class AESBundle:
    iv: bytes
    ciphertext: bytes

    def as_bytes(self) -> bytes:
        return self.iv + self.ciphertext


class AESCipher:
    """AES-128 CBC cipher for educational use."""

    def __init__(self, key: bytes) -> None:
        if len(key) != 16:
            raise ValueError("AES-128 key must be 16 bytes")
        self._key = key
        self._round_keys = _expand_key(key)

    @classmethod
    def generate_key(cls, length: int = 16) -> bytes:
        if length != 16:
            raise ValueError("AES-128 key length must be 16 bytes")
        return os.urandom(length)

    def encrypt(self, plaintext: bytes) -> AESBundle:
        iv = os.urandom(BLOCK_SIZE)
        padded = _pad(plaintext)
        blocks = [padded[i:i + BLOCK_SIZE] for i in range(0, len(padded), BLOCK_SIZE)]
        ciphertext_blocks = []
        previous = iv
        for block in blocks:
            xor_block = _xor_bytes(block, previous)
            encrypted = _encrypt_block(xor_block, self._round_keys)
            ciphertext_blocks.append(encrypted)
            previous = encrypted
        return AESBundle(iv=iv, ciphertext=b"".join(ciphertext_blocks))

    def decrypt(self, bundle: AESBundle) -> bytes:
        blocks = [bundle.ciphertext[i:i + BLOCK_SIZE] for i in range(0, len(bundle.ciphertext), BLOCK_SIZE)]
        plaintext_blocks = []
        previous = bundle.iv
        for block in blocks:
            decrypted = _decrypt_block(block, self._round_keys)
            plaintext_blocks.append(_xor_bytes(decrypted, previous))
            previous = block
        return _unpad(b"".join(plaintext_blocks))

    def encrypt_bytes(self, plaintext: bytes) -> bytes:
        bundle = self.encrypt(plaintext)
        return bundle.as_bytes()

    def decrypt_bytes(self, payload: bytes) -> bytes:
        iv, ciphertext = payload[:BLOCK_SIZE], payload[BLOCK_SIZE:]
        return self.decrypt(AESBundle(iv=iv, ciphertext=ciphertext))


def demo_encrypt_decrypt(message: str) -> Tuple[bytes, bytes]:
    key = AESCipher.generate_key()
    cipher = AESCipher(key)
    bundle = cipher.encrypt(message.encode("utf-8"))
    plaintext = cipher.decrypt(bundle)
    return bundle.as_bytes(), plaintext
