# Cryptography

## Overview

This module provides implementations of various cryptographic techniques, including symmetric encryption (AES), asymmetric encryption (RSA), and hash functions (SHA-256).

## Usage

### Symmetric Encryption (AES)

```python
from cryptography.symmetric.aes_encryption import encrypt_aes
from cryptography.symmetric.aes_decryption import decrypt_aes

key = os.urandom(32)
plaintext = b"This is a secret message"
ciphertext = encrypt_aes(key, plaintext)
decrypted_text = decrypt_aes(key, ciphertext)
