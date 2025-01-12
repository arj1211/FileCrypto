# crypto/encryptor.py
import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from crypto.config import SecurityConfig


class SecureEncryptor:
    def __init__(self):
        self.block_size = SecurityConfig.BLOCK_SIZE

    def _validate_key(self, key: bytes) -> None:
        """Validate the encryption key."""
        if len(key) != SecurityConfig.AES_KEY_SIZE:
            raise ValueError(
                f"Invalid key length. Expected {SecurityConfig.AES_KEY_SIZE} bytes, "
                f"got {len(key)} bytes"
            )

    def encrypt(self, data: bytes, key: bytes) -> bytes:
        """
        Encrypt data using AES in CBC mode with PKCS7 padding.
        Returns: iv + encrypted_data
        """
        self._validate_key(key)

        # Generate a random IV
        iv = os.urandom(16)  # AES block size is 16 bytes

        # Create padder
        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()

        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

        # Encrypt
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Return IV + encrypted data
        return iv + encrypted_data

    def decrypt(self, encrypted_data: bytes, key: bytes) -> bytes:
        """
        Decrypt data using AES in CBC mode with PKCS7 padding.
        Expects input in format: iv + encrypted_data
        """
        self._validate_key(key)

        # Extract IV and ciphertext
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

        # Decrypt
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove padding
        unpadder = padding.PKCS7(self.block_size).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        return data
