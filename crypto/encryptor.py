import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Encryptor:
    def encrypt_data(self, data, shared_key):
        transaction_key = os.urandom(32)
        iv = os.urandom(12)

        # Encrypt data with transaction key
        cipher = Cipher(algorithms.AES(transaction_key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()

        # Encrypt transaction key with shared key
        cipher_shared = Cipher(algorithms.AES(shared_key), modes.GCM(iv))
        encryptor_shared = cipher_shared.encryptor()
        encrypted_transaction_key = (
            encryptor_shared.update(transaction_key) + encryptor_shared.finalize()
        )

        return iv, ciphertext, encryptor.tag, encrypted_transaction_key

    def decrypt_data(self, iv, ciphertext, tag, encrypted_transaction_key, shared_key):
        print(f"Debug - Decrypting Transaction Key:")
        print(f"IV: {iv.hex()}")
        print(f"Tag: {tag.hex()}")
        print(f"Encrypted Transaction Key: {encrypted_transaction_key.hex()}")
        print(f"Shared Key: {shared_key.hex()}")

        # Decrypt the transaction key using the shared key
        cipher_shared = Cipher(algorithms.AES(shared_key), modes.GCM(iv, tag))
        decryptor_shared = cipher_shared.decryptor()

        try:
            transaction_key = decryptor_shared.update(encrypted_transaction_key)
            transaction_key += (
                decryptor_shared.finalize()
            )  # Separate finalize to avoid InvalidTag error
        except Exception as e:
            print(f"Failed to decrypt the transaction key: {e}")
            raise

        # Decrypt the data using the transaction key
        cipher = Cipher(algorithms.AES(transaction_key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        return plaintext
