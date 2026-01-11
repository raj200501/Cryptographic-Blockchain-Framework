from acbf.crypto.aes import AESCipher


def encrypt_aes(key, plaintext):
    cipher = AESCipher(key)
    return cipher.encrypt_bytes(plaintext)


def main():
    key = AESCipher.generate_key()
    plaintext = b"This is a secret message"
    ciphertext = encrypt_aes(key, plaintext)
    print(f"Ciphertext: {ciphertext.hex()}")


if __name__ == "__main__":
    main()
