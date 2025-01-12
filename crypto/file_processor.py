# crypto/file_processor.py
from pathlib import Path

from .encryptor import SecureEncryptor
from .key_manager import SecureKeyManager


class SecureFileProcessor:
    def __init__(self, key_dir: str = "keys"):
        self.key_manager = SecureKeyManager(key_dir)
        self.encryptor = SecureEncryptor()

    def encrypt_file(self, input_path: str, output_path: str = None) -> None:
        """Encrypt a file using AES-256."""
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Generate output path if not provided
        if output_path is None:
            output_path = str(input_path) + ".encrypted"

        # Ensure parent directory exists
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Get or generate key
        try:
            key = self.key_manager.get_key()
        except ValueError:
            key = self.key_manager.generate_key()

        # Read and encrypt file
        with open(input_path, "rb") as f:
            data = f.read()
            encrypted_data = self.encryptor.encrypt(data, key)

        # Write encrypted data
        with open(output_path, "wb") as f:
            f.write(encrypted_data)

    def decrypt_file(self, input_path: str, output_path: str = None) -> None:
        """Decrypt an encrypted file."""
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Generate output path if not provided
        if output_path is None:
            output_path = str(input_path).replace(".encrypted", "")

        # Ensure parent directory exists
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Get key
        key = self.key_manager.get_key()

        # Read and decrypt file
        with open(input_path, "rb") as f:
            encrypted_data = f.read()
            try:
                decrypted_data = self.encryptor.decrypt(encrypted_data, key)
            except Exception as e:
                raise ValueError(f"Failed to decrypt file: {e}")

        # Write decrypted data
        with open(output_path, "wb") as f:
            f.write(decrypted_data)
