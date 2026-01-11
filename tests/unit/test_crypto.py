from acbf.crypto.aes import AESCipher
from acbf.crypto.hashing import sha256_hexdigest
from acbf.crypto.rsa import generate_rsa_keypair, rsa_decrypt, rsa_encrypt


def test_aes_encrypt_decrypt_roundtrip():
    key = AESCipher.generate_key()
    cipher = AESCipher(key)
    plaintext = b"acbf test"
    bundle = cipher.encrypt(plaintext)
    recovered = cipher.decrypt(bundle)
    assert recovered == plaintext


def test_rsa_encrypt_decrypt_roundtrip():
    keypair = generate_rsa_keypair()
    plaintext = b"rsa test"
    ciphertext = rsa_encrypt(keypair.public_key, plaintext)
    recovered = rsa_decrypt(keypair.private_key, ciphertext)
    assert recovered == plaintext


def test_sha256_hashing():
    digest = sha256_hexdigest("acbf")
    assert digest == "f8f206de151e8ad397d6508ebd075ec984175a15f84f838c07415cc6c56a63f9"
