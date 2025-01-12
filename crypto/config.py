# crypto/config.py
from cryptography.hazmat.primitives import hashes


class SecurityConfig:
    # Key sizes
    AES_KEY_SIZE = 32  # 256 bits
    DH_KEY_SIZE = 2048  # bits

    # Block size for AES
    BLOCK_SIZE = 128  # bits

    # Hash algorithm for key derivation
    HASH_ALGORITHM = hashes.SHA256
