from cryptography.hazmat.primitives import serialization

from crypto.encryptor import Encryptor
from crypto.key_exchange import KeyExchange
from crypto.key_manager import KeyManager


def main():
    # Step 1: Key Generation
    key_manager = KeyManager()
    print("Generating and storing a new encryption key...")
    key = key_manager.generate_and_store_key()
    print(f"Generated key: {key.hex()}")

    # Step 2: Simulate Secure Key Exchange
    print("Simulating secure key exchange...")
    key_exchange = KeyExchange()
    peer_public_key = key_exchange.public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    # Simulate using the same public key for simplicity
    shared_key = key_exchange.perform_key_exchange(peer_public_key)
    print(f"Derived shared key: {shared_key.hex()}")

    # Step 3: Encrypt Data
    print("Encrypting data...")
    encryptor = Encryptor()
    data = b"This is some sensitive data to encrypt"
    iv, ciphertext, tag, encrypted_transaction_key = encryptor.encrypt_data(
        data, shared_key
    )

    # Debugging prints
    print("IV:", iv.hex())
    print("Ciphertext:", ciphertext.hex())
    print("Tag:", tag.hex())
    print("Encrypted Transaction Key:", encrypted_transaction_key.hex())

    print("Encryption completed successfully!")

    # Step 4: Decrypt Data
    print("Decrypting data...")
    decrypted_data = encryptor.decrypt_data(
        iv, ciphertext, tag, encrypted_transaction_key, shared_key
    )
    print(f"Decrypted data: {decrypted_data}")


if __name__ == "__main__":
    main()
