from acbf.crypto.hashing import sha256_hexdigest


def main():
    message = "This is a secret message"
    digest = sha256_hexdigest(message)
    print(f"SHA-256: {digest}")


if __name__ == "__main__":
    main()
