import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class SecureEncryptor:
    VALID_KEY_SIZES = [16, 24, 32]  # AES-128, AES-192, or AES-256 (in bytes)

    def __init__(self):
        self.backend = default_backend()

    def _validate_key(self, key: bytes) -> None:
        """Validate the encryption key length"""
        if len(key) not in self.VALID_KEY_SIZES:
            raise ValueError(
                f"Invalid key size ({len(key)} bytes). "
                f"Key must be one of {self.VALID_KEY_SIZES} bytes long for AES encryption."
            )

    def encrypt(self, data: bytes, key: bytes) -> bytes:
        """Encrypt data using AES in CBC mode with PKCS7 padding"""
        self._validate_key(key)

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        # Add PKCS7 padding
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padded_data = data + bytes([padding_length] * padding_length)

        # Encrypt the data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Return IV + encrypted data
        return iv + encrypted_data

    def decrypt(self, encrypted_data: bytes, key: bytes) -> bytes:
        """Decrypt data using AES in CBC mode with PKCS7 padding"""
        self._validate_key(key)

        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        # Decrypt the data
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove PKCS7 padding
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]
