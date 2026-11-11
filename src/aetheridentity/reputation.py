"""L3 — Reputation (§6.3 of SPECIFICATION.md).

Implements Definition 3 of the paper:
- Reputation record: signed observation.
- Score: fixed point of an EigenTrust-style iteration, computed in exact
  arithmetic with a fixed iteration count K and a canonical ordering.
- The score is a view over S, not a stored value.

Out of scope (v2.0.0):
- Whether reputation may influence admission (policy decision).
- Per-task-class reputation (open question Q10).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable

from aetheridentity.records import (
    ReputationRecord,
    canonical_bytes,
)
from aetheridentity.signer import Signer

K = 100
DAMPING = Fraction(1, 5)  # a = 0.2


def record_observation(
    signer: Signer,
    observer: str,
    subject: str,
    evidence: str,
    outcome: int,
    created_at: int = 0,
) -> ReputationRecord:
    """Create and sign a reputation record."""
    if outcome not in (-1, 0, 1):
        raise ValueError("outcome must be -1, 0, or +1")
    record = ReputationRecord(
        record_type="reputation",
        signer_id=observer,
        created_at=created_at,
        observer=observer,
        subject=subject,
        evidence=evidence,
        outcome=outcome,
        t=created_at,
    )
    sig = signer.sign(canonical_bytes(record))
    return ReputationRecord(**{**record.__dict__, "signature": sig})


def _build_local_trust(
    records: Iterable[ReputationRecord],
    observers: list[str],
    subjects: list[str],
) -> list[list[Fraction]]:
    """Build the row-stochastic matrix C from reputation records.

    C[i][j] = normalized positive outcome from observers[i] about subjects[j].
    """
    n = len(observers)
    m = len(subjects)
    raw = [[0 for _ in range(m)] for _ in range(n)]

    # Accumulate positive outcomes only (v > 0), as in the paper's definition.
    for r in records:
        if r.record_type != "reputation":
            continue
        if r.observer not in observers or r.subject not in subjects:
            continue
        i = observers.index(r.observer)
        j = subjects.index(r.subject)
        if r.outcome > 0:
            raw[i][j] += r.outcome

    # Normalize each row. If a row is all zeros, use the uniform distribution.
    C = [[Fraction(0) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        total = sum(raw[i])
        if total == 0:
            for j in range(m):
                C[i][j] = Fraction(1, m)
        else:
            for j in range(m):
                C[i][j] = Fraction(raw[i][j], total)
    return C


def _anchor_distribution(anchors: list[str], subjects: list[str]) -> list[Fraction]:
    """Uniform distribution over the anchor set Γ₀."""
    m = len(subjects)
    if not anchors:
        return [Fraction(1, m) for _ in range(m)]
    p = [Fraction(0) for _ in range(m)]
    for a in anchors:
        if a in subjects:
            p[subjects.index(a)] = Fraction(1, len(anchors))
    return p


def _iterate(
    C: list[list[Fraction]],
    p: list[Fraction],
    a: Fraction,
    K: int,
) -> list[Fraction]:
    """Iterate t ← (1 − a) · Cᵀ t + a · p for K steps.

    Initial t is the uniform distribution.
    """
    m = len(p)
    t = [Fraction(1, m) for _ in range(m)]
    one_minus_a = Fraction(1) - a

    for _ in range(K):
        # Compute Cᵀ t: for each j, sum_i C[i][j] * t[i].
        ct = [Fraction(0) for _ in range(m)]
        for i in range(len(C)):
            ti = t[i]
            if ti == 0:
                continue
            row = C[i]
            for j in range(m):
                ct[j] += row[j] * ti
        t = [one_minus_a * ct[j] + a * p[j] for j in range(m)]
    return t


def reputation_of(
    records: Iterable[ReputationRecord],
    anchors: list[str] | None = None,
) -> dict[str, Fraction]:
    """Compute the reputation vector over all subjects in `records`.

    - Observers and subjects are sorted canonically (lexicographic by id).
    - Iteration count K = 100.
    - Damping a = 1/5.
    - Exact arithmetic (Fraction).
    """
    records = list(records)
    observers_set = {r.observer for r in records if r.record_type == "reputation"}
    subjects_set = {r.subject for r in records if r.record_type == "reputation"}
    observers = sorted(observers_set)
    subjects = sorted(subjects_set)

    if not subjects:
        return {}

    C = _build_local_trust(records, observers, subjects)
    p = _anchor_distribution(anchors or [], subjects)
    t = _iterate(C, p, DAMPING, K)
    return {subjects[j]: t[j] for j in range(len(subjects))}


def reputation_residual(
    records: Iterable[ReputationRecord],
    anchors: list[str] | None = None,
) -> Fraction:
    """‖T(t_K) − t_K‖₁, for the convergence check (T06)."""
    records = list(records)
    observers = sorted({r.observer for r in records if r.record_type == "reputation"})
    subjects = sorted({r.subject for r in records if r.record_type == "reputation"})
    if not subjects:
        return Fraction(0)

    C = _build_local_trust(records, observers, subjects)
    p = _anchor_distribution(anchors or [], subjects)
    t_K = _iterate(C, p, DAMPING, K)
    # One more iteration.
    m = len(p)
    ct = [Fraction(0) for _ in range(m)]
    for i in range(len(C)):
        for j in range(m):
            ct[j] += C[i][j] * t_K[i]
    t_next = [(Fraction(1) - DAMPING) * ct[j] + DAMPING * p[j] for j in range(m)]
    return sum(abs(t_next[j] - t_K[j]) for j in range(m))
