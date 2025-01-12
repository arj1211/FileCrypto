import os
import unittest

from cryptography.exceptions import InvalidTag

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

    def test_wrong_key_decryption(self):
        """Test that decryption with wrong key fails with authentication error"""
        wrong_key = os.urandom(32)  # Generate a different key
        encrypted = self.encryptor.encrypt(self.test_data, self.key)

        # Decrypt with wrong key should raise InvalidTag
        with self.assertRaises(InvalidTag):
            self.encryptor.decrypt(encrypted, wrong_key)

    def test_tampered_data_detection(self):
        """Test that tampered encrypted data is detected"""
        encrypted = self.encryptor.encrypt(self.test_data, self.key)

        # Tamper with the encrypted data
        tampered = bytearray(encrypted)
        # Modify a byte in the ciphertext portion (after nonce and tag)
        tampered[30] = (tampered[30] + 1) % 256

        # Decryption of tampered data should raise InvalidTag
        with self.assertRaises(InvalidTag):
            self.encryptor.decrypt(bytes(tampered), self.key)

    def test_multiple_encryptions_different(self):
        """Test that multiple encryptions of same data produce different results"""
        encrypted1 = self.encryptor.encrypt(self.test_data, self.key)
        encrypted2 = self.encryptor.encrypt(self.test_data, self.key)
        encrypted3 = self.encryptor.encrypt(self.test_data, self.key)

        # Each encryption should be different due to random nonce
        self.assertNotEqual(encrypted1, encrypted2)
        self.assertNotEqual(encrypted2, encrypted3)
        self.assertNotEqual(encrypted1, encrypted3)

        # But they should all decrypt to the same data
        self.assertEqual(self.encryptor.decrypt(encrypted1, self.key), self.test_data)
        self.assertEqual(self.encryptor.decrypt(encrypted2, self.key), self.test_data)
        self.assertEqual(self.encryptor.decrypt(encrypted3, self.key), self.test_data)

    def test_large_data_encryption(self):
        """Test encryption/decryption of larger data"""
        large_data = os.urandom(1024 * 1024)  # 1MB of random data
        encrypted = self.encryptor.encrypt(large_data, self.key)
        decrypted = self.encryptor.decrypt(encrypted, self.key)
        self.assertEqual(large_data, decrypted)
