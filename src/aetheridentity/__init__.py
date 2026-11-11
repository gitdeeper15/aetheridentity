"""AetherIdentity v2.0.0 — Reference Implementation.

This package implements the specification in SPECIFICATION.md and the
invariants in INVARIANTS.md. It is a research artifact, not a production
system.

Public API:
    records      — Record types and canonical serialization
    signer       — Abstract Signer, FakeSigner, Ed25519Signer
    simulator    — Replicated state S as a flat list
    identity     — L1 Identity
    continuity   — L2 Continuity
    reputation   — L3 Reputation
    sybil        — L4 Sybil resistance
    delegation   — L5 Delegation
"""

__version__ = "2.0.0"
__paper__ = "10.5281/zenodo.24102739"
__osf__ = "10.17605/OSF.IO/B6AEN"

from aetheridentity import (
    continuity,
    delegation,
    identity,
    records,
    reputation,
    signer,
    simulator,
    sybil,
)

__all__ = [
    "continuity",
    "delegation",
    "identity",
    "records",
    "reputation",
    "signer",
    "simulator",
    "sybil",
]
