"""Smoke tests for Phase 4 core modules."""

from aetheridentity.records import (
    InceptionRecord,
    canonical_bytes,
    record_hash,
)
from aetheridentity.signer import Ed25519Signer, FakeSigner
from aetheridentity.simulator import Simulator
from aetheridentity.identity import create_identity, identifier, verify_identity


def test_canonical_json_is_stable():
    """T24: canonical JSON stability."""
    r = InceptionRecord(
        record_type="inception",
        signer_id="abc",
        created_at=1,
        alg="ed25519",
        pk=b"\x01\x02",
        label="test",
        t_c=1,
    )
    assert canonical_bytes(r) == canonical_bytes(r)


def test_identifier_determinism():
    """T02: identifier determinism (without signer)."""
    pk = b"some-public-key"
    a = identifier("ed25519", pk, "agent")
    b = identifier("ed25519", pk, "agent")
    assert a == b
    assert a != identifier("ed25519", pk, "other")


def test_fake_signer_roundtrip():
    """T11: FakeSigner roundtrip."""
    s = FakeSigner()
    msg = b"hello"
    sig = s.sign(msg)
    assert s.verify(msg, sig, s.public_key())
    assert not s.verify(b"other", sig, s.public_key())


def test_ed25519_signer_roundtrip():
    """T11: Ed25519Signer roundtrip."""
    s = Ed25519Signer()
    msg = b"hello"
    sig = s.sign(msg)
    assert s.verify(msg, sig, s.public_key())
    assert not s.verify(b"other", sig, s.public_key())


def test_signer_separation():
    """T11: FakeSigner and Ed25519Signer are not interchangeable."""
    fake = FakeSigner()
    real = Ed25519Signer()
    msg = b"hello"
    fake_sig = fake.sign(msg)
    real_sig = real.sign(msg)
    assert not real.verify(msg, fake_sig, fake.public_key())
    assert not fake.verify(msg, real_sig, real.public_key())


def test_simulator_admit_and_dedup():
    """Simulator admits a record once, deduplicates on re-admit."""
    signer = FakeSigner()
    sim = Simulator(signer)
    r = InceptionRecord(
        record_type="inception",
        signer_id="abc",
        created_at=1,
        alg="ed25519",
        pk=b"\x01",
        label="test",
        t_c=1,
    )
    assert sim.admit(r) is True
    assert sim.admit(r) is False
    assert len(sim) == 1


def test_identity_roundtrip():
    """L1: create and verify an identity."""
    signer = FakeSigner()
    rec = create_identity(signer, label="agent-1", created_at=0)
    assert verify_identity([rec], rec.signer_id)
    assert not verify_identity([rec], "wrong-id")
