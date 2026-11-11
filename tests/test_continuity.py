"""Tests for L2 — Continuity."""

from aetheridentity.continuity import (
    continuity_chain,
    create_inception,
    create_rotation,
    detect_fork,
    hash_key,
    verify_rotation,
)
from aetheridentity.identity import identifier
from aetheridentity.signer import FakeSigner
from aetheridentity.simulator import Simulator


def test_inception_record_creation():
    """L2: inception record has the correct identifier."""
    signer = FakeSigner()
    rec = create_inception(signer, label="agent", next_pk=b"next", created_at=0)
    assert rec.record_type == "inception"
    assert rec.signer_id == identifier("ed25519", signer.public_key(), "agent")
    assert rec.signature != b""


def test_rotation_reveals_committed_key():
    """T03: a rotation is valid iff it reveals the pre-committed key."""
    signer = FakeSigner()
    next_pk = b"the-next-key"
    commitment = hash_key(next_pk)
    rotation = create_rotation(
        signer=signer,
        ident="agent-id",
        epoch=1,
        new_pk=next_pk,
        next_pk=b"the-following-key",
        prev_hash="0" * 64,
        created_at=1,
    )
    assert verify_rotation(rotation, commitment) is True

    wrong_commitment = hash_key(b"a-different-key")
    assert verify_rotation(rotation, wrong_commitment) is False


def test_no_fork_with_distinct_predecessors():
    """T04: distinct predecessors do not constitute a fork."""
    signer = FakeSigner()
    r1 = create_rotation(signer, "id", 1, b"k1", b"k2", "a" * 64, 1)
    r2 = create_rotation(signer, "id", 1, b"k3", b"k4", "b" * 64, 2)
    assert detect_fork([r1, r2]) is False


def test_fork_detected_with_same_predecessor():
    """T04: two valid rotations with the same predecessor and different content are a fork."""
    signer = FakeSigner()
    r1 = create_rotation(signer, "id", 1, b"k1", b"k2", "a" * 64, 1)
    r2 = create_rotation(signer, "id", 1, b"k3", b"k4", "a" * 64, 2)
    assert detect_fork([r1, r2]) is True


def test_continuity_chain_ordering():
    """L2: the continuity chain is ordered by epoch."""
    signer = FakeSigner()
    r2 = create_rotation(signer, "id", 2, b"k3", b"k4", "b" * 64, 2)
    r1 = create_rotation(signer, "id", 1, b"k1", b"k2", "a" * 64, 1)
    chain = continuity_chain([r2, r1], "id")
    assert [r.epoch for r in chain] == [1, 2]


def test_rotation_roundtrip_in_simulator():
    """L2: a rotation record can be admitted and read back."""
    signer = FakeSigner()
    sim = Simulator(signer)
    inception = create_inception(signer, label="agent", next_pk=b"k2", created_at=0)
    rotation = create_rotation(
        signer=signer,
        ident=inception.signer_id,
        epoch=1,
        new_pk=b"k2",
        next_pk=b"k3",
        prev_hash="0" * 64,
        created_at=1,
    )
    assert sim.admit(inception) is True
    assert sim.admit(rotation) is True
    assert len(sim) == 2
