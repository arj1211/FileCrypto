# tests/test_encryptor.py
import os
import unittest

from crypto.config import SecurityConfig
from crypto.encryptor import SecureEncryptor


class TestSecureEncryptor(unittest.TestCase):
    def setUp(self):
        self.encryptor = SecureEncryptor()
        self.test_key = os.urandom(SecurityConfig.AES_KEY_SIZE)

    def test_encryption_decryption(self):
        """Test that encryption followed by decryption returns original data"""
        original_data = b"Hello, this is a test message!"
        encrypted_data = self.encryptor.encrypt(original_data, self.test_key)
        decrypted_data = self.encryptor.decrypt(encrypted_data, self.test_key)
        self.assertEqual(original_data, decrypted_data)

    def test_different_ivs(self):
        """Test that multiple encryptions of the same data produce different results"""
        data = b"Same data"
        encrypted1 = self.encryptor.encrypt(data, self.test_key)
        encrypted2 = self.encryptor.encrypt(data, self.test_key)
        self.assertNotEqual(encrypted1, encrypted2)

    def test_invalid_key_length(self):
        """Test that invalid key lengths raise appropriate errors"""
        invalid_key = os.urandom(16)  # Too short
        with self.assertRaises(ValueError):
            self.encryptor.encrypt(b"test", invalid_key)
