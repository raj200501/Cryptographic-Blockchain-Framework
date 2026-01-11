# Cryptography

## Overview

ACBF includes a small cryptography toolkit implemented in pure Python. The goal
is to provide reproducible demos, not production-grade cryptographic services.

The primary helpers live in `acbf.crypto`:

- `AESCipher` for AES-128 CBC encryption/decryption.
- RSA key generation and encryption helpers (toy implementation).
- SHA-256 hashing convenience functions.

## AES Usage

```python
from acbf.crypto.aes import AESCipher

key = AESCipher.generate_key()
cipher = AESCipher(key)

bundle = cipher.encrypt(b"secret")
plaintext = cipher.decrypt(bundle)
```

`AESCipher` uses AES-128 CBC with PKCS7 padding. It is implemented in pure
Python for learning purposes and is not optimized for speed.

## RSA Usage

```python
from acbf.crypto.rsa import generate_rsa_keypair, rsa_encrypt, rsa_decrypt

keypair = generate_rsa_keypair()
ciphertext = rsa_encrypt(keypair.public_key, b"message")
plaintext = rsa_decrypt(keypair.private_key, ciphertext)
```

The RSA implementation is intentionally minimal and intended for demos only.

## SHA-256 Usage

```python
from acbf.crypto.hashing import sha256_hexdigest

print(sha256_hexdigest("acbf"))
```

## Example Script

The legacy scripts under `cryptography/` import these helpers and provide
runnable examples:

- `cryptography/symmetric/aes_encryption.py`
- `cryptography/asymmetric/rsa_encryption.py`
- `cryptography/hash_functions/sha256_hash.py`
