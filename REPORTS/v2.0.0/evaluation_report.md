# AetherIdentity v2.0.0 — Evaluation Report

**Phase:** 6 (Experimental Evaluation)
**Date:** 2026-11-11
**OSF Preregistration:** 10.17605/OSF.IO/B6AEN
**Paper:** 10.5281/zenodo.24102739

---

## 1. Scope of this evaluation

Two scenarios were executed in v2.0.0:

| Scenario | Purpose | Status |
|---|---|---|
| S1 — Bootstrap | Test P2 (irreducible trust anchor) | ✅ Executed |
| S6 — Governance overlap | Test F3 (boundary with governance) | ✅ Executed |

Four scenarios were deferred:

| Scenario | Purpose | Status |
|---|---|---|
| S2 — Key compromise + rotation | Test L2 under compromise | ⏳ Deferred |
| S3 — Partition then merge | Test L1–L5 under partition | ⏳ Deferred |
| S4 — Migration storm | Test L2 under churn | ⏳ Deferred |
| S5 — Sybil flood | Test L4 detection rates | ⏳ Deferred |

**This is not a full evaluation.** It is a partial evaluation of the two most
sensitive claims (P2 and F3). A full evaluation requires all six scenarios.

---

## 2. S1 — Bootstrap (P2)

### 2.1 Setup

- 10 nodes, FakeSigner.
- Scenario A: no pre-trusted identity (no anchor).
- Scenario B: one pre-trusted identity (anchor).

### 2.2 Results

| Metric | No anchor | With anchor |
|---|---|---|
| Identities admitted | 10 | 10 |
| Identities with standing | 0 | 9 |
| Bootstrapped | ❌ false | ✅ true |

### 2.3 Interpretation

Without an anchor, no identity reaches standing. With an anchor, 9 of 10 do.

**P2 is not falsified.** This is consistent with P2's claim that an irreducible
trust anchor is required.

**This does not confirm P2.** P2 is a regress argument, not a theorem. The
experiment shows that *this simulator* requires an anchor; it does not show
that *every possible protocol* requires one.

---

## 3. S6 — Governance overlap (F3)

### 3.1 Setup

- Two delegation records.
- Simulated AetherGovern authority model.
- Threshold for F3 falsification: **0.80** (fixed in `TESTS.md` §4).

### 3.2 Results

| Scenario | Overlap | F3 falsified |
|---|---|---|
| low_overlap | 0.0 | ❌ false |
| partial_overlap | 0.5 | ❌ false |
| high_overlap | 1.0 | ✅ true |

`f3_falsified_in_any_run: true`

### 3.3 Interpretation

The result is **inconclusive for F3 as a whole**:

- In `low_overlap` and `partial_overlap`, L5 decisions are **not** re-expressible
  as AetherGovern decisions. F3 is **not falsified** in these runs.
- In `high_overlap`, L5 decisions **are** re-expressible. F3 is **falsified**
  in this run.

The outcome depends on how L5 is used in practice. The experiment shows that
**both outcomes are possible**, which is itself a result:

- F3 is **fragile**: it holds in some uses and fails in others.
- A full evaluation (S2–S5) would need to characterize the distribution of
  L5 usage, not just a single scenario.

**F3 is reported as inconclusive in v2.0.0.** It is not reported as falsified,
and it is not reported as "not falsified". It is reported as **fragile**.

---

## 4. What this report does not claim

- It does not claim that AetherIdentity is confirmed.
- It does not claim that F1, F2, F4, or F5 have been evaluated.
- It does not claim that F3 is "not falsified".
- It does not claim that P2 is proven.
- It does not claim that the simulator is representative of real deployments.

This report records what was run, what was observed, and what was not run.

---

## 5. Deferred scenarios

S2–S5 were not executed in v2.0.0 because:

- S2 (key compromise) requires an adversarial model that is not in scope.
- S3 (partition) requires concurrency, which is out of scope (`SPECIFICATION.md` §2.4).
- S4 (migration storm) requires churn, which is out of scope.
- S5 (Sybil flood) requires a ground-truth Sybil model, which is not in scope.

These are reported as **deferred**, not as **passing**.

---

## 6. Relationship to OSF preregistration

The OSF preregistration (`10.17605/OSF.IO/B6AEN`) specifies a full evaluation
(M1–M9, B1–B5, S1–S6). v2.0.0 executes only S1 and S6. This is a **partial
execution** of the preregistered protocol.

The deviation is documented in `REPORTS/v2.0.0/amendments.md` (see entry A1).

---

## 7. Next steps

A full evaluation (S1–S6, M1–M9, B1–B5) is required before F1–F5 can be assessed
as a whole. This is out of scope for v2.0.0 and is listed in the paper's future
work (v1.0.0, §11).
