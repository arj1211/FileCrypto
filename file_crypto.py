import base64
import json
import os
import tempfile
from io import BytesIO
from pathlib import Path

import pyzipper
from cryptography.fernet import Fernet


class FileCrypto:
    def __init__(self):
        self.key = None

    def generate_key(self):
        """Generate a new Fernet encryption key"""
        self.key = Fernet.generate_key()
        return self.key

    def file_to_base64(self, file_path, chunk_size=64 * 1024):
        """Convert file to base64 in chunks"""
        with open(file_path, "rb") as file:
            while chunk := file.read(chunk_size):
                yield base64.b64encode(chunk)

    def encrypt_data(self, data):
        """Encrypt data using Fernet"""
        if not self.key:
            self.generate_key()
        fernet = Fernet(self.key)
        return fernet.encrypt(data)

    def decrypt_data(self, encrypted_data, key):
        """Decrypt data using Fernet"""
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_data)

    def create_protected_zip(self, encrypted_data, key, file_metadata, password):
        """Create AES-encrypted zip with encrypted data, key, and metadata"""
        zip_buffer = BytesIO()

        # Use AES-256 encrypted zip
        with pyzipper.AESZipFile(
            zip_buffer, "w", compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES
        ) as zip_file:
            # Set password
            zip_file.pwd = password.encode()

            # Add encrypted data
            zip_file.writestr("encrypted_data.txt", encrypted_data)

            # Add metadata
            zip_file.writestr("metadata.json", json.dumps(file_metadata))

            # Add key file
            zip_file.writestr("key.txt", key)

        return zip_buffer.getvalue()

    def encrypt_file(self, file_path, password, output_file):
        """Encrypt file and create protected zip archive"""
        # Get file metadata
        path = Path(file_path)
        file_metadata = {
            "original_name": path.name,
            "extension": path.suffix,
            "stem": path.stem,
        }

        # Encrypt file in chunks
        encrypted_chunks = []
        for base64_chunk in self.file_to_base64(file_path):
            encrypted_chunk = self.encrypt_data(base64_chunk)
            encrypted_chunks.append(encrypted_chunk)

        # Join encrypted chunks
        encrypted_data = b"\n".join(encrypted_chunks)

        # Create password-protected zip
        zip_data = self.create_protected_zip(
            encrypted_data, self.key, file_metadata, password
        )

        # Convert final zip to base64
        final_base64 = base64.b64encode(zip_data)

        # Save final base64 string
        output_file = output_file if output_file else "encrypted.txt"
        with open(output_file, "wb") as f:
            f.write(final_base64)

        return output_file

    def decrypt_file(self, encrypted_file_path, password, output_dir=None):
        """Decrypt file from encrypted base64 zip archive"""
        try:
            # Read base64 encoded zip
            with open(encrypted_file_path, "rb") as f:
                zip_data = base64.b64decode(f.read())

            # Create zip file in memory
            zip_buffer = BytesIO(zip_data)

            # Extract files from zip
            with pyzipper.AESZipFile(
                zip_buffer, "r", encryption=pyzipper.WZ_AES
            ) as zip_file:
                try:
                    # Set password for decryption
                    zip_file.pwd = password.encode()

                    # Try to read all required files
                    encrypted_data = zip_file.read("encrypted_data.txt")
                    metadata = json.loads(zip_file.read("metadata.json"))
                    key = zip_file.read("key.txt")
                except (RuntimeError, pyzipper.BadZipFile):
                    raise ValueError("Invalid password or corrupted file")

            # Decrypt data chunks
            try:
                decrypted_content = b""
                for line in encrypted_data.split(b"\n"):
                    if line.strip():
                        # Decrypt chunk
                        decrypted_chunk = self.decrypt_data(line.strip(), key)
                        # Decode base64
                        decoded_chunk = base64.b64decode(decrypted_chunk)
                        decrypted_content += decoded_chunk
            except Exception as e:
                raise ValueError(
                    "Decryption failed - possibly corrupted data or wrong password"
                )

            # Determine output path
            if output_dir:
                output_path = Path(output_dir) / metadata["original_name"]
            else:
                output_path = Path(metadata["original_name"])

            # Save decrypted file
            with open(output_path, "wb") as f:
                f.write(decrypted_content)

            return output_path

        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")


if __name__ == "__main__":
    import sys

    def print_usage():
        print("Usage:")
        print(
            "To encrypt: python file_crypto.py encrypt <file_path> <password> [encrypted_file_name]"
        )
        print(
            "To decrypt: python file_crypto.py decrypt <encrypted_file_path> <password> [output_directory]"
        )

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    crypto = FileCrypto()

    try:
        if sys.argv[1] == "encrypt" and (len(sys.argv) == 4 or len(sys.argv) == 5):
            file_path = sys.argv[2]
            password = sys.argv[3]
            encrypted_file_name = sys.argv[4] if len(sys.argv) == 5 else None

            output_file = crypto.encrypt_file(file_path, password, encrypted_file_name)
            print(f"File encrypted successfully. Output saved to: {output_file}")

        elif sys.argv[1] == "decrypt" and (len(sys.argv) == 4 or len(sys.argv) == 5):
            encrypted_file = sys.argv[2]
            password = sys.argv[3]
            output_dir = sys.argv[4] if len(sys.argv) == 5 else None

            output_file = crypto.decrypt_file(encrypted_file, password, output_dir)
            print(f"File decrypted successfully. Output saved to: {output_file}")

        else:
            print_usage()

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
