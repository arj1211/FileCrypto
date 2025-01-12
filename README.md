# FileCrypto

> ⚠️ **WARNING**: This is an educational project and contains known security vulnerabilities. 
> Not suitable for production use or protecting sensitive data. See "Security Considerations" 
> section for details.

A file encryption/decryption utility that implements AES-256 encryption in CBC mode with key management and file processing capabilities.

## Features

- AES-256 encryption in CBC mode
- Basic key generation and management
- PKCS7 padding for block alignment
- Random IV generation for each encryption
- File structure preservation
- Command-line interface
- Modular architecture with separate components for:
  - Key Management
  - Encryption/Decryption
  - Key Exchange
  - Metadata Management

## Security Considerations

### Current Security Vulnerabilities

This implementation has several known security vulnerabilities that users should be aware of:

[Rest of security considerations section as previously written...]

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
   - Manages key rotation and deletion
   - Provides secure key retrieval

3. **SecureEncryptor**
   - Implements AES-256 encryption in CBC mode
   - Handles PKCS7 padding
   - Manages IV generation and storage

4. **MetadataManager**
   - Handles file metadata preservation
   - Manages metadata storage and retrieval

### Security Features

1. **Strong Encryption**
   - AES-256 encryption in CBC mode
   - Random IV for each encryption operation
   - PKCS7 padding for proper block alignment

2. **Key Management**
   - Secure key generation using system entropy
   - Protected key storage
   - Key rotation capabilities
   - Separate storage path for keys

3. **Process Security**
   - Chunk-based file processing
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
   - Random IV generation
   - AES-256-CBC encryption
   - PKCS7 padding application
   - IV prepended to encrypted data

3. **File Handling**
   - Original file read in binary mode
   - Encrypted data written to output file
   - Automatic extension management

### Decryption Process

1. **Key Retrieval**
   - Secure key loading from storage
   - Key validation

2. **Decryption**
   - IV extraction from encrypted data
   - AES-256-CBC decryption
   - PKCS7 padding removal
   - Original data restoration

## Error Handling

The system includes comprehensive error handling for:
- Missing input files
- Invalid keys
- Corruption in encrypted data
- Invalid file permissions
- Missing key files
- Decryption failures

## Security Considerations

1. **Key Storage**
   - Keys stored in dedicated directory
   - Separate from encrypted files
   - Protected access permissions

2. **Encryption Strength**
   - AES-256 encryption
   - Random IV generation
   - PKCS7 padding
   - CBC mode operation

3. **Implementation Security**
   - Clean error messages
   - Secure file handling
   - Protected key management

## Future Improvements

1. **Security Enhancements**
   - Key derivation function implementation
   - Digital signature support
   - Integrity verification
   - Secure memory handling

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


## Security Considerations

### Current Security Vulnerabilities

This implementation has several known security vulnerabilities that users should be aware of:

#### Memory Handling
- The entire file content is loaded into memory during encryption/decryption
- No secure memory wiping is implemented
- Sensitive data (keys, plaintext) remains in memory until garbage collection occurs
- Vulnerable to memory dumps that could expose keys and plaintext data

#### Key Management Issues
- Keys are stored directly on the filesystem without additional protection
- No key derivation function (KDF) implementation
- Missing salt usage in cryptographic operations
- Single key reuse across all operations
- No key rotation mechanism
- Keys could be exposed through filesystem access

#### File Operation Risks
- No secure handling of temporary files
- Potential data remnants left in temporary storage
- Missing cleanup procedures for intermediate files
- File operations are not atomic, leading to potential partial writes

#### Error Handling Weaknesses
- Detailed error messages could leak information about the cryptographic operations
- Stack traces might expose internal implementation details
- Non-uniform error handling could enable timing attacks

#### Input Validation Gaps
- Limited validation of input file paths
- No maximum file size limits
- Missing content type validation
- Path traversal vulnerabilities possible

#### Missing Security Features
- No message authentication (MAC)
- No digital signatures
- Missing integrity checks
- No verification of encrypted data

#### Operational Security Gaps
- No logging of cryptographic operations
- Missing audit trail
- No version control for encrypted files
- Absent access control mechanisms

### Important Notice

This implementation is currently **NOT SUITABLE FOR PRODUCTION USE** or for protecting sensitive data. It is a basic implementation that serves educational purposes but requires significant security improvements before being used in any production environment.

### Recommended Uses

- Educational purposes only
- Learning about cryptographic implementations
- Understanding security considerations in cryptographic software
- Testing and development environments (with non-sensitive data)

### Do Not Use For

- Storing sensitive personal information
- Protecting production data
- Commercial applications
- Any situation requiring genuine security guarantees

### Future Improvements Needed

A production-ready version would need to implement:
1. Secure memory handling and wiping
2. Proper key derivation and management
3. Authenticated encryption
4. Secure temporary file handling
5. Comprehensive input validation
6. Proper error handling
7. Audit logging
8. Access controls


## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for improvements.

## License

This project is licensed under the MIT License.

## Disclaimer

While this implementation uses strong cryptographic primitives, it's recommended to review the security requirements for your specific use case. Always keep secure backups of important files before encryption.