# FileCrypto

A secure file encryption/decryption utility that uses Fernet symmetric encryption, AES-256 encrypted zip archives, base64 encoding, and password protection to secure files while preserving original file metadata.

## Features

- Dual-layer encryption:
  - Fernet symmetric encryption (AES-128 in CBC mode) for file content
  - AES-256 encrypted zip archive for the entire package
- Secure password-protected key storage
- Preservation of original filename and extension
- Metadata preservation within encrypted file
- Base64 encoding for universal compatibility 
- Chunk-based processing for memory efficiency
- Command-line interface
- All-in-one encryption/decryption class

## Requirements

- Python 3.8+
- cryptography package
- pyzipper package

## Installation

1. Clone this repository or download the script
2. Install required dependencies:
```bash
pip install cryptography pyzipper
```

## Usage

### Command Line Interface

```bash
# Encrypt a file (creates encrypted.txt by default)
python file_crypto.py encrypt <file_path> <password> [encrypted_file_name]

# Decrypt a file (restores original filename)
python file_crypto.py decrypt encrypted.txt <password> [output_directory]
```

### Example Usage

```bash
# Encrypt myfile.docx
python file_crypto.py encrypt myfile.docx mypassword123

# Encrypt with custom output name
python file_crypto.py encrypt myfile.docx mypassword123 custom_name.txt

# Decrypt back to myfile.docx in current directory
python file_crypto.py decrypt encrypted.txt mypassword123

# Decrypt to specific directory
python file_crypto.py decrypt encrypted.txt mypassword123 /path/to/output
```

## How It Works

### Encryption Process Flow

1. **Metadata Collection**
   - Original filename is captured
   - File extension is preserved
   - Metadata is stored in JSON format

2. **Base64 Encoding**
   - File is read in 64KB chunks
   - Each chunk is converted to base64
   - Ensures binary data can be safely stored as text

3. **Fernet Encryption**
   - Random encryption key is generated
   - Each base64 chunk is encrypted using Fernet
   - Provides AES-128 encryption in CBC mode with PKCS7 padding

4. **AES-256 Encrypted Zip Creation**
   - Encrypted data stored as 'encrypted_data.txt'
   - Metadata stored as 'metadata.json'
   - Encryption key stored as 'key.txt'
   - Entire zip is encrypted using AES-256
   - Password required for access to any file within zip

5. **Final Base64 Encoding**
   - Entire encrypted zip archive is converted to base64
   - Saved as 'encrypted.txt' (or custom name)
   - Original filename is not exposed in encrypted file

### Decryption Process Flow

1. **Initial Base64 Decoding**
   - Reads the encrypted.txt file
   - Decodes base64 to get the encrypted zip archive

2. **AES-256 Zip Extraction**
   - Opens the encrypted zip archive
   - Requires correct password for access
   - Extracts encrypted data, metadata, and key
   - Failed password attempts are rejected

3. **Chunk Decryption**
   - Each encrypted chunk is decrypted using the key
   - Base64 is decoded to get original binary data
   - Chunks are combined to recreate original file

4. **File Restoration**
   - Uses stored metadata to recreate original filename
   - Saves file with original name and extension
   - Optionally saves to specified output directory

## Security Features

1. **Multi-layer Security**
   - Fernet symmetric encryption (AES-128-CBC) for content
   - AES-256 encryption for zip archive
   - Password-protected archive access
   - Base64 encoding for safe transfer
   - Original filename hidden in encrypted file

2. **Key Management**
   - Encryption key is automatically generated
   - Key is stored within AES-256 encrypted zip
   - Wrong passwords fail completely and securely

3. **Metadata Protection**
   - File metadata stored inside encrypted archive
   - Original filename not exposed in encrypted file name
   - All sensitive information is protected

## Class Structure

### FileCrypto Class

Main methods:
- `generate_key()`: Creates new Fernet encryption key
- `encrypt_file()`: Main encryption method with metadata handling
- `decrypt_file()`: Main decryption method with metadata restoration
- `create_protected_zip()`: Creates AES-256 encrypted archive with metadata
- `file_to_base64()`: Handles chunk-based base64 encoding
- `encrypt_data()`: Handles Fernet encryption
- `decrypt_data()`: Handles Fernet decryption

## Output Files

### Encryption Output
- `encrypted.txt` (or custom name): Contains:
  - Encrypted file data
  - Original file metadata
  - Encryption key
  - All within AES-256 encrypted zip archive
  - Final archive encoded in base64

### Decryption Output
- Restores file with original name and extension
- Optional output directory specification
- Preserves original file structure

## Error Handling

The script includes error handling for:
- Invalid passwords (fails securely)
- Missing files
- Corruption in encrypted data
- Invalid command-line arguments
- Invalid output directories
- Failed decryption attempts

## Limitations

- Password strength depends on user input
- No built-in password strength validation
- File paths must be accessible to the script

## Best Practices

1. **Password Security**
   - Use strong, unique passwords
   - Don't share passwords through same channel as encrypted files
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
- Additional metadata support (creation date, permissions, etc.)
- Compression options for different file types