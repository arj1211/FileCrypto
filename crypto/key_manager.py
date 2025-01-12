import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


class KeyManager:
    def __init__(self, key_file="key.secure"):
        self.key_file = key_file

    def generate_and_store_key(self):
        key = os.urandom(32)
        master_key = Fernet.generate_key()
        self._save_encrypted_key(key, master_key)
        return key

    def _save_encrypted_key(self, key, master_key):
        f = Fernet(master_key)
        encrypted_key = f.encrypt(key)
        with open(self.key_file, "wb") as key_file:
            key_file.write(encrypted_key)

    def rotate_key(self, current_key):
        return HKDF(
            algorithm=SHA256(), length=32, salt=os.urandom(16), info=b"key rotation"
        ).derive(current_key)
