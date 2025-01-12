from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh, padding, rsa
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


class KeyExchange:
    def __init__(self):
        self.parameters = dh.generate_parameters(generator=2, key_size=2048)
        self.private_key = self.parameters.generate_private_key()
        self.public_key = self.private_key.public_key()

    def perform_key_exchange(self, peer_public_key_bytes):
        # Deserialize the peer's public key
        peer_public_key = serialization.load_pem_public_key(peer_public_key_bytes)

        # Generate the shared key
        shared_key = self.private_key.exchange(peer_public_key)
        return HKDF(
            algorithm=SHA256(), length=32, salt=None, info=b"shared_key"
        ).derive(shared_key)

    def sign_key(self, public_key_bytes, private_signing_key):
        return private_signing_key.sign(
            public_key_bytes,
            padding.PSS(mgf=padding.MGF1(SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            SHA256(),
        )
