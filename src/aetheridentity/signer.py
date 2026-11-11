"""Abstract Signer interface (§4 of SPECIFICATION.md).

Two implementations:
- FakeSigner: for unit tests and scenarios. Not cryptographic.
- Ed25519Signer: real Ed25519 via the `cryptography` library.

A signature produced by one is not accepted by the other.
"""

from __future__ import annotations

from typing import Protocol

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)


class Signer(Protocol):
    """Abstract signer interface."""

    def sign(self, message: bytes) -> bytes: ...
    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool: ...
    def public_key(self) -> bytes: ...


class FakeSigner:
    """Non-cryptographic signer for tests.

    The signature is the SHA-256 of the message prefixed with a fixed tag.
    This is NOT secure and MUST NOT be used outside tests.
    """

    TAG = b"FAKE-SIGNER:"

    def __init__(self) -> None:
        self._pk = b"fake-pk"

    def sign(self, message: bytes) -> bytes:
        import hashlib

        return self.TAG + hashlib.sha256(message).digest()

    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        if not signature.startswith(self.TAG):
            return False
        return self.sign(message) == signature

    def public_key(self) -> bytes:
        return self._pk


class Ed25519Signer:
    """Real Ed25519 signer using the `cryptography` library."""

    def __init__(self) -> None:
        self._sk = Ed25519PrivateKey.generate()
        self._pk = self._sk.public_key()

    def sign(self, message: bytes) -> bytes:
        return self._sk.sign(message)

    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        try:
            pub = Ed25519PublicKey.from_public_bytes(public_key)
            pub.verify(signature, message)
            return True
        except (InvalidSignature, ValueError):
            return False

    def public_key(self) -> bytes:
        return self._pk.public_bytes(Encoding.Raw, PublicFormat.Raw)
