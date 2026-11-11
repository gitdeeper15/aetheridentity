"""L4 — Sybil Resistance (§6.4 of SPECIFICATION.md).

Implements:
- SybilClaim: signed, evidence-backed claim of shared control.
- Cluster formation: claims signed by at least tau distinct anchored attesters.
- cluster_weight_of: divide each member's weight by cluster size.
- detection_rates: separate false-positive and false-negative rates.

Out of scope (v2.0.0):
- Detection guarantees (none are claimed).
- Admissible evidence (open question Q13).
- Threshold tau (fixed at 2 in INVARIANTS.md).
"""

from __future__ import annotations

from typing import Iterable

from aetheridentity.records import SybilClaim, canonical_bytes
from aetheridentity.signer import Signer

TAU = 2  # threshold for cluster formation (INVARIANTS.md, O4)


def issue_sybil_claim(
    signer: Signer,
    attester: str,
    target: str,
    evidence: str,
    created_at: int = 0,
) -> SybilClaim:
    """Create and sign a Sybil claim."""
    record = SybilClaim(
        record_type="sybil_claim",
        signer_id=attester,
        created_at=created_at,
        attester=attester,
        target=target,
        evidence=evidence,
        t=created_at,
    )
    sig = signer.sign(canonical_bytes(record))
    return SybilClaim(**{**record.__dict__, "signature": sig})


def _cluster_of(
    records: Iterable[SybilClaim],
    anchored: set[str],
    tau: int = TAU,
) -> dict[str, set[str]]:
    """Build clusters from claims.

    A cluster is a set of identities linked by at least `tau` distinct
    anchored attesters. The evidence string is used as a grouping key:
    claims about the same evidence are considered to describe the same
    cluster.
    """
    # Group claims by evidence.
    by_evidence: dict[str, list[SybilClaim]] = {}
    for r in records:
        if r.record_type != "sybil_claim":
            continue
        by_evidence.setdefault(r.evidence, []).append(r)

    clusters: dict[str, set[str]] = {}
    for evidence, claims in by_evidence.items():
        distinct_attesters = {c.attester for c in claims if c.attester in anchored}
        if len(distinct_attesters) < tau:
            continue
        members: set[str] = set()
        for c in claims:
            members.add(c.attester)
            members.add(c.target)
        for m in members:
            clusters[m] = members
    return clusters


def cluster_weight_of(
    records: Iterable[SybilClaim],
    ident: str,
    anchored: set[str] | None = None,
    tau: int = TAU,
) -> float:
    """Return the weight of `ident` in its cluster (1/m), or 1.0 if not in a cluster."""
    anchored = anchored or set()
    clusters = _cluster_of(records, anchored, tau)
    if ident not in clusters:
        return 1.0
    return 1.0 / len(clusters[ident])


def detection_rates(
    predicted: set[str],
    ground_truth: set[str],
    honest_operators: set[str],
) -> dict[str, float]:
    """Compute false-positive and false-negative rates.

    - False positive rate: fraction of honest operators wrongly flagged.
    - False negative rate: fraction of true Sybils not flagged.
    - Detection rate: fraction of true Sybils flagged.
    """
    true_positives = predicted & ground_truth
    false_positives = (predicted - ground_truth) & honest_operators
    false_negatives = ground_truth - predicted

    fp_rate = len(false_positives) / len(honest_operators) if honest_operators else 0.0
    fn_rate = len(false_negatives) / len(ground_truth) if ground_truth else 0.0
    detection_rate = len(true_positives) / len(ground_truth) if ground_truth else 0.0

    return {
        "detection_rate": detection_rate,
        "false_positive_rate": fp_rate,
        "false_negative_rate": fn_rate,
        "true_positives": len(true_positives),
        "false_positives": len(false_positives),
        "false_negatives": len(false_negatives),
    }
