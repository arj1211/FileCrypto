# tests/test_file_processor.py
import os
import unittest
from pathlib import Path

from crypto.file_processor import SecureFileProcessor


class TestSecureFileProcessor(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_files")
        self.test_dir.mkdir(exist_ok=True)

        # Create test file
        self.test_file = self.test_dir / "test.txt"
        with open(self.test_file, "w") as f:
            f.write("Test content for encryption")

        # Initialize processor with test key directory
        self.test_key_dir = self.test_dir / "test_keys"
        self.test_key_dir.mkdir(exist_ok=True)
        self.processor = SecureFileProcessor(str(self.test_key_dir))

    def tearDown(self):
        # Clean up test files and directories
        if self.test_dir.exists():
            for file in self.test_dir.glob("*"):
                if file.is_file():
                    file.unlink()
            for subdir in self.test_dir.glob("*"):
                if subdir.is_dir():
                    for f in subdir.glob("*"):
                        f.unlink()
                    subdir.rmdir()
            self.test_dir.rmdir()

    def test_encrypt_decrypt_cycle(self):
        """Test full encryption and decryption cycle"""
        # Define file paths
        encrypted_file = self.test_dir / "test.txt.encrypted"
        decrypted_file = self.test_dir / "decrypted.txt"

        # Encrypt the file
        self.processor.encrypt_file(str(self.test_file), str(encrypted_file))
        self.assertTrue(encrypted_file.exists())

        # Decrypt the file
        self.processor.decrypt_file(str(encrypted_file), str(decrypted_file))
        self.assertTrue(decrypted_file.exists())

        # Compare original and decrypted content
        with open(self.test_file, "rb") as f1, open(decrypted_file, "rb") as f2:
            self.assertEqual(f1.read(), f2.read())

    def test_invalid_file_handling(self):
        """Test handling of non-existent files"""
        with self.assertRaises(FileNotFoundError):
            self.processor.encrypt_file("nonexistent.txt")

    def test_corrupted_file_handling(self):
        """Test handling of corrupted encrypted files"""
        # Create a corrupted encrypted file
        corrupted_file = self.test_dir / "corrupted.encrypted"
        with open(corrupted_file, "wb") as f:
            f.write(b"This is not a valid encrypted file")

        decrypted_file = self.test_dir / "decrypted.txt"
        with self.assertRaises(ValueError):
            self.processor.decrypt_file(str(corrupted_file), str(decrypted_file))
