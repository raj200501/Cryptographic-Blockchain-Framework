from acbf.crypto.rsa import generate_rsa_keypair, rsa_decrypt, rsa_encrypt


def decrypt_rsa(private_key, ciphertext):
    return rsa_decrypt(private_key, ciphertext)


def main():
    keypair = generate_rsa_keypair()
    plaintext = b"This is a secret message"
    ciphertext = rsa_encrypt(keypair.public_key, plaintext)
    recovered = decrypt_rsa(keypair.private_key, ciphertext)
    print(f"Recovered: {recovered.decode('utf-8')}")


if __name__ == "__main__":
    main()
