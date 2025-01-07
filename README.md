# FileCrypto

A secure file encryption/decryption utility that uses Fernet symmetric encryption, base64 encoding, and password-protected zip archives to secure files.

## Features

- Symmetric encryption using Fernet (AES-128 in CBC mode)
- Password-protected key storage
- Base64 encoding for universal compatibility
- Chunk-based processing for memory efficiency
- Command-line interface
- All-in-one encryption/decryption class

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

### Command Line Interface

```bash
# Encrypt a file
python file_crypto.py encrypt <file_path> <password>

# Decrypt a file
python file_crypto.py decrypt <encrypted_file_path> <password> <output_path>
```

### Example Usage

```bash
# Encrypt
python file_crypto.py encrypt myfile.txt mypassword123

# Decrypt
python file_crypto.py decrypt myfile.txt.encrypted.txt mypassword123 decrypted_file.txt
```

## How It Works

### Encryption Process Flow

1. **Base64 Encoding**
   - File is read in 64KB chunks
   - Each chunk is converted to base64
   - This ensures binary data can be safely stored as text

2. **Fernet Encryption**
   - A random encryption key is generated
   - Each base64 chunk is encrypted using Fernet
   - Fernet provides secure AES-128 encryption in CBC mode with PKCS7 padding

3. **Zip Archive Creation**
   - Encrypted data is stored in the zip as 'encrypted_data.txt'
   - Encryption key is stored as 'key.txt'
   - Key file is password-protected using the user's password
   - This keeps the key secure while bundling it with the data

4. **Final Base64 Encoding**
   - Entire zip archive is converted to base64
   - Saved as a .txt file with '.encrypted.txt' extension
   - This makes the encrypted file easy to transfer and store

### Decryption Process Flow

1. **Initial Base64 Decoding**
   - Reads the .encrypted.txt file
   - Decodes base64 to get the zip archive

2. **Zip Extraction**
   - Opens the zip archive in memory
   - Extracts encrypted data
   - Uses provided password to extract the key file

3. **Chunk Decryption**
   - Each encrypted chunk is decrypted using the key
   - Base64 is decoded to get original binary data
   - Chunks are combined to recreate the original file

## Security Features

1. **Multi-layer Security**
   - Fernet symmetric encryption (AES-128-CBC)
   - Password-protected zip archive
   - Base64 encoding for safe transfer

2. **Key Management**
   - Encryption key is automatically generated
   - Key is password-protected within the zip
   - Key is bundled with encrypted data for convenience

3. **Chunk Processing**
   - Large files are processed in chunks
   - Prevents memory overflow
   - Maintains performance with large files

## Class Structure

### FileCrypto Class

Main methods:
- `generate_key()`: Creates new Fernet encryption key
- `encrypt_file()`: Main encryption method
- `decrypt_file()`: Main decryption method
- `create_protected_zip()`: Creates password-protected archive
- `file_to_base64()`: Handles chunk-based base64 encoding
- `encrypt_data()`: Handles Fernet encryption
- `decrypt_data()`: Handles Fernet decryption

## Output Files

- Original filename + `.encrypted.txt`: Contains the final encrypted data
- The encrypted file contains:
  - Encrypted file data
  - Encryption key (password-protected)
  - All bundled in a base64-encoded zip archive

## Error Handling

The script includes error handling for:
- Invalid passwords
- Missing files
- Corruption in encrypted data
- Invalid command-line arguments

## Limitations

- Password strength depends on user input
- No built-in password strength validation
- Zip encryption uses legacy ZIP 2.0 encryption
- File paths must be accessible to the script

## Best Practices

1. **Password Security**
   - Use strong, unique passwords
   - Don't share passwords through the same channel as encrypted files
   - Keep passwords secure and documented

2. **File Management**
   - Keep backups of original files
   - Verify successful decryption before deleting originals
   - Use secure channels for transferring encrypted files

3. **Usage**
   - Test encryption/decryption with small files first
   - Verify file integrity after decryption
   - Keep track of passwords used for different files

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.

## Future Improvements

Potential areas for enhancement:
- Password strength validation
- Multiple encryption algorithms support
- Progress indicators for large files
- Batch processing capabilities
- GUI interface
- Modern zip encryption methods