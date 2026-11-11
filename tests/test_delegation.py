"""Tests for L5 — Delegation."""

from aetheridentity.delegation import (
    Scope,
    delegate,
    effective_expiry,
    effective_scope,
    governance_overlap,
    is_revoked,
    is_valid_for_action,
    revoke,
    validate_delegation,
)
from aetheridentity.records import record_hash
from aetheridentity.signer import FakeSigner


def test_delegate_signed():
    """L5: a delegation is signed and well-formed."""
    signer = FakeSigner()
    d = delegate(
        signer,
        delegator="alice",
        delegatee="bob",
        scope=Scope(frozenset({"read"})),
        expiry=100,
        created_at=0,
    )
    assert d.record_type == "delegation"
    assert d.delegator == "alice"
    assert d.delegatee == "bob"
    assert d.signature != b""


def test_validate_root_delegation():
    """L5: a root delegation with non-empty scope and positive expiry is valid."""
    signer = FakeSigner()
    root = delegate(signer, "alice", "bob", Scope(frozenset({"read"})), 100, "", 0)
    assert validate_delegation([root], root) is True


def test_validate_child_delegation():
    """T07: a child delegation with narrower scope and expiry is valid."""
    signer = FakeSigner()
    root = delegate(signer, "alice", "bob", Scope(frozenset({"read", "write"})), 100, "", 0)
    parent_id = record_hash(root)
    child = delegate(signer, "bob", "carol", Scope(frozenset({"read"})), 50, parent_id, 1)
    assert validate_delegation([root, child], child) is True


def test_validate_widening_rejected():
    """T07: a child that widens scope is invalid."""
    signer = FakeSigner()
    root = delegate(signer, "alice", "bob", Scope(frozenset({"read"})), 100, "", 0)
    parent_id = record_hash(root)
    child = delegate(signer, "bob", "carol", Scope(frozenset({"read", "write"})), 50, parent_id, 1)
    assert validate_delegation([root, child], child) is False


def test_validate_longer_expiry_rejected():
    """T07: a child with longer expiry is invalid."""
    signer = FakeSigner()
    root = delegate(signer, "alice", "bob", Scope(frozenset({"read"})), 100, "", 0)
    parent_id = record_hash(root)
    child = delegate(signer, "bob", "carol", Scope(frozenset({"read"})), 200, parent_id, 1)
    assert validate_delegation([root, child], child) is False


def test_effective_scope_intersection():
    """L5: effective scope is the intersection of the chain."""
    signer = FakeSigner()
    root = delegate(signer, "alice", "bob", Scope(frozenset({"read", "write"})), 100, "", 0)
    parent_id = record_hash(root)
    child = delegate(signer, "bob", "carol", Scope(frozenset({"read"})), 50, parent_id, 1)
    eff = effective_scope([root, child], child)
    assert eff.permissions == frozenset({"read"})


def test_effective_expiry_minimum():
    """L5: effective expiry is the minimum of the chain."""
    signer = FakeSigner()
    root = delegate(signer, "alice", "bob", Scope(frozenset({"read"})), 100, "", 0)
    parent_id = record_hash(root)
    child = delegate(signer, "bob", "carol", Scope(frozenset({"read"})), 50, parent_id, 1)
    assert effective_expiry([root, child], child) == 50


def test_is_valid_for_action():
    """T08: an action is valid if inside the effective scope and before expiry."""
    signer = FakeSigner()
    root = delegate(signer, "alice", "bob", Scope(frozenset({"read"})), 100, "", 0)
    assert is_valid_for_action([root], root, action_time=50, required_permission="read") is True
    assert is_valid_for_action([root], root, action_time=150, required_permission="read") is False
    assert is_valid_for_action([root], root, action_time=50, required_permission="write") is False


def test_revocation_propagates():
    """T08: revoking a link invalidates downstream actions."""
    signer = FakeSigner()
    root = delegate(signer, "alice", "bob", Scope(frozenset({"read"})), 100, "", 0)
    parent_id = record_hash(root)
    child = delegate(signer, "bob", "carol", Scope(frozenset({"read"})), 50, parent_id, 1)
    rev = revoke(signer, root, created_at=2)
    records = [root, child, rev]
    assert is_revoked(records, root) is True
    assert is_valid_for_action(records, child, action_time=10, required_permission="read") is False


def test_governance_overlap_zero():
    """F3: no overlap means L5 is distinct from AetherGovern."""
    signer = FakeSigner()
    d = delegate(signer, "alice", "bob", Scope(frozenset({"read"})), 100, "", 0)
    overlap = governance_overlap([d], {"alice": frozenset()})
    assert overlap == 0.0


def test_governance_overlap_full():
    """F3: full overlap means L5 folds into AetherGovern."""
    signer = FakeSigner()
    d = delegate(signer, "alice", "bob", Scope(frozenset({"read"})), 100, "", 0)
    overlap = governance_overlap([d], {"alice": frozenset({"bob"})})
    assert overlap == 1.0
