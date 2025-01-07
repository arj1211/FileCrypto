import base64
import os
import tempfile
import zipfile
from io import BytesIO

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

    def create_protected_zip(self, encrypted_data, key, password):
        """Create password-protected zip with encrypted data and key"""
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Add encrypted data
            zip_file.writestr("encrypted_data.txt", encrypted_data)

            # Add password-protected key file
            with tempfile.NamedTemporaryFile(delete=False) as temp_key_file:
                temp_key_file.write(key)
                temp_key_file.flush()

                # Add key file with password protection
                zip_file.write(temp_key_file.name, "key.txt", zipfile.ZIP_DEFLATED)
                zip_file.setpassword(password.encode())

            os.unlink(temp_key_file.name)

        return zip_buffer.getvalue()

    def encrypt_file(self, file_path, password):
        """Encrypt file and create protected zip archive"""
        # Encrypt file in chunks
        encrypted_chunks = []
        for base64_chunk in self.file_to_base64(file_path):
            encrypted_chunk = self.encrypt_data(base64_chunk)
            encrypted_chunks.append(encrypted_chunk)

        # Join encrypted chunks
        encrypted_data = b"\n".join(encrypted_chunks)

        # Create password-protected zip
        zip_data = self.create_protected_zip(encrypted_data, self.key, password)

        # Convert final zip to base64
        final_base64 = base64.b64encode(zip_data)

        # Save final base64 string
        output_file = f"{file_path}.encrypted.txt"
        with open(output_file, "wb") as f:
            f.write(final_base64)

        return output_file

    def decrypt_file(self, encrypted_file_path, password, output_path):
        """Decrypt file from encrypted base64 zip archive"""
        # Read base64 encoded zip
        with open(encrypted_file_path, "rb") as f:
            zip_data = base64.b64decode(f.read())

        # Create zip file in memory
        zip_buffer = BytesIO(zip_data)

        # Extract files from zip
        with zipfile.ZipFile(zip_buffer, "r") as zip_file:
            # Extract encrypted data
            encrypted_data = zip_file.read("encrypted_data.txt")

            # Extract key file using password
            try:
                key = zip_file.read("key.txt", pwd=password.encode())
            except RuntimeError:
                raise ValueError("Invalid password")

        # Decrypt data chunks
        decrypted_content = b""
        for line in encrypted_data.split(b"\n"):
            if line.strip():
                # Decrypt chunk
                decrypted_chunk = self.decrypt_data(line.strip(), key)
                # Decode base64
                decoded_chunk = base64.b64decode(decrypted_chunk)
                decrypted_content += decoded_chunk

        # Save decrypted file
        with open(output_path, "wb") as f:
            f.write(decrypted_content)

        return output_path


if __name__ == "__main__":
    import sys

    def print_usage():
        print("Usage:")
        print("To encrypt: python file_crypto.py encrypt <file_path> <password>")
        print(
            "To decrypt: python file_crypto.py decrypt <encrypted_file_path> <password> <output_path>"
        )

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    crypto = FileCrypto()

    try:
        if sys.argv[1] == "encrypt" and len(sys.argv) == 4:
            file_path = sys.argv[2]
            password = sys.argv[3]

            output_file = crypto.encrypt_file(file_path, password)
            print(f"File encrypted successfully. Output saved to: {output_file}")

        elif sys.argv[1] == "decrypt" and len(sys.argv) == 5:
            encrypted_file = sys.argv[2]
            password = sys.argv[3]
            output_path = sys.argv[4]

            output_file = crypto.decrypt_file(encrypted_file, password, output_path)
            print(f"File decrypted successfully. Output saved to: {output_file}")

        else:
            print_usage()

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
