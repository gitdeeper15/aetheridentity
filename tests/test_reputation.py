"""Tests for L3 — Reputation."""

from fractions import Fraction

from aetheridentity.reputation import (
    K,
    DAMPING,
    record_observation,
    reputation_of,
    reputation_residual,
)
from aetheridentity.signer import FakeSigner


def test_record_observation_signature():
    """L3: observation record is signed and well-formed."""
    signer = FakeSigner()
    rec = record_observation(
        signer,
        observer="alice",
        subject="bob",
        evidence="evidence-1",
        outcome=1,
        created_at=0,
    )
    assert rec.record_type == "reputation"
    assert rec.outcome == 1
    assert rec.signature != b""


def test_reputation_determinism():
    """T05: reputation is deterministic for a fixed S."""
    signer = FakeSigner()
    records = [
        record_observation(signer, "alice", "bob", "e1", 1, 1),
        record_observation(signer, "alice", "bob", "e2", 1, 2),
        record_observation(signer, "alice", "carol", "e3", 0, 3),
    ]
    a = reputation_of(records)
    b = reputation_of(records)
    assert a == b


def test_reputation_permutation_invariance():
    """T01: reputation is invariant under permutation of S."""
    signer = FakeSigner()
    records = [
        record_observation(signer, "alice", "bob", "e1", 1, 1),
        record_observation(signer, "alice", "bob", "e2", 1, 2),
        record_observation(signer, "alice", "carol", "e3", 0, 3),
    ]
    a = reputation_of(records)
    b = reputation_of(list(reversed(records)))
    assert a == b


def test_reputation_fixed_point_convergence():
    """T06: the iteration converges within K steps."""
    signer = FakeSigner()
    records = [
        record_observation(signer, "alice", "bob", "e1", 1, 1),
        record_observation(signer, "alice", "bob", "e2", 1, 2),
        record_observation(signer, "alice", "carol", "e3", 0, 3),
    ]
    residual = reputation_residual(records)
    assert residual < Fraction(1, 1_000_000)


def test_reputation_range():
    """L3: reputation values are in [0, 1] and non-negative.

    Note: the vector is not required to sum to 1. The iteration
    t ← (1−a)·Cᵀt + a·p does not preserve the L1 norm unless C is
    doubly stochastic, which is not assumed here.
    """
    signer = FakeSigner()
    records = [
        record_observation(signer, "alice", "bob", "e1", 1, 1),
        record_observation(signer, "alice", "carol", "e2", 1, 2),
    ]
    vec = reputation_of(records)
    for v in vec.values():
        assert 0 <= v <= 1
    # The vector is non-empty and non-negative.
    assert all(v >= 0 for v in vec.values())
    assert len(vec) == 2


def test_reputation_is_fraction():
    """L3: reputation is computed in exact arithmetic (Fraction)."""
    signer = FakeSigner()
    records = [
        record_observation(signer, "alice", "bob", "e1", 1, 1),
    ]
    vec = reputation_of(records)
    for v in vec.values():
        assert isinstance(v, Fraction)
