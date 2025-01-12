import os
import unittest
from pathlib import Path

from crypto.key_manager import SecureKeyManager


class TestSecureKeyManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_keys")
        self.test_dir.mkdir(exist_ok=True)
        self.key_manager = SecureKeyManager()
        self.key_manager.key_dir = self.test_dir

    def tearDown(self):
        # Clean up test directory
        for file in self.test_dir.glob("*"):
            file.unlink()
        self.test_dir.rmdir()

    def test_key_generation(self):
        """Test that generated keys are of correct length"""
        key = self.key_manager.generate_key()
        self.assertEqual(len(key), 32)  # 256 bits = 32 bytes

    def test_key_storage_retrieval(self):
        """Test that stored keys can be correctly retrieved"""
        key = self.key_manager.generate_key()
        key_path = self.test_dir / "test_key.key"

        # Test binary storage
        self.key_manager.save_key(key, key_path, use_base64=False)
        retrieved_key = self.key_manager.read_key(str(key_path))
        self.assertEqual(key, retrieved_key)

        # Test base64 storage
        self.key_manager.save_key(key, key_path, use_base64=True)
        retrieved_key = self.key_manager.read_key(str(key_path))
        self.assertEqual(key, retrieved_key)

    def test_key_rotation(self):
        """Test that key rotation generates new keys"""
        key1 = self.key_manager.generate_key()
        key2 = self.key_manager.generate_key()
        self.assertNotEqual(key1, key2)

    def test_key_deletion(self):
        """Test that keys can be deleted"""
        key = self.key_manager.generate_key()
        key_path = self.test_dir / "test_key.key"
        self.key_manager.save_key(key, key_path)

        self.assertTrue(key_path.exists())
        key_path.unlink()
        self.assertFalse(key_path.exists())
