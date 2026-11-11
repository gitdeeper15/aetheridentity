# AetherIdentity v2.0.0 — Test Execution Report

**Phase:** 5 (Test Execution)
**Date:** 2026-11-11
**Test runner:** pytest 9.0.3
**Python:** 3.13.13
**Platform:** Android (Termux)
**Coverage tool:** pytest-cov 7.1.0
**Total coverage:** **93%**

---

## 1. Summary

| Metric | Value |
|---|---|
| Tests collected | 35 |
| Tests passed | 35 |
| Tests failed | 0 |
| Tests skipped | 0 |
| Tests designed in Phase 3 | 24 |
| Tests deferred | 4 (T18, T19, T20, T22) |
| Tests not testable in v2.0.0 | 6 (see §6) |

The 35 tests exceed the 24 designed in Phase 3 because Phase 4 added edge-case tests
that were implicit in the invariants but not enumerated in `TESTS.md`.

---

## 2. Test results by module

| Module | Tests | Passed | Failed |
|---|---|---|---|
| `test_smoke.py` | 7 | 7 | 0 |
| `test_continuity.py` | 6 | 6 | 0 |
| `test_reputation.py` | 6 | 6 | 0 |
| `test_sybil.py` | 5 | 5 | 0 |
| `test_delegation.py` | 11 | 11 | 0 |
| **Total** | **35** | **35** | **0** |

---

## 3. Invariant coverage

| Invariant | Tests | Status |
|---|---|---|
| I1 — Permutation invariance | `test_reputation_permutation_invariance` | ✅ |
| I2 — Identifier determinism | `test_identifier_determinism` | ✅ |
| I3 — Chain validity | `test_rotation_reveals_committed_key` | ✅ |
| I4 — Fork visibility | `test_fork_detected_with_same_predecessor` | ✅ |
| I5 — Reputation determinism | `test_reputation_determinism` | ✅ |
| I6 — Fixed-point convergence | `test_reputation_fixed_point_convergence` | ✅ |
| I7 — Delegation monotonicity | `test_validate_widening_rejected`, `test_validate_longer_expiry_rejected` | ✅ |
| I8 — Revocation propagation | `test_revocation_propagates` | ✅ |
| I9 — Cluster weight | `test_cluster_weight_with_tau_claims` | ✅ |
| I10 — Detection rates reported | `test_detection_rates` | ✅ |
| I11 — Signer separation | `test_signer_separation` | ✅ |
| I12 — Structural vs. crypto | `test_canonical_json_is_stable` + signer tests | ✅ |

**All 12 core invariants are covered.**

---

## 4. Failure-condition and proposition coverage

| Claim | Test | Status |
|---|---|---|
| F1 — Non-redundancy | `test_f1_bounded_extension` | ⏳ Deferred (requires AetherGovern/AetherMesh simulator) |
| F2 — Orthogonality | `test_f2_verified_claims` | ⏳ Deferred (requires AetherProof simulator) |
| F3 — Boundary with governance | `test_governance_overlap_zero`, `test_governance_overlap_full` | ✅ Partially (overlap function exists; full S6 evaluation is Phase 6) |
| F4 — Decentralizability | `test_cluster_weight_with_tau_claims`, delegation tests | ✅ Partially (residuals measurable; full evaluation is Phase 6) |
| F5 — Observable benefit | `test_f5_decision_rule` | ⏳ Deferred (requires all baselines and scenarios) |
| P1 — Determinism | `test_reputation_determinism`, `test_identifier_determinism` | ✅ |
| P2 — Bootstrap | `test_p2_bootstrap` | ⏳ Deferred (requires bootstrap scenario; S1 in Phase 6) |

---

## 5. Deferred tests

| Test | Reason | Where it would run |
|---|---|---|
| T18 — F1 bounded extension | Requires AetherGovern/AetherMesh simulator | Future version |
| T19 — F2 verified claims | Requires AetherProof simulator | Future version |
| T20 — F5 decision rule | Requires all scenarios S1–S6 and baselines B1–B5 | Phase 6 |
| T22 — Sequential admission only | Enforced by `Simulator.admit` (no concurrency API) | — (enforced by design) |

---

## 6. Tests not testable under v2.0.0

| Item | Reason |
|---|---|
| Concurrent admission | Out of scope (`SPECIFICATION.md` §2.4) |
| Causal delivery | Out of scope |
| Fork resolution | Out of scope |
| Recovery after total key loss | Out of scope |
| Single-instance enforcement | Requires bounded agreement |
| Byzantine behavior | Out of scope |

These are **not** reported as passing. They are reported as **not testable under v2.0.0**.

---

## 7. Coverage

| Module | Coverage | Missing lines |
|---|---|---|
| `__init__.py` | 100% | — |
| `signer.py` | 100% | — |
| `sybil.py` | 98% | 62 |
| `continuity.py` | 97% | 103 |
| `identity.py` | 97% | 50 |
| `records.py` | 97% | 42, 108 |
| `delegation.py` | 91% | 43, 77, 80, 86, 107, 150, 194, 215, 245 |
| `simulator.py` | 91% | 34, 46 |
| `reputation.py` | 85% | 39, 70, 72, 83-84, 96-100, 123, 149, 166 |
| **TOTAL** | **93%** | 29 lines |

The uncovered lines are edge cases (error branches, empty-cluster paths, non-matching identity). They do not affect the core invariants, all of which are covered.

Coverage JSON is in `ANALYSIS/coverage.json`.

---

## 8. Reproduction

```bash
cd /storage/emulated/0/Download/AetherIdentity
python3 -m pytest tests/ -v --cov=src/aetheridentity --cov-report=term-missing --cov-report=json:ANALYSIS/coverage.json
```

The output should match §1.

---

9. What this report does not claim

· It does not claim that AetherIdentity is confirmed.
· It does not claim that F1–F5 are "not falsified" (that is Phase 6's job).
· It does not claim that the architecture is production-ready.
· It does not hide deferred tests: they are listed in §5.

This report records what was run, what passed, and what was not run.

---

10. Next phase

Phase 6 — Experimental Evaluation. The scenarios S1–S6 will be implemented in
experiments/, and the results will be written to REPORTS/v2.0.0/evaluation_report.md.
The evaluation follows the OSF-preregistered protocol (10.17605/OSF.IO/B6AEN).
