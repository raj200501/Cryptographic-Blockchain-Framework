from acbf.crypto.rsa import generate_rsa_keypair, rsa_encrypt


def generate_keys():
    keypair = generate_rsa_keypair()
    return keypair.private_key, keypair.public_key


def encrypt_rsa(public_key, plaintext):
    return rsa_encrypt(public_key, plaintext)


def main():
    _, public_key = generate_keys()
    plaintext = b"This is a secret message"
    ciphertext = encrypt_rsa(public_key, plaintext)
    print(f"Ciphertext: {ciphertext.hex()}")


if __name__ == "__main__":
    main()
