from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

def decrypt_rsa(private_key, ciphertext):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext

def main():
    private_key = serialization.load_pem_private_key(
        b"-----BEGIN PRIVATE KEY-----\n...",
        password=None,
    )
    ciphertext = b"\x00\x00..."  # Example ciphertext
    plaintext = decrypt_rsa(private_key, ciphertext)
    print(f"Plaintext: {plaintext}")

if __name__ == "__main__":
    main()
