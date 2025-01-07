# File Encryptor

A Python script that encrypts files using Fernet symmetric encryption with base64 encoding, processing files in chunks to handle large files efficiently.

## Features

- Symmetric encryption using Fernet (AES-128 in CBC mode)
- Base64 encoding of file contents
- Chunk-based processing for memory efficiency
- Automatic key generation and storage

## Requirements

- Python 3.8+
- cryptography package

## Installation

1. Clone this repository or download the script
2. Install the required dependency:
```bash
pip install cryptography
```

## Usage

1. Place the script `base64_fernet_encrypt.py` in your desired directory
2. Run the script:
```bash
python base64_fernet_encrypt.py
```

The script will:
1. Generate a secure encryption key
2. Encrypt your file in chunks
3. Save the encrypted data to `encrypted_file.txt`
4. Save the encryption key to `encryption_key.txt`

## How It Works

The script operates in several steps:

1. **Base64 Encoding (`file_to_base64` function)**:
   - Reads the input file in chunks of 64KB
   - Converts each chunk to base64 encoding
   - Yields the encoded chunks for processing

2. **Encryption (`encrypt_data` function)**:
   - Uses Fernet symmetric encryption
   - Takes base64-encoded data and an encryption key
   - Returns the encrypted data

3. **File Saving (`save_to_file` function)**:
   - Handles writing data to files
   - Used for both encrypted data and key storage

4. **Main Process**:
   - Generates a random encryption key
   - Reads the input file in chunks
   - Encrypts each chunk
   - Saves encrypted data and key to separate files

## Security Note

The encryption key is saved in plaintext. In a production environment, you should:
- Never commit the encryption key to version control
- Use secure methods to transfer the key to recipients
- Consider using environment variables or secure key storage solutions

## Output Files

- `encrypted_file.txt`: Contains the encrypted data
- `encryption_key.txt`: Contains the encryption key

## Example

```python
# Example of how to modify the input file path
file_path = "your_file.txt"  # Change this to your target file
```

## Limitations

- The encryption key must be kept secure
- The script currently hardcodes output filenames
- No built-in decryption functionality (can be added as needed)

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.
