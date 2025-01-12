import base64
import os
from pathlib import Path

from .file_processor import FileProcessor


class SecureKeyManager:
    def __init__(self):
        self.file_processor = FileProcessor()
        self.key_dir = Path("keys")
        self.key_dir.mkdir(exist_ok=True)

    def generate_key(self) -> bytes:
        """Generate a new 256-bit key"""
        return os.urandom(32)  # 32 bytes = 256 bits

    def save_key(self, key: bytes, key_path: Path, use_base64: bool = False) -> None:
        """Save a key to file, optionally in base64 format"""
        # Ensure the key is exactly 32 bytes
        if len(key) != 32:
            raise ValueError(f"Key must be exactly 32 bytes, got {len(key)} bytes")

        if use_base64:
            # For base64 keys, write directly to avoid double encoding
            encoded_key = base64.b64encode(key).decode("utf-8")
            with open(key_path, "w") as f:
                f.write(encoded_key)
        else:
            with open(key_path, "wb") as f:
                f.write(key)

    def read_key(self, key_path: str) -> bytes:
        """Read a key from file, handling both binary and base64 formats"""
        path = Path(key_path)

        # Try reading as base64 first
        try:
            with open(path, "r") as f:
                content = f.read().strip()
                try:
                    key = base64.b64decode(content)
                    if len(key) == 32:
                        return key
                except:
                    pass
        except:
            pass

        # Try reading as binary
        try:
            with open(path, "rb") as f:
                key = f.read()
                if len(key) == 32:
                    return key
        except:
            pass

        raise ValueError(f"Could not read valid 32-byte key from {key_path}")
