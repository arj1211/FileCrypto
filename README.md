# FileCrypto

> ⚠️ **WARNING**: This is an educational project and contains known security vulnerabilities. 
> Not suitable for production use or protecting sensitive data. See "Security Considerations" 
> section for details.

A file encryption/decryption utility that implements AES-256-GCM encryption with authenticated encryption, key management, and file processing capabilities.

## Features

- AES-256-GCM authenticated encryption
- Secure key generation and management
- Built-in tampering detection
- Automatic nonce generation for each encryption
- Authentication tag verification
- File structure preservation
- Command-line interface
- Modular architecture with separate components for:
  - Key Management
  - Encryption/Decryption
  - File Processing
  - Metadata Management

## Security Features

- Uses AES-256-GCM (Galois/Counter Mode) for authenticated encryption
- Automatic authentication tag verification during decryption 
- Unique nonce (number used once) for each encryption
- Immediate detection and rejection of:
  - Tampered data
  - Incorrect decryption keys
  - Invalid key sizes
- No padding oracle vulnerabilities (GCM mode)

## Requirements

- Python 3.8+
- cryptography package

## Installation

1. Clone this repository
2. Install required dependencies:
```bash
pip install cryptography
```

## Usage

### Command Line Interface

```bash
# Encrypt a file (creates .encrypted extension by default)
python main.py encrypt <input_file> [--output output_file]

# Decrypt a file (removes .encrypted extension by default)
python main.py decrypt <encrypted_file> [--output output_file]
```

### Example Usage

```bash
# Encrypt a file
python main.py encrypt document.pdf

# Encrypt with custom output path
python main.py encrypt document.pdf -o secure_doc.encrypted

# Decrypt a file
python main.py decrypt document.pdf.encrypted

# Decrypt with custom output path
python main.py decrypt document.pdf.encrypted -o restored_doc.pdf
```

## Architecture

### Component Structure

1. **SecureFileProcessor**
   - Main class coordinating encryption/decryption operations
   - Handles file I/O and process management

2. **SecureKeyManager**
   - Generates and stores encryption keys
   - Manages secure key storage
   - Provides secure key retrieval

3. **SecureEncryptor**
   - Implements AES-256-GCM encryption
   - Handles nonce generation and authentication
   - Manages tag generation and verification

4. **MetadataManager**
   - Handles file metadata preservation
   - Manages metadata storage and retrieval

### Security Features

1. **Strong Encryption**
   - AES-256 encryption in GCM mode
   - Random nonce for each encryption operation
   - Authenticated encryption with built-in integrity checking
   - No padding required (GCM mode)

2. **Key Management**
   - Secure key generation using system entropy
   - Protected key storage
   - Separate storage path for keys

3. **Process Security**
   - Chunk-based file processing
   - Automatic tampering detection
   - Secure error handling
   - Clean exception management

## Directory Structure

```
project_root/
├── crypto/
│   ├── __init__.py
│   ├── config.py
│   ├── encryptor.py
│   ├── key_manager.py
│   ├── key_exchange.py
│   └── metadata_manager.py
├── keys/
│   └── encryption_key.key
├── tests/
└── main.py
```

## Implementation Details

### Encryption Process

1. **Key Generation**
   - Secure random key generation
   - Key storage in protected directory

2. **Encryption**
   - Random nonce generation
   - AES-256-GCM encryption
   - Authentication tag generation
   - Nonce and tag prepended to encrypted data

3. **File Handling**
   - Original file read in binary mode
   - Encrypted data written to output file
   - Automatic extension management

### Decryption Process

1. **Key Retrieval**
   - Secure key loading from storage
   - Key validation

2. **Decryption**
   - Nonce and tag extraction from encrypted data
   - Authentication tag verification
   - AES-256-GCM decryption
   - Original data restoration

## Error Handling

The system includes comprehensive error handling for:
- Missing input files
- Invalid keys
- Corruption in encrypted data
- Invalid file permissions
- Missing key files
- Decryption failures
- Tampering detection
- Authentication failures

### Error Categories

1. **Cryptographic Errors**
   - Invalid key size
   - Failed authentication
   - Corrupted data detection
   - Nonce verification failures

2. **File Operation Errors**
   - File access permissions
   - Missing files
   - Invalid file paths
   - I/O errors

3. **Key Management Errors**
   - Key loading failures
   - Invalid key format
   - Key storage errors
   - Key rotation failures


## Security Considerations

### Current Security Features

This implementation includes several security improvements:

#### Cryptographic Strength
- Uses AES-256-GCM authenticated encryption
- Automatic tampering detection
- Unique nonce for each encryption operation
- Built-in integrity verification through authentication tags
- No padding vulnerabilities (GCM mode)

#### Error Handling
- Immediate detection of tampered data
- Secure rejection of incorrect keys
- Validation of key sizes
- Clear error boundaries for security-related failures

However, users should still be aware of remaining considerations:

#### Memory Handling
- The entire file content is loaded into memory during encryption/decryption
- No secure memory wiping is implemented
- Sensitive data (keys, plaintext) remains in memory until garbage collection occurs
- Vulnerable to memory dumps that could expose keys and plaintext data

#### File Operation Risks
- No secure handling of temporary files
- Potential data remnants left in temporary storage
- Missing cleanup procedures for intermediate files
- File operations are not atomic, leading to potential partial writes

## Future Improvements

1. **Security Enhancements**
   - Secure memory handling and wiping
   - Key derivation function implementation
   - Digital signature support
   - Atomic file operations

2. **Feature Additions**
   - Multi-file processing
   - Directory encryption
   - Progress indicators
   - GUI interface
   - Compression support

3. **Operational Improvements**
   - Logging system
   - Configuration management
   - Performance optimizations
   - Batch processing

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for improvements.

When contributing, please:
- Follow existing code style
- Add tests for new features
- Update documentation as needed
- Maintain security best practices
- Document any security considerations

## License

This project is licensed under the MIT License.

## Disclaimer

While this implementation uses strong cryptographic primitives and includes security features like authenticated encryption, users should review the security requirements for their specific use case. Always keep secure backups of important files before encryption.