from acbf.crypto.aes import AESCipher


def decrypt_aes(key, payload):
    cipher = AESCipher(key)
    return cipher.decrypt_bytes(payload)


def main():
    key = AESCipher.generate_key()
    plaintext = b"This is a secret message"
    cipher = AESCipher(key)
    payload = cipher.encrypt_bytes(plaintext)
    recovered = decrypt_aes(key, payload)
    print(f"Recovered: {recovered.decode('utf-8')}")


if __name__ == "__main__":
    main()
