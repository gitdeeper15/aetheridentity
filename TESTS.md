# AetherIdentity v2.0.0 — Test Design

**Version:** 2.0.0 (Phase 3)
**Input:** INVARIANTS.md (Phase 2)
**Status:** Test design. No code.
**Decision record:** ROADMAP_v2.md

---

## 0. Purpose

This document specifies the tests that will be implemented in Phase 4 and executed in Phase 5. Each test is:

1. Named.
2. Mapped to an invariant from `INVARIANTS.md`.
3. Stated with preconditions, procedure, expected outcome, and failure mode.

The test count is **determined by the invariants**, not assumed in advance. The number of tests is reported in §5.

---

## 1. Test format

Each test has:

| Field | Meaning |
|---|---|
| **ID** | `T01`, `T02`, … |
| **Name** | Short, descriptive. |
| **Invariant** | `I1`–`I12`, `F1`–`F5`, `P1`, `P2`. |
| **Level** | `unit`, `integration`, `invariant`, `security`, `experiment`. |
| **Preconditions** | What must be true before the test runs. |
| **Procedure** | What the test does. |
| **Expected** | What must hold for the test to pass. |
| **Failure mode** | What a failure means. |
| **Signer** | `FakeSigner`, `Ed25519Signer`, or `both`. |

---

## 2. Unit tests (T01–T12)

### T01 — Permutation invariance

| Field | Value |
|---|---|
| **Invariant** | I1 |
| **Level** | unit |
| **Preconditions** | A random `S` of 20 records. |
| **Procedure** | Compute `q(S)` for each query `q`. Permute `S` to `S'`. Compute `q(S')`. |
| **Expected** | `q(S) == q(S')` for all `q`, bit for bit. |
| **Failure mode** | A query depends on order. P1's "same S" claim fails. |
| **Signer** | `FakeSigner` |

### T02 — Identifier determinism

| Field | Value |
|---|---|
| **Invariant** | I2 |
| **Level** | unit |
| **Preconditions** | A key pair and a label. |
| **Procedure** | Create two inception records with the same `(alg, pk, λ)`. |
| **Expected** | `id(r1) == id(r2)`. |
| **Failure mode** | Identifier derivation is not deterministic. P1's condition (a) fails. |
| **Signer** | `both` |

### T03 — Chain validity

| Field | Value |
|---|---|
| **Invariant** | I3 |
| **Level** | unit |
| **Preconditions** | A valid continuity chain of length 5. |
| **Procedure** | Recompute the chain from `S`. |
| **Expected** | Each link verifies; `H(pk_k) == c_{k-1}`; `o_k` verifies. |
| **Failure mode** | A rotation is accepted without a valid pre-commitment. |
| **Signer** | `both` |

### T04 — Fork visibility

| Field | Value |
|---|---|
| **Invariant** | I4 |
| **Level** | unit |
| **Preconditions** | A valid rotation `r1` from epoch `k`. |
| **Procedure** | Construct `r2` with the same predecessor, different content. Add both to `S`. |
| **Expected** | `status_of(S, id) == "contested"`. |
| **Failure mode** | The fork is silently resolved. F4's residual is hidden. |
| **Signer** | `FakeSigner` |

### T05 — Reputation determinism

| Field | Value |
|---|---|
| **Invariant** | I5 |
| **Level** | unit |
| **Preconditions** | A random `S` with reputation records. |
| **Procedure** | Compute `reputation_of(S, id)` twice, independently. |
| **Expected** | The two vectors are identical, bit for bit. |
| **Failure mode** | The vector depends on floating point or ordering. P1's condition (c) fails. |
| **Signer** | `FakeSigner` |

### T06 — Fixed-point convergence

| Field | Value |
|---|---|
| **Invariant** | I6 |
| **Level** | unit |
| **Preconditions** | A random `S` with reputation records. |
| **Procedure** | Compute `‖T(t_K) − t_K‖₁` after `K = 100` iterations. |
| **Expected** | Residual below `1e-6`. |
| **Failure mode** | The iteration does not converge within `K`. Exact-arithmetic claim fails. |
| **Signer** | `FakeSigner` |

### T07 — Delegation monotonicity

| Field | Value |
|---|---|
| **Invariant** | I7 |
| **Level** | unit |
| **Preconditions** | A delegation chain of length 5. |
| **Procedure** | For each link, check `S_k ⊆ S_{k-1}` and `e_k ≤ e_{k-1}`. |
| **Expected** | All links satisfy monotonicity. |
| **Failure mode** | Scope or expiry widens. Definition 4 is violated. |
| **Signer** | `FakeSigner` |

### T08 — Revocation propagation

| Field | Value |
|---|---|
| **Invariant** | I8 |
| **Level** | unit |
| **Preconditions** | A delegation chain of length 3. |
| **Procedure** | Revoke link 2. Attempt an action authorized by link 3. |
| **Expected** | The action is invalid. |
| **Failure mode** | Downstream links remain valid. Definition 4 is violated. |
| **Signer** | `FakeSigner` |

### T09 — Cluster weight

| Field | Value |
|---|---|
| **Invariant** | I9 |
| **Level** | unit |
| **Preconditions** | A Sybil cluster of size `m = 4`, with `τ = 2` claims. |
| **Procedure** | Compute `cluster_weight_of(S, id)` for each member. |
| **Expected** | `0.25` for each member. |
| **Failure mode** | Weight is not `1/m`. L4 does not down-weight. |
| **Signer** | `FakeSigner` |

### T10 — Detection rates reported

| Field | Value |
|---|---|
| **Invariant** | I10 |
| **Level** | unit |
| **Preconditions** | A Sybil scenario result. |
| **Procedure** | Inspect `results.json`. |
| **Expected** | Both `false_positive_rate` and `false_negative_rate` exist and are numeric. |
| **Failure mode** | Only one rate is reported. A "flag everything" detector would pass. |
| **Signer** | `FakeSigner` |

### T11 — Signer separation

| Field | Value |
|---|---|
| **Invariant** | I11 |
| **Level** | unit |
| **Preconditions** | A message. |
| **Procedure** | Sign with `FakeSigner`, verify with `Ed25519Signer`. Sign with `Ed25519Signer`, verify with `FakeSigner`. |
| **Expected** | Both verifications return `False`. |
| **Failure mode** | The two signers are interchangeable. Cryptographic separation fails. |
| **Signer** | `both` |

### T12 — Structural vs. cryptographic verification

| Field | Value |
|---|---|
| **Invariant** | I12 |
| **Level** | unit |
| **Preconditions** | A malformed record and a structurally valid record with an invalid signature. |
| **Procedure** | Run structural validation and signature verification separately. |
| **Expected** | Malformed: structural fails, signature not attempted. Invalid signature: structural passes, signature fails. |
| **Failure mode** | The two checks are merged. |
| **Signer** | `Ed25519Signer` |

---

## 3. Invariant tests (T13–T24)

### T13 — Agreement-free functions

| Field | Value |
|---|---|
| **Invariant** | F4 |
| **Level** | invariant |
| **Preconditions** | Two nodes with the same `S`. |
| **Procedure** | Each node computes `status_of`, `reputation_of`, `cluster_weight_of` independently. |
| **Expected** | Identical outputs. No communication between nodes. |
| **Failure mode** | A function needs communication. F4 is falsified. |
| **Signer** | `FakeSigner` |

### T14 — P1 same-S determinism

| Field | Value |
|---|---|
| **Invariant** | P1 |
| **Level** | invariant |
| **Preconditions** | Two nodes with the same `S`. |
| **Procedure** | Compute all views. |
| **Expected** | Identical views, bit for bit. |
| **Failure mode** | P1 is falsified. |
| **Signer** | `both` |

### T15 — P2 bootstrap

| Field | Value |
|---|---|
| **Invariant** | P2 |
| **Level** | invariant |
| **Preconditions** | A simulated network with no pre-trusted identity. |
| **Procedure** | Attempt to bootstrap admission. |
| **Expected** | Bootstrap fails without an external trust anchor. |
| **Failure mode** | Bootstrap succeeds. P2 is falsified. |
| **Signer** | `FakeSigner` |

### T16 — F3 governance overlap (S6)

| Field | Value |
|---|---|
| **Invariant** | F3 |
| **Level** | experiment |
| **Preconditions** | A simulated AetherGovern authority-chain model. |
| **Procedure** | For each L5 decision, attempt to re-express it as an AetherGovern decision. |
| **Expected** | Overlap fraction below a threshold fixed in Phase 3 (see §4). |
| **Failure mode** | Overlap fraction at or above threshold. F3 is falsified. |
| **Signer** | `FakeSigner` |

### T17 — F4 residuals measurable

| Field | Value |
|---|---|
| **Invariant** | F4 |
| **Level** | invariant |
| **Preconditions** | A scenario with the five F4 residuals as parameters. |
| **Procedure** | Run the scenario with each residual set to a different value. |
| **Expected** | Each residual has a measurable effect on at least one metric. |
| **Failure mode** | A residual is not measurable. It is hidden in the simulator. |
| **Signer** | `FakeSigner` |

### T18 — F1 bounded extension (deferred)

| Field | Value |
|---|---|
| **Invariant** | F1 |
| **Level** | experiment |
| **Preconditions** | An AetherGovern/AetherMesh simulator (not part of v2.0.0). |
| **Procedure** | Attempt to express R1–R6 as a bounded extension of one dimension. |
| **Expected** | At least one requirement cannot be so expressed. |
| **Failure mode** | All requirements are expressible. F1 is falsified. |
| **Signer** | `FakeSigner` |

### T19 — F2 verified claims (deferred)

| Field | Value |
|---|---|
| **Invariant** | F2 |
| **Level** | experiment |
| **Preconditions** | An AetherProof simulator (not part of v2.0.0). |
| **Procedure** | Attempt to encode every identity decision as a verified claim. |
| **Expected** | At least one decision cannot be encoded. |
| **Failure mode** | All decisions are encodable. F2 is falsified. |
| **Signer** | `FakeSigner` |

### T20 — F5 decision rule (deferred)

| Field | Value |
|---|---|
| **Invariant** | F5 |
| **Level** | experiment |
| **Preconditions** | All scenarios S1–S6 and all baselines B1–B5. |
| **Procedure** | Apply the OSF-preregistered decision rule. |
| **Expected** | F5 is "not falsified". |
| **Failure mode** | The rule says falsified. F5 is falsified. |
| **Signer** | `Ed25519Signer` (for cryptographic realism) |

### T21 — No silent deletion

| Field | Value |
|---|---|
| **Invariant** | I1, I5 |
| **Level** | invariant |
| **Preconditions** | A random `S`. |
| **Procedure** | Attempt to remove an admitted record. |
| **Expected** | The record is still present; no query returns a different result. |
| **Failure mode** | A record can be deleted silently. `S` is no longer a set. |
| **Signer** | `FakeSigner` |

### T22 — Sequential admission only

| Field | Value |
|---|---|
| **Invariant** | (out of scope) |
| **Level** | invariant |
| **Preconditions** | A simulator. |
| **Procedure** | Attempt concurrent admission. |
| **Expected** | The simulator raises an error or documents that concurrency is not supported. |
| **Failure mode** | Concurrency is silently accepted without being specified. |
| **Signer** | `FakeSigner` |

### T23 — Signature tampering detected

| Field | Value |
|---|---|
| **Invariant** | I11, I12 |
| **Level** | security |
| **Preconditions** | A valid signed record. |
| **Procedure** | Tamper with one byte of the canonical serialization. Verify. |
| **Expected** | Verification fails. |
| **Failure mode** | Tampering is accepted. Cryptographic verification is broken. |
| **Signer** | `Ed25519Signer` |

### T24 — Canonical JSON stability

| Field | Value |
|---|---|
| **Invariant** | (D-T) |
| **Level** | unit |
| **Preconditions** | A record with nested fields. |
| **Procedure** | Serialize to canonical JSON twice; compare bytes. |
| **Expected** | Identical byte sequences. |
| **Failure mode** | Canonicalization is unstable. Signatures would be inconsistent. |
| **Signer** | `FakeSigner` |

---

## 4. Thresholds fixed here

The following thresholds are fixed **before** Phase 4. Changing them requires an amendment in `REPORTS/v2.0.0/amendments.md`.

| Threshold | Value | Used in |
|---|---|---|
| Sybil cluster size for T09 | `m = 4` | T09 |
| Sybil threshold `τ` | `2` | T09, S5 |
| Epoch length | `100` admissions | S2, S5 |
| Reputation iteration count `K` | `100` | T06 |
| Reputation residual tolerance | `1e-6` | T06 |
| F3 overlap threshold | `0.80` | T16, S6 |
| F4 residual measurement tolerance | `10%` | T17 |
| Number of seeds per scenario | `10` | Phase 6 |

The F3 overlap threshold (`0.80`) is a **decision**: if 80% or more of L5 decisions can be re-expressed as AetherGovern decisions, F3 is falsified. This threshold is set before observing any result.

---

## 5. Test counts

| Level | Count |
|---|---|
| Unit | 12 (T01–T12) |
| Invariant | 6 (T13–T17, T21) |
| Security | 1 (T23) |
| Experiment (deferred) | 4 (T18–T20, T22) |
| Canonicalization | 1 (T24) |
| **Total** | **24** |

The count is **24** because the invariants require 24 tests. It is not a target.

---

## 6. Test dependencies

```

T01, T02 ─┐
T03 ──────┼──> T13 ──> T14 ──> T15
T04 ──────┤
T05, T06 ─┤
T07, T08 ─┤
T09, T10 ─┘
T11, T12 ──> T23
T24 ──────> (all signature tests)

```

A test is skipped if its dependency fails. Skips are reported in Phase 5, not hidden.

---

## 7. What is not tested in v2.0.0

The following are **not tested** in v2.0.0, and are reported as such in Phase 5:

| Item | Reason |
|---|---|
| Concurrent admission | Out of scope (§2.4 of SPECIFICATION.md) |
| Causal delivery | Out of scope |
| Fork resolution | Out of scope |
| Recovery after total key loss | Out of scope |
| Single-instance enforcement | Requires bounded agreement |
| Byzantine behavior | Out of scope |

These are **not** reported as passing. They are reported as **not testable under v2.0.0**.

---

## 8. Next phase

Phase 4 — Reference Implementation. The tests in this document become the `tests/` directory. The simulator in `src/aetheridentity/` implements the specification. No test is written before its invariant is specified, and no invariant is specified without a test that can fail.

---

## Appendix A — Test summary

| ID | Name | Invariant | Level |
|---|---|---|---|
| T01 | Permutation invariance | I1 | unit |
| T02 | Identifier determinism | I2 | unit |
| T03 | Chain validity | I3 | unit |
| T04 | Fork visibility | I4 | unit |
| T05 | Reputation determinism | I5 | unit |
| T06 | Fixed-point convergence | I6 | unit |
| T07 | Delegation monotonicity | I7 | unit |
| T08 | Revocation propagation | I8 | unit |
| T09 | Cluster weight | I9 | unit |
| T10 | Detection rates reported | I10 | unit |
| T11 | Signer separation | I11 | unit |
| T12 | Structural vs. crypto | I12 | unit |
| T13 | Agreement-free functions | F4 | invariant |
| T14 | P1 same-S determinism | P1 | invariant |
| T15 | P2 bootstrap | P2 | invariant |
| T16 | F3 governance overlap | F3 | experiment |
| T17 | F4 residuals measurable | F4 | invariant |
| T18 | F1 bounded extension | F1 | experiment (deferred) |
| T19 | F2 verified claims | F2 | experiment (deferred) |
| T20 | F5 decision rule | F5 | experiment (deferred) |
| T21 | No silent deletion | I1, I5 | invariant |
| T22 | Sequential admission only | — | invariant |
| T23 | Signature tampering detected | I11, I12 | security |
| T24 | Canonical JSON stability | D-T | unit |

## Appendix B — Relationship to Phase 2

| Invariant | Test(s) |
|---|---|
| I1 | T01, T21 |
| I2 | T02 |
| I3 | T03 |
| I4 | T04 |
| I5 | T05, T21 |
| I6 | T06 |
| I7 | T07 |
| I8 | T08 |
| I9 | T09 |
| I10 | T10 |
| I11 | T11, T23 |
| I12 | T12, T23 |
| F1 | T18 |
| F2 | T19 |
| F3 | T16 |
| F4 | T13, T17 |
| F5 | T20 |
| P1 | T14 |
| P2 | T15 |
