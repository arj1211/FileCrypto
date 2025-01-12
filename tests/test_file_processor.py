import base64
import os
import unittest
from pathlib import Path

from crypto.file_processor import FileProcessor


class TestFileProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = FileProcessor()
        self.test_dir = Path("test_files")
        self.test_dir.mkdir(exist_ok=True)
        self.test_file = self.test_dir / "test.txt"
        self.test_data = b"Hello, World!"

    def tearDown(self):
        # Clean up test files
        if self.test_file.exists():
            self.test_file.unlink()
        self.test_dir.rmdir()

    def test_binary_write_read(self):
        """Test binary file writing and reading"""
        self.processor.write_file(self.test_file, self.test_data, use_base64=False)
        read_data = self.processor.read_file(self.test_file)
        self.assertEqual(read_data, self.test_data)

    def test_base64_write_read(self):
        """Test base64 file writing and reading"""
        self.processor.write_file(self.test_file, self.test_data, use_base64=True)
        read_data = self.processor.read_file(self.test_file)
        self.assertEqual(read_data, self.test_data)
