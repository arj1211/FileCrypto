import argparse
import logging
import sys
from pathlib import Path

from crypto.encryptor import SecureEncryptor
from crypto.key_exchange import SecureKeyExchange
from crypto.key_manager import SecureKeyManager
from crypto.metadata_manager import MetadataManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecureFileProcessor:
    def __init__(self):
        # Create keys directory if it doesn't exist
        keys_dir = Path("keys")
        keys_dir.mkdir(exist_ok=True)

        self.key_exchange = SecureKeyExchange()
        self.key_manager = SecureKeyManager(storage_path=str(keys_dir))
        self.encryptor = SecureEncryptor()
        self.metadata_manager = MetadataManager()

    def encrypt_file(self, input_path: str, output_path: str = None) -> None:
        try:
            if output_path is None:
                output_path = input_path + ".encrypted"

            with open(input_path, "rb") as f:
                data = f.read()

            key = self.key_manager.generate_key()
            encrypted_data = self.encryptor.encrypt(data, key)

            with open(output_path, "wb") as f:
                f.write(encrypted_data)

            logger.info(f"Successfully encrypted {input_path} to {output_path}")

        except Exception as e:
            logger.error(f"Failed to encrypt file: {str(e)}")
            raise

    def decrypt_file(self, input_path: str, output_path: str = None) -> None:
        try:
            if output_path is None:
                output_path = input_path.replace(".encrypted", "")
                if output_path == input_path:
                    output_path = input_path + ".decrypted"

            with open(input_path, "rb") as f:
                encrypted_data = f.read()

            key = self.key_manager.get_key()
            decrypted_data = self.encryptor.decrypt(encrypted_data, key)

            with open(output_path, "wb") as f:
                f.write(decrypted_data)

            logger.info(f"Successfully decrypted {input_path} to {output_path}")

        except Exception as e:
            logger.error(f"Failed to decrypt file: {str(e)}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Secure file encryption/decryption tool"
    )
    parser.add_argument(
        "action", choices=["encrypt", "decrypt"], help="Action to perform"
    )
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("--output", "-o", help="Output file path (optional)")

    args = parser.parse_args()

    try:
        processor = SecureFileProcessor()

        if args.action == "encrypt":
            processor.encrypt_file(args.input_file, args.output)
        else:
            processor.decrypt_file(args.input_file, args.output)

        return 0

    except Exception as e:
        logger.error(f"Failed to process file: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
