"""L5 — Delegation (§6.5 of SPECIFICATION.md).

Implements Definition 4 of the paper:
- Delegation record: (i, j, S_d, e_d, p_d).
- Validity: S_d ⊆ S_p, e_d ≤ e_p, parent valid.
- Effective scope: intersection. Effective expiry: minimum.
- Revocation of any link invalidates downstream links.

Out of scope (v2.0.0):
- Expressive scopes (open question Q16).
- Retroactive vs. prospective revocation (open question Q17).
- Whether L5 is separable from AetherGovern (tested via governance_overlap).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from aetheridentity.records import DelegationRecord, canonical_bytes
from aetheridentity.signer import Signer


@dataclass(frozen=True)
class Scope:
    """A scope is a set of permissions (strings)."""

    permissions: frozenset[str]

    def is_subset_of(self, other: "Scope") -> bool:
        return self.permissions.issubset(other.permissions)

    def intersect(self, other: "Scope") -> "Scope":
        return Scope(self.permissions & other.permissions)

    def __str__(self) -> str:
        return "|".join(sorted(self.permissions))


def _parse_scope(s: str) -> Scope:
    """Parse a scope string ('p1|p2|...') into a Scope."""
    if not s:
        return Scope(frozenset())
    return Scope(frozenset(s.split("|")))


def delegate(
    signer: Signer,
    delegator: str,
    delegatee: str,
    scope: Scope,
    expiry: int,
    parent: str = "",
    created_at: int = 0,
) -> DelegationRecord:
    """Create and sign a delegation record."""
    record = DelegationRecord(
        record_type="delegation",
        signer_id=delegator,
        created_at=created_at,
        delegator=delegator,
        delegatee=delegatee,
        scope=str(scope),
        expiry=expiry,
        parent=parent,
    )
    sig = signer.sign(canonical_bytes(record))
    return DelegationRecord(**{**record.__dict__, "signature": sig})


def _find_parent(
    records: Iterable[DelegationRecord],
    parent_id: str,
) -> DelegationRecord | None:
    """Find a parent delegation by its signature hash (acting as id)."""
    if not parent_id:
        return None
    for r in records:
        if r.record_type != "delegation":
            continue
        # Use the canonical hash as the delegation's identifier.
        from aetheridentity.records import record_hash

        if record_hash(r) == parent_id:
            return r
    return None


def validate_delegation(
    records: Iterable[DelegationRecord],
    child: DelegationRecord,
) -> bool:
    """A delegation is valid iff:
    - its scope is a subset of the parent's scope,
    - its expiry is ≤ the parent's expiry,
    - the parent is valid (recursively).
    A root delegation (no parent) is valid iff its scope is non-empty and
    its expiry is positive.
    """
    child_scope = _parse_scope(child.scope)

    if not child.parent:
        return len(child_scope.permissions) > 0 and child.expiry > 0

    parent = _find_parent(records, child.parent)
    if parent is None:
        return False

    parent_scope = _parse_scope(parent.scope)
    if not child_scope.is_subset_of(parent_scope):
        return False
    if child.expiry > parent.expiry:
        return False
    return validate_delegation(records, parent)


def effective_scope(
    records: Iterable[DelegationRecord],
    leaf: DelegationRecord,
) -> Scope:
    """The effective scope of a chain is the intersection of its scopes."""
    records = list(records)
    chain = _chain_of(records, leaf)
    result = _parse_scope(chain[0].scope)
    for r in chain[1:]:
        result = result.intersect(_parse_scope(r.scope))
    return result


def effective_expiry(
    records: Iterable[DelegationRecord],
    leaf: DelegationRecord,
) -> int:
    """The effective expiry of a chain is the minimum of its expiries."""
    records = list(records)
    chain = _chain_of(records, leaf)
    return min(r.expiry for r in chain)


def _chain_of(
    records: list[DelegationRecord],
    leaf: DelegationRecord,
) -> list[DelegationRecord]:
    """Return the chain from root to leaf."""
    chain = [leaf]
    current = leaf
    while current.parent:
        parent = _find_parent(records, current.parent)
        if parent is None:
            break
        chain.append(parent)
        current = parent
    return list(reversed(chain))


def revoke(
    signer: Signer,
    target_delegation: DelegationRecord,
    created_at: int = 0,
) -> DelegationRecord:
    """Create and sign a revocation record for a delegation.

    A revocation is represented as a delegation with an empty scope and
    expiry 0, targeting the original delegation via `parent`.
    """
    from aetheridentity.records import record_hash

    target_id = record_hash(target_delegation)
    record = DelegationRecord(
        record_type="delegation",
        signer_id=target_delegation.delegator,
        created_at=created_at,
        delegator=target_delegation.delegator,
        delegatee=target_delegation.delegatee,
        scope="",
        expiry=0,
        parent=target_id,
    )
    sig = signer.sign(canonical_bytes(record))
    return DelegationRecord(**{**record.__dict__, "signature": sig})


def is_revoked(
    records: Iterable[DelegationRecord],
    delegation: DelegationRecord,
) -> bool:
    """A delegation is revoked if any link in its chain has a revocation record."""
    from aetheridentity.records import record_hash

    records = list(records)
    target_id = record_hash(delegation)
    for r in records:
        if r.record_type != "delegation":
            continue
        if r.scope == "" and r.expiry == 0 and r.parent == target_id:
            return True
    return False


def is_valid_for_action(
    records: Iterable[DelegationRecord],
    delegation: DelegationRecord,
    action_time: int,
    required_permission: str,
) -> bool:
    """Check that a delegation authorizes an action.

    - The chain must be valid (validate_delegation).
    - The action_time must be ≤ the effective expiry.
    - The required permission must be in the effective scope.
    - No link in the chain may be revoked.
    """
    records = list(records)
    if not validate_delegation(records, delegation):
        return False
    if action_time > effective_expiry(records, delegation):
        return False
    if required_permission not in effective_scope(records, delegation).permissions:
        return False
    chain = _chain_of(records, delegation)
    for link in chain:
        if is_revoked(records, link):
            return False
    return True


def governance_overlap(
    records: Iterable[DelegationRecord],
    authority_chains: dict[str, frozenset[str]],
) -> float:
    """Measure the fraction of L5 decisions that can be re-expressed as
    AetherGovern decisions (F3, tested in S6).

    For each delegation in `records`, check whether its (delegator, delegatee)
    pair already appears in the `authority_chains` mapping, where
    authority_chains[delegator] is the set of principals authorized to act
    on behalf of `delegator` under AetherGovern.

    Returns:
        Fraction in [0, 1]. 1.0 means every L5 decision is already an
        AetherGovern decision (F3 falsified if ≥ the threshold 0.80).
    """
    records = [r for r in records if r.record_type == "delegation"]
    if not records:
        return 0.0
    overlaps = 0
    for r in records:
        authorized = authority_chains.get(r.delegator, frozenset())
        if r.delegatee in authorized:
            overlaps += 1
    return overlaps / len(records)
