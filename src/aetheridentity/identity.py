"""L1 — Identity (§6.1 of SPECIFICATION.md)."""

from __future__ import annotations

import hashlib
from typing import Iterable

from aetheridentity.records import InceptionRecord, canonical_bytes
from aetheridentity.signer import Signer

DOMAIN_TAG = b"AETHERIDENTITY/v2"


def identifier(alg: str, pk: bytes, label: str) -> str:
    """Definition 1: id(t) = H(tag ‖ alg ‖ pk ‖ λ)."""
    h = hashlib.sha256()
    h.update(DOMAIN_TAG)
    h.update(b"\x00")
    h.update(alg.encode("utf-8"))
    h.update(b"\x00")
    h.update(pk)
    h.update(b"\x00")
    h.update(label.encode("utf-8"))
    return h.hexdigest()


def create_identity(signer: Signer, label: str, alg: str = "ed25519", created_at: int = 0) -> InceptionRecord:
    """Create an inception record and sign it."""
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
    return InceptionRecord(
        **{**record.__dict__, "signature": sig}
    )


def verify_identity(records: Iterable[InceptionRecord], ident: str) -> bool:
    """Check that the identifier recomputes from the record's fields."""
    for r in records:
        if r.record_type != "inception":
            continue
        if identifier(r.alg, r.pk, r.label) == ident:
            return True
    return False
