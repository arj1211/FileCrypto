import os
import unittest

from crypto.encryptor import SecureEncryptor


class TestSecureEncryptor(unittest.TestCase):
    def setUp(self):
        self.encryptor = SecureEncryptor()
        self.test_data = b"Hello, World!"
        self.key = os.urandom(32)  # 256-bit key

    def test_encryption_decryption(self):
        """Test that encryption followed by decryption returns original data"""
        encrypted = self.encryptor.encrypt(self.test_data, self.key)
        decrypted = self.encryptor.decrypt(encrypted, self.key)
        self.assertEqual(self.test_data, decrypted)

    def test_different_keys(self):
        """Test that different keys produce different ciphertexts"""
        key2 = os.urandom(32)
        encrypted1 = self.encryptor.encrypt(self.test_data, self.key)
        encrypted2 = self.encryptor.encrypt(self.test_data, key2)
        self.assertNotEqual(encrypted1, encrypted2)

    def test_invalid_key_length(self):
        """Test that invalid key lengths raise appropriate errors"""
        invalid_key = os.urandom(20)  # 160-bit key (invalid for AES)
        with self.assertRaises(ValueError):
            self.encryptor.encrypt(self.test_data, invalid_key)

    def test_different_data(self):
        """Test that different data produces different ciphertexts"""
        data2 = b"Different data"
        encrypted1 = self.encryptor.encrypt(self.test_data, self.key)
        encrypted2 = self.encryptor.encrypt(data2, self.key)
        self.assertNotEqual(encrypted1, encrypted2)
