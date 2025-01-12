# crypto/key_manager.py
import os
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet

from crypto.config import SecurityConfig


class SecureKeyManager:
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.key_file = self.storage_path / "encryption_key.key"
        self._current_key = None

    def generate_key(self) -> bytes:
        """Generate a new encryption key and store it."""
        key = os.urandom(SecurityConfig.AES_KEY_SIZE)
        self._current_key = key

        # Save the key
        self.storage_path.mkdir(parents=True, exist_ok=True)
        with open(self.key_file, "wb") as f:
            f.write(key)

        return key

    def get_key(self) -> bytes:
        """Retrieve the current encryption key."""
        if self._current_key:
            return self._current_key

        if not self.key_file.exists():
            raise ValueError("No encryption key found. Please generate one first.")

        with open(self.key_file, "rb") as f:
            self._current_key = f.read()

        return self._current_key

    def delete_key(self) -> None:
        """Delete the current encryption key."""
        if self.key_file.exists():
            self.key_file.unlink()
        self._current_key = None

    def rotate_key(self) -> bytes:
        """Generate a new key and replace the old one."""
        self.delete_key()
        return self.generate_key()
