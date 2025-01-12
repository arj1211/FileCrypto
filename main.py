import argparse
from pathlib import Path

from crypto.encryptor import SecureEncryptor
from crypto.file_processor import FileProcessor
from crypto.key_manager import SecureKeyManager


class FileCrypto:
    def __init__(self):
        self.encryptor = SecureEncryptor()
        self.key_manager = SecureKeyManager()
        self.file_processor = FileProcessor()

    def encrypt_file(
        self, input_path: Path, output_path: Path, key: bytes, use_base64: bool
    ) -> None:
        """Encrypt a file using the provided key"""
        data = self.file_processor.read_file(input_path)
        encrypted_data = self.encryptor.encrypt(data, key)
        self.file_processor.write_file(output_path, encrypted_data, use_base64)

    def decrypt_file(
        self, input_path: Path, output_path: Path, key: bytes, use_base64: bool
    ) -> None:
        """Decrypt a file using the provided key"""
        encrypted_data = self.file_processor.read_file(input_path)
        decrypted_data = self.encryptor.decrypt(encrypted_data, key)
        self.file_processor.write_file(output_path, decrypted_data, use_base64)


def main():
    parser = argparse.ArgumentParser(description="File encryption/decryption utility")
    parser.add_argument("action", choices=["encrypt", "decrypt", "generate-key"])
    parser.add_argument("file", nargs="?", help="File to process")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument(
        "--base64",
        action="store_true",
        help="Save files in base64 encoded format (readable in text editor)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    crypto = FileCrypto()

    if args.debug:
        print("Debug mode enabled")

    if args.action == "generate-key":
        key = crypto.key_manager.generate_key()
        key_path = Path("keys/encryption_key.key")
        if args.debug:
            print(f"Generated key length: {len(key)} bytes")
        crypto.key_manager.save_key(key, key_path, args.base64)
        print(f"Key generated and saved to {key_path}")
        return

    if not args.file:
        parser.error("File path is required for encryption/decryption")

    input_path = Path(args.file)
    if not input_path.exists():
        print(f"Error: File {input_path} not found")
        return

    key = crypto.key_manager.read_key("keys/encryption_key.key")
    if args.debug:
        print(f"Read key length: {len(key)} bytes")

    if args.action == "encrypt":
        output_path = (
            Path(args.output)
            if args.output
            else input_path.with_suffix(input_path.suffix + ".encrypted")
        )
        if args.debug:
            print(f"Input file size: {input_path.stat().st_size} bytes")
        crypto.encrypt_file(input_path, output_path, key, args.base64)
        if args.debug:
            print(f"Output file size: {output_path.stat().st_size} bytes")
        print(f"File encrypted and saved to {output_path}")

    elif args.action == "decrypt":
        output_path = Path(args.output) if args.output else input_path.with_suffix("")
        if args.debug:
            print(f"Input file size: {input_path.stat().st_size} bytes")
        crypto.decrypt_file(input_path, output_path, key, args.base64)
        if args.debug:
            print(f"Output file size: {output_path.stat().st_size} bytes")
        print(f"File decrypted and saved to {output_path}")


if __name__ == "__main__":
    main()
