# AetherIdentity v2.0.0 — Invariants

**Version:** 2.0.0 (Phase 2)
**Parent paper:** v1.0.0 (Zenodo 10.5281/zenodo.24102739)
**Input:** SPECIFICATION.md (Phase 1)
**Status:** Invariants. No code.
**Decision record:** ROADMAP_v2.md

---

## 0. Purpose

This document defines the invariants that every run of the reference implementation must satisfy. Each invariant is:

1. Stated in a form that can be checked mechanically.
2. Mapped to a failure condition (F1–F5) or a proposition (P1–P2).
3. Accompanied by its failure mode (what a violation would mean).

An invariant that cannot be checked mechanically is either weakened to a checkable form or reported as **not checkable** with a documented reason.

---

## 1. Invariant format

Each invariant has the following fields:

| Field | Meaning |
|---|---|
| **ID** | `I1`, `I2`, … |
| **Statement** | What must hold. |
| **Check** | How it is checked (function, test, or property). |
| **Bears on** | F1–F5 or P1–P2. |
| **Failure mode** | What a violation means. |
| **Status** | `checkable` / `not checkable` / `deferred`. |

---

## 2. Core invariants (I1–I12)

### I1 — Determinism of queries

**Statement.** For any `S`, any permutation `S'` of `S`, and any query function `q`, `q(S) == q(S')`.

**Check.** Property-based test: generate random `S`, permute, compare outputs bit-for-bit.

**Bears on.** P1.

**Failure mode.** A query function depends on the order of `S`. This would mean the specification's claim that `S` is a set (not a sequence) is false, and P1 cannot hold.

**Status.** `checkable`.

---

### I2 — Identifier determinism

**Statement.** For any two inception records `r1`, `r2` with the same `(alg, pk, λ)`, `id(r1) == id(r2)`.

**Check.** Construct two records with identical inputs; compare identifiers.

**Bears on.** P1.

**Failure mode.** Identifier derivation is not a deterministic function of its inputs. This would contradict Definition 1 and make P1's condition (a) false.

**Status.** `checkable`.

---

### I3 — Continuity chain validity

**Statement.** For any `id` with a continuity chain `C` in `S`, `C` is valid: `r₀` is self-signed, and for each `k ≥ 1`, `H(pk_k) == c_{k-1}`, `h_{k-1}` is correct, and `o_k` verifies under `pk_k`.

**Check.** Recompute the chain from `S`; verify each link.

**Bears on.** P1, F4.

**Failure mode.** A rotation record is accepted without a valid pre-commitment. This would mean the continuity chain does not enforce the offline-key rule.

**Status.** `checkable`.

---

### I4 — Fork visibility

**Statement.** If two valid rotation records share a predecessor and differ in content, `status_of(S, id) == "contested"`.

**Check.** Construct a fork; assert status.

**Bears on.** F4.

**Failure mode.** A fork is silently resolved. This would mean the specification hides the fork-resolution residual.

**Status.** `checkable`.

---

### I5 — Reputation determinism

**Statement.** For any `S`, `reputation_of(S, id)` is computed in exact arithmetic with a fixed iteration count `K` and a canonical ordering, and returns the same vector for every node holding the same `S`.

**Check.** Two independent computations on the same `S`; compare vectors bit-for-bit.

**Bears on.** P1.

**Failure mode.** The reputation vector depends on floating-point arithmetic, iteration count, or ordering. This would contradict P1's condition (c).

**Status.** `checkable`.

---

### I6 — Reputation fixed point

**Statement.** The reputation iteration `t ← (1 − a) · Cᵀ t + a · p` converges to a fixed point within `K` iterations, with error below a stated tolerance.

**Check.** Compute the residual `‖T(t_K) − t_K‖₁`; assert below tolerance.

**Bears on.** P1.

**Failure mode.** The iteration does not converge within `K`. This would mean the exact-arithmetic claim is not satisfied.

**Status.** `checkable`.

---

### I7 — Delegation monotonicity

**Statement.** For any valid delegation chain `d₁ → d₂ → … → dₙ`, `S_n ⊆ S_{n-1} ⊆ … ⊆ S₁` and `e_n ≤ e_{n-1} ≤ … ≤ e₁`.

**Check.** Construct chains with random scopes and expiries; assert monotonicity.

**Bears on.** F4.

**Failure mode.** Scope or expiry can widen along the chain. This would contradict Definition 4.

**Status.** `checkable`.

---

### I8 — Revocation propagation

**Statement.** If a delegation `d_k` in a chain is revoked, then for any action whose causal closure contains the revocation, the action is invalid.

**Check.** Construct a chain, revoke a link, assert invalidity.

**Bears on.** F4.

**Failure mode.** Revocation does not invalidate downstream links. This would contradict Definition 4.

**Status.** `checkable`.

---

### I9 — Sybil cluster weight

**Statement.** For any identity `id` in a Sybil cluster of size `m`, `cluster_weight_of(S, id) == 1.0 / m`.

**Check.** Construct a cluster; assert weight.

**Bears on.** F4.

**Failure mode.** Cluster weight is not deterministic or not `1/m`. This would mean L4 does not down-weight clusters.

**Status.** `checkable`.

---

### I10 — Sybil detection rates reported

**Statement.** For any Sybil scenario, both false-positive rate (on honest operators) and false-negative rate (on injected clusters) are reported.

**Check.** Assert both fields exist and are numeric in `results.json`.

**Bears on.** F4, F5.

**Failure mode.** Only one rate is reported. This would allow a detector that flags everything to score perfectly on detection.

**Status.** `checkable`.

---

### I11 — Signature separation

**Statement.** A signature produced by `FakeSigner` is not accepted by `Ed25519Signer`, and vice versa.

**Check.** Sign with one, verify with the other; assert `False`.

**Bears on.** P1, F2.

**Failure mode.** The two signers are interchangeable. This would mean the cryptographic verification path is not separated from the test path.

**Status.** `checkable`.

---

### I12 — Structural vs. cryptographic verification

**Statement.** For every record, structural validation and signature verification are checked separately, and both results are reported.

**Check.** Assert both fields exist in the test report.

**Bears on.** P1, F2.

**Failure mode.** The two checks are merged. This would allow a structurally valid but cryptographically invalid record to pass.

**Status.** `checkable`.

---

## 3. Failure-condition invariants (F1–F5)

### 3.1 F1 — Non-redundancy

**Claim.** At least one requirement R1–R6 is not met by L1–L5 plus a bounded extension of one existing dimension.

**How it can be falsified.** A test that expresses all R1–R6 as a bounded extension of exactly one Aether dimension.

**Invariant.** If such a test exists and passes, F1 is falsified.

**Status.** `deferred` (requires AetherGovern/AetherMesh simulator; see S6).

---

### 3.2 F2 — Orthogonality to verification

**Claim.** Some identity decisions cannot be encoded as verified claims.

**How it can be falsified.** A test that encodes every identity decision as a verified claim.

**Invariant.** If such a test exists and passes, F2 is falsified.

**Status.** `deferred` (requires AetherProof simulator).

---

### 3.3 F3 — Boundary with governance

**Claim.** Identity is not reducible to governance plus conventional verification.

**How it can be falsified.** In S6, the fraction of L5 decisions re-expressible as AetherGovern decisions is high (threshold fixed in Phase 3).

**Invariant.** If the fraction exceeds the threshold, F3 is falsified.

**Status.** `checkable` (in S6).

---

### 3.4 F4 — Decentralizability

**Claim.** Most identity functions are monotone or deterministic functions of monotone state; four residuals require something outside the replicated state.

**How it can be falsified.** A test that shows a central authority or strong consistency is required for a function that the specification classifies as agreement-free.

**Invariant.** Every function classified as agreement-free must be computable by two nodes holding the same `S` without communication.

**Status.** `checkable`.

---

### 3.5 F5 — Observable benefit

**Claim.** There exists a scenario class in which the best baseline fails and AetherIdentity succeeds.

**How it can be falsified.** For every scenario, some baseline is non-inferior on the primary metrics, or M9 is ever non-zero.

**Invariant.** If F5's decision rule (from OSF preregistration) is satisfied, F5 is falsified.

**Status.** `deferred` (requires all scenarios S1–S6 and all baselines B1–B5).

---

## 4. Proposition invariants (P1–P2)

### 4.1 P1 — Determinism of local identity issuance

**Claim.** Under conditions (a)–(d), admission satisfies A6, and all honest nodes derive the same views once delivery is complete.

**Invariant.** Two nodes with the same `S` derive identical `status_of`, `reputation_of`, `cluster_weight_of`, `continuity_chain_of`, `delegation_chain_of`.

**Status.** `checkable`.

**Failure mode.** A view differs between nodes with the same `S`. This falsifies P1.

---

### 4.2 P2 — Irreducible trust anchor

**Claim.** Any identity protocol that admits on evidence leaves an irreducible trust anchor.

**How it can be falsified.** A simulated network bootstraps without any externally trusted identity.

**Invariant.** If such a bootstrap succeeds, P2 is falsified.

**Status.** `checkable` (in S1, with a documented bootstrap procedure).

---

## 5. Open decisions resolved here

Phase 1 listed seven open decisions (O1–O7). Phase 2 resolves them as follows:

| # | Decision | Resolution |
|---|---|---|
| O1 | Fixed iteration count `K` | `K = 100` for exact arithmetic; convergence checked in I6. |
| O2 | Canonical ordering of identities | Lexicographic by identifier hash. |
| O3 | Exact arithmetic for reputation | `fractions.Fraction` for the iteration; final vector rounded to 6 decimal places for reporting only. |
| O4 | Threshold `τ` for Sybil clusters | `τ = 2` for v2.0.0; tested for sensitivity in S5. |
| O5 | Epoch length for sponsor quotas | `1` logical epoch = `100` admissions; tested for sensitivity in S5. |
| O6 | Whether recovery is implemented | **No.** Out of scope for v2.0.0; documented as a residual. |
| O7 | Whether L5 is separable from AetherGovern | Tested in S6; result reported in Phase 6. |

These resolutions are **binding** for Phase 4. Changing them requires an amendment in `REPORTS/v2.0.0/phase_log.md`.

---

## 6. Invariants that are not checkable in v2.0.0

The following are **not checkable** in v2.0.0, and are reported as such in Phase 5:

| Invariant | Reason | Where it would be checkable |
|---|---|---|
| Concurrent admission | Out of scope (§2.4 of SPECIFICATION.md) | Future version with concurrency |
| Causal delivery | Out of scope | Future version with AetherMesh integration |
| Fork resolution | Out of scope | Future version with an authority model |
| Recovery after total key loss | Out of scope | Future version with a guardian protocol |
| Single-instance enforcement | Requires bounded agreement | Future version with consensus |
| Byzantine behavior | Out of scope | Future version with adversarial model |

These are **not** reported as passing. They are reported as **not testable under v2.0.0**.

---

## 7. Invariant coverage

| Invariant | Bears on | Phase 3 test | Phase 5 status |
|---|---|---|---|
| I1 | P1 | `test_permutation_invariance` | — |
| I2 | P1 | `test_identifier_determinism` | — |
| I3 | P1, F4 | `test_chain_validity` | — |
| I4 | F4 | `test_fork_visibility` | — |
| I5 | P1 | `test_reputation_determinism` | — |
| I6 | P1 | `test_fixed_point_convergence` | — |
| I7 | F4 | `test_delegation_monotonicity` | — |
| I8 | F4 | `test_revocation_propagation` | — |
| I9 | F4 | `test_cluster_weight` | — |
| I10 | F4, F5 | `test_detection_rates` | — |
| I11 | P1, F2 | `test_signer_separation` | — |
| I12 | P1, F2 | `test_structural_vs_crypto` | — |
| F1 | F1 | `test_f1_bounded_extension` | deferred |
| F2 | F2 | `test_f2_verified_claims` | deferred |
| F3 | F3 | `test_f3_governance_overlap` | checkable (S6) |
| F4 | F4 | `test_f4_agreement_free` | — |
| F5 | F5 | `test_f5_decision_rule` | deferred |
| P1 | P1 | `test_p1_same_s` | — |
| P2 | P2 | `test_p2_bootstrap` | checkable (S1) |

---

## 8. Next phase

Phase 3 — `TESTS.md`. Each invariant in §7 becomes at least one test with preconditions, postconditions, and expected outcome. The test count is **determined by the invariants**, not assumed in advance.

---

## Appendix A — Invariant summary

| ID | Short name | Status |
|---|---|---|
| I1 | Permutation invariance | checkable |
| I2 | Identifier determinism | checkable |
| I3 | Chain validity | checkable |
| I4 | Fork visibility | checkable |
| I5 | Reputation determinism | checkable |
| I6 | Fixed-point convergence | checkable |
| I7 | Delegation monotonicity | checkable |
| I8 | Revocation propagation | checkable |
| I9 | Cluster weight | checkable |
| I10 | Detection rates reported | checkable |
| I11 | Signer separation | checkable |
| I12 | Structural vs. crypto | checkable |
| F1 | Non-redundancy | deferred |
| F2 | Orthogonality | deferred |
| F3 | Governance overlap | checkable (S6) |
| F4 | Agreement-free | checkable |
| F5 | Decision rule | deferred |
| P1 | Same-S determinism | checkable |
| P2 | Bootstrap | checkable (S1) |

## Appendix B — Relationship to v1.0.0 paper

| Paper section | This document |
|---|---|
| §3 Definitions | §2 (I2, I3, I5) |
| §4 Failure conditions | §3 |
| §5 Requirements | §7 |
| §6 Architecture | §2, §4 |
| §8 Evaluation design | §6, §7 |
| §10 Open questions | §5 (resolves O1–O7) |
