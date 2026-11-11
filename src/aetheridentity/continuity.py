"""L2 — Continuity (§6.2 of SPECIFICATION.md).

Implements Definition 2 of the paper:
- Continuity chain with pre-committed next keys.
- Rotation requires the next key, kept offline.
- Fork detection: two valid rotations with the same predecessor.

Out of scope (v2.0.0):
- Fork resolution.
- Recovery after total key loss.
- Single-instance enforcement.
"""

from __future__ import annotations

import hashlib
from typing import Iterable

from aetheridentity.records import (
    InceptionRecord,
    RotationRecord,
    canonical_bytes,
)
from aetheridentity.signer import Signer


def hash_key(pk: bytes) -> bytes:
    """Hash a public key for pre-commitment (H(pk))."""
    return hashlib.sha256(pk).digest()


def create_inception(
    signer: Signer,
    label: str,
    next_pk: bytes,
    alg: str = "ed25519",
    created_at: int = 0,
) -> InceptionRecord:
    """Create an inception record that commits to the next key.

    The inception record itself has no `next_pk` field in Definition 1,
    but the commitment is stored as the first rotation's `commitment`
    field when the first rotation is created. To keep the record types
    simple, we store the commitment implicitly: the caller must pass
    `next_pk` when creating the first rotation.
    """
    from aetheridentity.identity import identifier

    pk = signer.public_key()
    signer_id = identifier(alg, pk, label)
    record = InceptionRecord(
        record_type="inception",
        signer_id=signer_id,
        created_at=created_at,
        alg=alg,
        pk=pk,
        label=label,
        t_c=created_at,
    )
    sig = signer.sign(canonical_bytes(record))
    return InceptionRecord(**{**record.__dict__, "signature": sig})


def create_rotation(
    signer: Signer,
    ident: str,
    epoch: int,
    new_pk: bytes,
    next_pk: bytes,
    prev_hash: str,
    created_at: int = 0,
) -> RotationRecord:
    """Create a rotation record that reveals `new_pk` and commits to `next_pk`."""
    commitment = hash_key(next_pk)
    record = RotationRecord(
        record_type="rotation",
        signer_id=ident,
        created_at=created_at,
        id=ident,
        epoch=epoch,
        new_pk=new_pk,
        commitment=commitment,
        prev_hash=prev_hash,
        signing_pk=signer.public_key(),
    )
    sig = signer.sign(canonical_bytes(record))
    return RotationRecord(**{**record.__dict__, "signature": sig})


def verify_rotation(
    rotation: RotationRecord,
    previous_commitment: bytes,
) -> bool:
    """Verify that a rotation reveals the pre-committed key."""
    return hash_key(rotation.new_pk) == previous_commitment


def detect_fork(rotations: Iterable[RotationRecord]) -> bool:
    """A fork is two valid rotations with the same predecessor and different content."""
    seen: dict[str, bytes] = {}
    for r in rotations:
        if r.record_type != "rotation":
            continue
        content = canonical_bytes(r)
        if r.prev_hash in seen:
            if seen[r.prev_hash] != content:
                return True
        else:
            seen[r.prev_hash] = content
    return False


def continuity_chain(
    records: Iterable,
    ident: str,
) -> list[RotationRecord]:
    """Return the continuity chain for `ident`, ordered by epoch."""
    chain = [r for r in records if isinstance(r, RotationRecord) and r.id == ident]
    return sorted(chain, key=lambda r: r.epoch)
