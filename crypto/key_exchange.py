# crypto/key_exchange.py
import os
from typing import Tuple

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh, ec, padding, rsa
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from crypto.config import SecurityConfig


class SecurityError(Exception):
    pass


class SecureKeyExchange:
    def __init__(self):
        # Generate DH parameters with safe prime
        self.parameters = dh.generate_parameters(
            generator=2, key_size=SecurityConfig.DH_KEY_SIZE
        )
        self._validate_dh_parameters()

        self.private_key = self.parameters.generate_private_key()
        self.public_key = self.private_key.public_key()

        # Generate signing key pair
        self.signing_key = ec.generate_private_key(ec.SECP384R1())

    def _validate_dh_parameters(self):
        # Basic validation of DH parameters
        params = self.parameters.parameter_numbers()

        # Validate generator
        if params.g != 2:
            raise SecurityError("Invalid generator")

        # Validate key size
        if params.p.bit_length() != SecurityConfig.DH_KEY_SIZE:
            raise SecurityError("Invalid key size")

    def get_public_bytes(self) -> bytes:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def perform_key_exchange(
        self,
        peer_public_key_bytes: bytes,
        peer_signature: bytes,
        peer_signing_key: ec.EllipticCurvePublicKey,
    ) -> bytes:
        try:
            # Verify the signature
            peer_signing_key.verify(
                peer_signature, peer_public_key_bytes, ec.ECDSA(hashes.SHA384())
            )

            # Deserialize and validate peer's public key
            peer_public_key = serialization.load_pem_public_key(peer_public_key_bytes)

            # Perform the exchange
            shared_key = self.private_key.exchange(peer_public_key)

            # Derive final key using HKDF
            return HKDF(
                algorithm=SecurityConfig.HASH_ALGORITHM(),
                length=SecurityConfig.AES_KEY_SIZE,
                salt=os.urandom(SecurityConfig.HASH_ALGORITHM.digest_size),
                info=b"shared_key_v1",
            ).derive(shared_key)

        except Exception as e:
            raise SecurityError(f"Key exchange failed: {str(e)}")

    def sign_key(self, public_key_bytes: bytes) -> bytes:
        return self.signing_key.sign(
            public_key_bytes, ec.ECDSA(SecurityConfig.HASH_ALGORITHM())
        )
