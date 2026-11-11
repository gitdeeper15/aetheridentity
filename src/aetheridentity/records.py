"""Record types for AetherIdentity.

Implements §3 of SPECIFICATION.md:
- Five record types (InceptionRecord, RotationRecord, ReputationRecord,
  DelegationRecord, SybilClaim).
- Canonical JSON serialization (§3.3).
- Record hashing (SHA-256 over canonical JSON).

No signatures are verified here. Signature verification belongs to signer.py.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Literal

RecordType = Literal["inception", "rotation", "reputation", "delegation", "sybil_claim"]


def _canonical_json(obj: dict[str, Any]) -> bytes:
    """Canonical JSON serialization (§3.3 of SPECIFICATION.md).

    - Keys sorted lexicographically.
    - No whitespace.
    - UTF-8 encoding.
    - Bytes encoded as lowercase hex.
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=_json_default,
    ).encode("utf-8")


def _json_default(obj: Any) -> Any:
    if isinstance(obj, bytes):
        return obj.hex()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def canonical_bytes(record: "BaseRecord") -> bytes:
    """Canonical serialization of a record, without its signature field."""
    data = asdict(record)
    data.pop("signature", None)
    return _canonical_json(data)


def record_hash(record: "BaseRecord") -> str:
    """SHA-256 hash of the canonical serialization (without signature)."""
    return hashlib.sha256(canonical_bytes(record)).hexdigest()


@dataclass(frozen=True)
class BaseRecord:
    """Common fields for all record types (§3.2 of SPECIFICATION.md)."""

    record_type: RecordType
    signer_id: str
    created_at: int
    signature: bytes = field(default=b"", compare=False)


@dataclass(frozen=True)
class InceptionRecord(BaseRecord):
    """Identity creation (Definition 1 of the paper)."""

    alg: str = ""
    pk: bytes = field(default=b"", compare=False)
    label: str = ""
    t_c: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "record_type", "inception")


@dataclass(frozen=True)
class RotationRecord(BaseRecord):
    """Key rotation (Definition 2 of the paper)."""

    id: str = ""
    epoch: int = 0
    new_pk: bytes = field(default=b"", compare=False)
    commitment: bytes = field(default=b"", compare=False)
    prev_hash: str = ""
    signing_pk: bytes = field(default=b"", compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "record_type", "rotation")


@dataclass(frozen=True)
class ReputationRecord(BaseRecord):
    """Signed observation (Definition 3 of the paper)."""

    observer: str = ""
    subject: str = ""
    evidence: str = ""
    outcome: int = 0
    t: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "record_type", "reputation")
        if self.outcome not in (-1, 0, 1):
            raise ValueError("outcome must be -1, 0, or +1")


@dataclass(frozen=True)
class DelegationRecord(BaseRecord):
    """Scoped authority (Definition 4 of the paper)."""

    delegator: str = ""
    delegatee: str = ""
    scope: str = ""
    expiry: int = 0
    parent: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "record_type", "delegation")


@dataclass(frozen=True)
class SybilClaim(BaseRecord):
    """Evidence-backed claim of shared control (§6.4 of SPECIFICATION.md)."""

    attester: str = ""
    target: str = ""
    evidence: str = ""
    t: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "record_type", "sybil_claim")


AnyRecord = InceptionRecord | RotationRecord | ReputationRecord | DelegationRecord | SybilClaim
