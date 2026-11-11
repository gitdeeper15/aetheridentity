"""Tests for L4 — Sybil Resistance."""

from aetheridentity.records import SybilClaim
from aetheridentity.signer import FakeSigner
from aetheridentity.sybil import (
    TAU,
    cluster_weight_of,
    detection_rates,
    issue_sybil_claim,
)


def test_sybil_claim_signed():
    """L4: a Sybil claim is signed and well-formed."""
    signer = FakeSigner()
    claim = issue_sybil_claim(signer, "alice", "bob", "evidence-1", created_at=0)
    assert claim.record_type == "sybil_claim"
    assert claim.attester == "alice"
    assert claim.target == "bob"
    assert claim.signature != b""


def test_cluster_weight_with_tau_claims():
    """T09: cluster weight is 1/m when tau claims link the members."""
    signer = FakeSigner()
    anchored = {"alice", "carol", "dave"}
    claims = [
        issue_sybil_claim(signer, "alice", "bob", "shared-evidence", 1),
        issue_sybil_claim(signer, "carol", "bob", "shared-evidence", 2),
        issue_sybil_claim(signer, "alice", "dave", "shared-evidence", 3),
        issue_sybil_claim(signer, "carol", "dave", "shared-evidence", 4),
    ]
    cluster = {"alice", "bob", "carol", "dave"}
    m = len(cluster)
    for member in cluster:
        w = cluster_weight_of(claims, member, anchored=anchored, tau=TAU)
        assert w == 1.0 / m, f"{member} has weight {w}, expected {1.0/m}"


def test_no_cluster_below_tau():
    """L4: fewer than tau distinct attesters means no cluster."""
    signer = FakeSigner()
    anchored = {"alice"}
    claims = [
        issue_sybil_claim(signer, "alice", "bob", "shared-evidence", 1),
        issue_sybil_claim(signer, "alice", "bob", "shared-evidence", 2),
    ]
    w = cluster_weight_of(claims, "bob", anchored=anchored, tau=TAU)
    assert w == 1.0


def test_detection_rates():
    """T10: both false-positive and false-negative rates are reported."""
    predicted = {"sybil-1", "sybil-2", "honest-1"}
    ground_truth = {"sybil-1", "sybil-2", "sybil-3"}
    honest_operators = {"honest-1", "honest-2", "honest-3"}

    rates = detection_rates(predicted, ground_truth, honest_operators)

    assert "detection_rate" in rates
    assert "false_positive_rate" in rates
    assert "false_negative_rate" in rates
    assert abs(rates["detection_rate"] - 2 / 3) < 1e-9
    assert abs(rates["false_positive_rate"] - 1 / 3) < 1e-9
    assert abs(rates["false_negative_rate"] - 1 / 3) < 1e-9


def test_detection_rates_empty_honest():
    """L4: no division by zero when there are no honest operators."""
    rates = detection_rates({"a"}, {"a"}, set())
    assert rates["false_positive_rate"] == 0.0
