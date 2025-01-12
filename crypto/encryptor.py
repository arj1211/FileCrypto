import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class SecureEncryptor:
    def __init__(self):
        self.backend = default_backend()

    def _validate_key(self, key: bytes) -> None:
        """Validate the encryption key length"""
        if len(key) != 32:  # We strictly require AES-256
            raise ValueError(
                f"Invalid key size: {len(key)} bytes. Required: 32 bytes (256 bits)"
            )

    def encrypt(self, data: bytes, key: bytes) -> bytes:
        """
        Encrypt data using AES-256-GCM.
        Returns: nonce (12 bytes) + tag (16 bytes) + ciphertext
        """
        self._validate_key(key)

        # Generate a random 96-bit nonce (12 bytes)
        nonce = os.urandom(12)

        # Create an encryptor object
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=self.backend)
        encryptor = cipher.encryptor()

        # Encrypt the data
        ciphertext = encryptor.update(data) + encryptor.finalize()

        # Return nonce + tag + ciphertext
        return nonce + encryptor.tag + ciphertext

    def decrypt(self, encrypted_data: bytes, key: bytes) -> bytes:
        """
        Decrypt data using AES-256-GCM.
        Input format: nonce (12 bytes) + tag (16 bytes) + ciphertext
        """
        self._validate_key(key)

        # Extract nonce and tag
        nonce = encrypted_data[:12]
        tag = encrypted_data[12:28]
        ciphertext = encrypted_data[28:]

        # Create a decryptor object
        cipher = Cipher(
            algorithms.AES(key), modes.GCM(nonce, tag), backend=self.backend
        )
        decryptor = cipher.decryptor()

        # Decrypt the data
        return decryptor.update(ciphertext) + decryptor.finalize()
