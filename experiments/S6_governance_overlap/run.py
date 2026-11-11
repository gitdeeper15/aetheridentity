"""S6 — Governance overlap (F3: boundary with governance).

Question: can L5 delegation decisions be re-expressed as AetherGovern
authority decisions?

If the fraction of overlapping decisions is >= 0.80, F3 is falsified
(L5 folds into AetherGovern).

This experiment:
- Constructs a set of delegation records.
- Constructs a simulated AetherGovern authority model.
- Measures the overlap fraction.
- Reports whether the overlap crosses the F3 threshold.

Output: experiments/S6_governance_overlap/results.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent.parent / "src"
sys.path.insert(0, str(SRC))

from aetheridentity.delegation import (
    Scope,
    delegate,
    governance_overlap,
)
from aetheridentity.records import record_hash
from aetheridentity.signer import FakeSigner

F3_THRESHOLD = 0.80


def scenario_low_overlap() -> dict:
    """L5 delegates to parties NOT authorized by AetherGovern."""
    signer = FakeSigner()
    records = [
        delegate(signer, "alice", "bob", Scope(frozenset({"read"})), 100, "", 0),
        delegate(signer, "alice", "carol", Scope(frozenset({"write"})), 100, "", 1),
    ]
    # AetherGovern only authorizes alice -> dave.
    authority = {"alice": frozenset({"dave"})}
    overlap = governance_overlap(records, authority)
    return {
        "scenario": "low_overlap",
        "n_delegations": len(records),
        "overlap_fraction": overlap,
        "threshold": F3_THRESHOLD,
        "f3_falsified": overlap >= F3_THRESHOLD,
    }


def scenario_high_overlap() -> dict:
    """L5 delegates only to parties already authorized by AetherGovern."""
    signer = FakeSigner()
    records = [
        delegate(signer, "alice", "bob", Scope(frozenset({"read"})), 100, "", 0),
        delegate(signer, "alice", "carol", Scope(frozenset({"write"})), 100, "", 1),
    ]
    # AetherGovern authorizes both bob and carol.
    authority = {"alice": frozenset({"bob", "carol"})}
    overlap = governance_overlap(records, authority)
    return {
        "scenario": "high_overlap",
        "n_delegations": len(records),
        "overlap_fraction": overlap,
        "threshold": F3_THRESHOLD,
        "f3_falsified": overlap >= F3_THRESHOLD,
    }


def scenario_partial_overlap() -> dict:
    """Half of L5 delegations are already authorized by AetherGovern."""
    signer = FakeSigner()
    records = [
        delegate(signer, "alice", "bob", Scope(frozenset({"read"})), 100, "", 0),
        delegate(signer, "alice", "carol", Scope(frozenset({"write"})), 100, "", 1),
    ]
    authority = {"alice": frozenset({"bob"})}
    overlap = governance_overlap(records, authority)
    return {
        "scenario": "partial_overlap",
        "n_delegations": len(records),
        "overlap_fraction": overlap,
        "threshold": F3_THRESHOLD,
        "f3_falsified": overlap >= F3_THRESHOLD,
    }


def main() -> None:
    runs = [scenario_low_overlap(), scenario_high_overlap(), scenario_partial_overlap()]
    out = {
        "experiment": "S6_governance_overlap",
        "purpose": "Test F3 (boundary with governance)",
        "threshold": F3_THRESHOLD,
        "runs": runs,
        "f3_falsified_in_any_run": any(r["f3_falsified"] for r in runs),
    }
    path = Path(__file__).parent / "results.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"wrote {path}")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
