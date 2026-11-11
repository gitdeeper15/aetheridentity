"""Experiment 3 — Delegation Scope Correctness.

Measures: whether delegations grant only authorized capabilities, and
whether expired delegations are correctly rejected.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aetheridentity.models import Identity, DelegationScope
from aetheridentity.delegation import delegate, authorize


def run() -> dict:
    results = []
    for i in range(20):
        a = Identity(public_key=f"pk-a-{i}")
        b = Identity(public_key=f"pk-b-{i}")
        caps = [f"cap-{j}" for j in range(5)]
        # Non-expired delegation
        d_ok = delegate(a, b, caps, DelegationScope.NARROW, expires_in=3600)
        # Expired delegation
        d_exp = delegate(a, b, caps, DelegationScope.NARROW, expires_in=-1)

        authorized_ok = [authorize(b, c, [d_ok]) for c in caps]
        authorized_exp = [authorize(b, c, [d_exp]) for c in caps]
        # Unauthorized capability
        unauthorized = authorize(b, "cap-unknown", [d_ok])

        results.append({
            "delegation_ok": all(authorized_ok),
            "delegation_expired_rejected": not any(authorized_exp),
            "unauthorized_rejected": not unauthorized,
        })

    return {
        "experiment": "delegation_scope",
        "metric": "M3 — Delegation scope correctness",
        "count": len(results),
        "results": results,
        "summary": {
            "all_authorized_ok": all(r["delegation_ok"] for r in results),
            "all_expired_rejected": all(r["delegation_expired_rejected"] for r in results),
            "all_unauthorized_rejected": all(r["unauthorized_rejected"] for r in results),
        },
    }


if __name__ == "__main__":
    out = run()
    (Path(__file__).parent / "results.json").write_text(json.dumps(out, indent=2))
    s = out["summary"]
    print(f"✅ {Path(__file__).parent / 'results.json'}")
    print(f"  count: {out['count']}")
    print(f"  all authorized ok: {s['all_authorized_ok']}")
    print(f"  all expired rejected: {s['all_expired_rejected']}")
    print(f"  all unauthorized rejected: {s['all_unauthorized_rejected']}")
