# AetherIdentity v2.0.0 — Release Report

**Version:** 2.0.0
**Date:** 2026-11-11
**Type:** Experimental Reference Implementation
**Parent paper:** v1.0.0 (Zenodo 10.5281/zenodo.24102739)
**OSF Preregistration:** 10.17605/OSF.IO/B6AEN

---

## 1. Summary

AetherIdentity v2.0.0 is a **partial reference implementation** of the identity
architecture specified in the v1.0.0 paper. It implements:

- L1 — Identity.
- L2 — Continuity.
- L3 — Reputation.
- L4 — Sybil resistance.
- L5 — Delegation.
- Interfaces I1–I4.
- A minimal independent simulator of replicated state `S`.

It does **not** implement:

- Network transport.
- Consensus.
- AetherMesh integration.
- Fork resolution.
- Recovery after total key loss.
- Single-instance enforcement.
- Byzantine behavior.

These are **out of scope** for v2.0.0 and are documented in `SPECIFICATION.md` §11.

---

## 2. What v2.0.0 supports

| Component | Status | Where |
|---|---|---|
| L1 — Identity | ✅ Implemented | `src/aetheridentity/identity.py` |
| L2 — Continuity | ✅ Implemented | `src/aetheridentity/continuity.py` |
| L3 — Reputation | ✅ Implemented | `src/aetheridentity/reputation.py` |
| L4 — Sybil resistance | ✅ Implemented | `src/aetheridentity/sybil.py` |
| L5 — Delegation | ✅ Implemented | `src/aetheridentity/delegation.py` |
| Simulator | ✅ Implemented | `src/aetheridentity/simulator.py` |
| Signer interface | ✅ Implemented | `src/aetheridentity/signer.py` |
| Record types | ✅ Implemented | `src/aetheridentity/records.py` |

---

## 3. Test results

| Metric | Value |
|---|---|
| Tests collected | 35 |
| Tests passed | 35 |
| Tests failed | 0 |
| Coverage | 93% |

All 12 core invariants (I1–I12) are covered. See `REPORTS/v2.0.0/test_report.md`.

---

## 4. Experimental results

| Scenario | Purpose | Result |
|---|---|---|
| S1 — Bootstrap | Test P2 | **P2 not falsified** (bootstrap requires an anchor) |
| S6 — Governance overlap | Test F3 | **F3 inconclusive** (fragile: holds in some uses, fails in others) |

Four scenarios (S2–S5) are **deferred** and reported as such.

See `REPORTS/v2.0.0/evaluation_report.md`.

---

## 5. What v2.0.0 does not claim

- It does not claim that AetherIdentity is confirmed.
- It does not claim that F1–F5 are "not falsified".
- It does not claim that P1–P2 are proven.
- It does not claim that the architecture is production-ready.
- It does not claim that the simulator is representative of real deployments.

This is a **research artifact**, not a product.

---

## 6. What changed from v1.0.0

| Aspect | v1.0.0 | v2.0.0 |
|---|---|---|
| Type | Paper | Paper + reference implementation |
| Code | None | `src/aetheridentity/` (8 modules) |
| Tests | None | 35 tests, 93% coverage |
| Experiments | None | S1 + S6 executed |
| OSF | Preregistration | Partial execution reported |

**The paper is not modified.** v2.0.0 implements it, and reports where it cannot.

---

## 7. How to reproduce

```bash
# Clone the repository
git clone https://github.com/gitdeeper15/aetheridentity.git
cd aetheridentity

# Install (development mode)
pip install -e ".[dev]"

# Run tests
pytest

# Run experiments
python experiments/S1_bootstrap/run.py
python experiments/S6_governance_overlap/run.py
```

See REPORTS/v2.0.0/test_report.md and REPORTS/v2.0.0/evaluation_report.md.

---

8. Files in this release

File Description
README.md Project overview
SPECIFICATION.md Architectural specification (Phase 1)
INVARIANTS.md Invariants (Phase 2)
TESTS.md Test design (Phase 3)
ROADMAP_v2.md Roadmap for v2.0.0
pyproject.toml Package configuration
src/aetheridentity/ Reference implementation
tests/ Test suite (35 tests)
experiments/S1_bootstrap/ S1 scenario
experiments/S6_governance_overlap/ S6 scenario
DATA/synthetic/ Synthetic data directory (empty)
ANALYSIS/coverage.json Code coverage
REPORTS/v2.0.0/ Test report, evaluation report, amendments, logs
RELEASE/RELEASE.md This file

---

9. Known limitations

1. Partial evaluation. Only S1 and S6 are executed. F1, F2, F4, and F5 are
   not evaluated in v2.0.0.
2. F3 is inconclusive. The experiment shows that F3 is fragile: it holds in
   some uses of L5 and fails in others. A full evaluation would require
   characterizing the distribution of L5 usage.
3. The simulator is not a network. It does not model concurrency, causal
   delivery, or Byzantine behavior.
4. The reference implementation is not production-grade. It is a research
   artifact.

---

10. Next steps

The following are not part of v2.0.0 and are listed for future work:

1. Full evaluation (S1–S6, M1–M9, B1–B5).
2. AetherMesh integration (optional, S7).
3. Fork resolution.
4. Recovery after total key loss.
5. Single-instance enforcement.
6. Machine-checked proofs of P1 and P2.

See ROADMAP_v2.md for the planning context.

---

11. Citation

```bibtex
@software{baladi2026aetheridentity_v2,
  author       = {Baladi, Samir},
  title        = {{AetherIdentity} v2.0.0: Reference Implementation of the
                  Falsification-First Identity Architecture},
  year         = {2026},
  month        = {November},
  version      = {2.0.0},
  doi          = {10.5281/zenodo.24102739},
  url          = {https://doi.org/10.5281/zenodo.24102739},
  note         = {Reference implementation. Paper: v1.0.0.}
}
```

---

AetherIdentity v2.0.0 — Experimental Reference Implementation
© 2026 Samir Baladi — Ronin Institute / Rite of Renaissance — MIT (code) + CC-BY-4.0 (docs)
