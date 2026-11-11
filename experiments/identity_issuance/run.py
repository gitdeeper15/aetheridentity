"""Experiment 1 — Identity Issuance Accuracy.

Measures: whether issuing identities with random public keys produces
unique, deterministic identities, and whether the verify function
accepts correct signatures and rejects incorrect ones.
"""

from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aetheridentity.identity import issue, verify


def run() -> dict:
    results = []
    for i in range(50):
        pk = f"pub-key-{i}"
        r = issue(public_key=pk, semantic_label=f"agent-{i}")
        # Verify with correct signature
        msg = f"hello-{i}"
        sig = hashlib.sha256((pk + msg).encode()).hexdigest()
        ok = verify(r.identity, sig, msg)
        # Verify with wrong signature
        bad = verify(r.identity, "wrong", msg)
        results.append({
            "identity_id": r.identity.id,
            "issued": r.valid,
            "correct_verified": ok,
            "wrong_rejected": not bad,
        })

    return {
        "experiment": "identity_issuance",
        "metric": "M1 — Identity issuance accuracy",
        "count": len(results),
        "results": results,
        "summary": {
            "all_issued": all(r["issued"] for r in results),
            "all_verified": all(r["correct_verified"] for r in results),
            "all_wrong_rejected": all(r["wrong_rejected"] for r in results),
            "unique_ids": len({r["identity_id"] for r in results}),
        },
    }


if __name__ == "__main__":
    out = run()
    (Path(__file__).parent / "results.json").write_text(json.dumps(out, indent=2))
    s = out["summary"]
    print(f"✅ {Path(__file__).parent / 'results.json'}")
    print(f"  count: {out['count']}")
    print(f"  all issued: {s['all_issued']}")
    print(f"  all verified: {s['all_verified']}")
    print(f"  all wrong rejected: {s['all_wrong_rejected']}")
    print(f"  unique ids: {s['unique_ids']}")
