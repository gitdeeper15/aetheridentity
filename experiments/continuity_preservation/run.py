"""Experiment 2 — Continuity Preservation.

Measures: whether an agent's identity is preserved across multiple
epochs (restarts), and whether the continuity chain is verified.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aetheridentity.models import Identity
from aetheridentity.continuity import record_continuity, verify_chain


def run() -> dict:
    results = []
    for i in range(10):
        identity = Identity(public_key=f"pk-{i}", semantic_label=f"agent-{i}")
        records = [record_continuity(identity.id, "genesis", "epoch-1", "h1")]
        for epoch in range(2, 6):
            records.append(
                record_continuity(identity.id, f"epoch-{epoch-1}", f"epoch-{epoch}", f"h{epoch}")
            )
        chain_ok = verify_chain(records, identity.id)
        # Verify identity id is preserved
        later = Identity(public_key=f"pk-{i}", semantic_label=f"agent-{i}")
        preserved = later.id == identity.id
        results.append({
            "identity_id": identity.id,
            "epochs": len(records),
            "chain_ok": chain_ok,
            "preserved": preserved,
        })

    return {
        "experiment": "continuity_preservation",
        "metric": "M2 — Continuity preservation",
        "count": len(results),
        "results": results,
        "summary": {
            "all_chains_ok": all(r["chain_ok"] for r in results),
            "all_preserved": all(r["preserved"] for r in results),
            "max_epochs": max(r["epochs"] for r in results),
        },
    }


if __name__ == "__main__":
    out = run()
    (Path(__file__).parent / "results.json").write_text(json.dumps(out, indent=2))
    s = out["summary"]
    print(f"✅ {Path(__file__).parent / 'results.json'}")
    print(f"  count: {out['count']}")
    print(f"  all chains ok: {s['all_chains_ok']}")
    print(f"  all preserved: {s['all_preserved']}")
    print(f"  max epochs: {s['max_epochs']}")
