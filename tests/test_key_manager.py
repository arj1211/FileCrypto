# tests/test_key_manager.py
import os
import unittest
from pathlib import Path

from crypto.config import SecurityConfig
from crypto.key_manager import SecureKeyManager


class TestSecureKeyManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_keys")
        self.key_manager = SecureKeyManager(str(self.test_dir))

    def tearDown(self):
        # Clean up test directory after each test
        if self.test_dir.exists():
            for file in self.test_dir.iterdir():
                file.unlink()
            self.test_dir.rmdir()

    def test_key_generation(self):
        """Test that generated keys are of correct length"""
        key = self.key_manager.generate_key()
        self.assertEqual(len(key), SecurityConfig.AES_KEY_SIZE)

    def test_key_storage_retrieval(self):
        """Test that stored keys can be correctly retrieved"""
        original_key = self.key_manager.generate_key()
        retrieved_key = self.key_manager.get_key()
        self.assertEqual(original_key, retrieved_key)

    def test_key_rotation(self):
        """Test that key rotation generates new keys"""
        original_key = self.key_manager.generate_key()
        rotated_key = self.key_manager.rotate_key()
        self.assertNotEqual(original_key, rotated_key)

    def test_key_deletion(self):
        """Test that keys can be deleted"""
        self.key_manager.generate_key()
        self.key_manager.delete_key()
        with self.assertRaises(ValueError):
            self.key_manager.get_key()
