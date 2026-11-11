# AetherIdentity v2.0.0 — Architectural Specification

**Version:** 2.0.0 (Phase 1)
**Parent paper:** v1.0.0 (Zenodo 10.5281/zenodo.24102739)
**Status:** Specification. No code.
**Decision record:** ROADMAP_v2.md

---

## 0. Purpose and constraints

This document specifies the operational surface of AetherIdentity v2.0.0. It is the input to Phase 4 (Reference Implementation). It is **not** a promise that the architecture works. It is a specification precise enough to be tested — and precise enough to **fail** if the architecture does not hold.

Three architectural decisions were fixed before this document was written:

| # | Decision | Rationale |
|---|---|---|
| D-S | Replicated state `S` is a **flat list of records**. | Keeps state simple; makes all queries pure functions. |
| D-T | Records are **dataclasses**; JSON is the canonical serialization. | Separates data model from transport. |
| D-G | Signatures use an **abstract `Signer`** with two implementations: `FakeSigner` (tests only) and `Ed25519Signer` (real). | Allows fast tests without weakening cryptographic verification. |

These decisions are **binding** for Phase 4. Changing them requires an amendment in `REPORTS/v2.0.0/phase_log.md`.

---

## 1. Scope

### 1.1 In scope

- L1 — Identity.
- L2 — Continuity.
- L3 — Reputation.
- L4 — Sybil resistance.
- L5 — Delegation.
- Interfaces I1–I4.
- A minimal, independent simulator of replicated state `S`.

### 1.2 Out of scope (v2.0.0)

- Network transport.
- Consensus.
- AetherMesh integration (studied as S7, optional).
- Production security.
- Machine-checked proofs of P1/P2.
- Guaranteed Sybil detection.
- Removal of the trust anchor.

### 1.3 What this specification must not do

- It must not assume P1 or P2 is true.
- It must not assume F1–F5 will be "not falsified".
- It must not hide the residual assumptions of F4.
- It must allow a test to fail for every claim.

---

## 2. Architectural decision 1 — Replicated state `S`

### 2.1 Definition

`S` is a **flat list** of admitted records. There is no deletion of admitted records. There is no silent replacement.

```python
S: list[Record]
```

Where Record is the union of the record types in §3.

2.2 Ordering

The order of S is admission order, not causal order. The simulator appends records as they are admitted. Two nodes that have admitted the same records in the same order hold the same S.

Ordering is not part of the meaning of S. All queries in §5 must be invariant under permutation of S. If a query is not permutation-invariant, the query is mis-specified.

2.3 Duplicates

A record is identified by its canonical serialization hash (§4.3). A record whose hash already appears in S is not appended again. This is the only deduplication rule.

2.4 What S does not solve

The flat list S does not solve:

· Concurrent admission.
· Fork resolution.
· Causal ordering.
· Conflict resolution.

These are out of scope for v2.0.0. The simulator admits records sequentially, and the specification says so explicitly. If a future version introduces concurrency, S will be re-specified.

2.5 Consequences for falsifiability

Because S is flat and admission is sequential, a test that depends on concurrent admission cannot be written in v2.0.0. Such a test is recorded in REPORTS/v2.0.0/stop_log.md as not testable under v2.0.0, not as passing.

---

3. Architectural decision 2 — Records as dataclasses with canonical JSON

3.1 Record types

Four record types, each a Python dataclass:

Type Purpose Paper reference
InceptionRecord Identity creation Definition 1
RotationRecord Key rotation Definition 2
ReputationRecord Signed observation Definition 3
DelegationRecord Scoped authority Definition 4

A fifth type, SybilClaim, is used by L4:

| SybilClaim | Evidence-backed claim of shared control | §6.4 |

3.2 Common fields

Every record has:

· record_type: str — one of "inception", "rotation", "reputation", "delegation", "sybil_claim".
· signer_id: str — the identifier of the signer.
· signature: bytes — signature over the canonical serialization.
· created_at: int — logical timestamp (monotonic counter, not wall clock).

3.3 Canonical serialization

Before signing, every record is serialized to canonical JSON:

· Keys sorted lexicographically.
· No whitespace.
· UTF-8 encoding.
· Integers only (no floats).
· Byte fields encoded as lowercase hex.

The canonical form of a record r is canon(r).

The signature is over H(canon(r)), where H is SHA-256.

3.4 Validation vs. signature verification

Two separate checks, never merged:

Check What it verifies When
Structural validation The record has all required fields, correct types, and satisfies the schema. Before signature verification.
Signature verification The signature is valid under the signer's public key. After structural validation.

A record that passes structural validation but fails signature verification is rejected, not stored. A record that fails structural validation is rejected before signature verification is attempted.

3.5 Consequence for falsifiability

A test may not claim "signature verified" if only structural validation passed. The specification requires both checks to be reported separately in the test report.

---

4. Architectural decision 3 — Abstract Signer

4.1 Interface

```python
class Signer(Protocol):
    def sign(self, message: bytes) -> bytes: ...
    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool: ...
    def public_key(self) -> bytes: ...
```

4.2 Implementations

Implementation Use Security
FakeSigner Unit tests, scenarios None. Not cryptographic.
Ed25519Signer Integration tests, evaluation Real Ed25519.

FakeSigner must not be used in experiments/. The evaluation report must state which signer was used for each experiment.

4.3 Rule

A signature produced by FakeSigner is not accepted by Ed25519Signer, and vice versa. The two signers are not interchangeable within the same run.

4.4 Consequence for falsifiability

A test that passes with FakeSigner and fails with Ed25519Signer is reported as a failure of the specification, not as a passing test. The specification requires that the same tests pass under both signers, or that the difference is documented as a limitation.

---

5. Query functions

All queries are pure functions of S and must be invariant under permutation of S.

Function Input Output Paper reference
status_of S, id IdentityStatus §6.6
reputation_of S, id ReputationVector Definition 3
continuity_chain_of S, id list[RotationRecord] Definition 2
delegation_chain_of S, id list[DelegationRecord] Definition 4
cluster_weight_of S, id float §6.4
is_valid_delegation S, action, chain bool Definition 4

5.1 Determinism

Given the same S, each function must return the same output bit for bit. This is checked by a test in Phase 3.

5.2 Exact arithmetic

reputation_of and cluster_weight_of must use exact arithmetic (integers or fractions.Fraction), not floating point. The fixed iteration count K and the canonical ordering are specified in INVARIANTS.md (Phase 2).

5.3 Consequence for falsifiability

If a query function is not permutation-invariant, the test fails. The specification does not allow a query to be "approximately invariant".

---

6. Layer specifications

6.1 L1 — Identity

Question. Who is the agent, and can it prove it?

Inputs. InceptionRecord.

Operations.

· create_identity(signer, label) -> InceptionRecord.
· verify_identity(S, id) -> bool.

Specification.

· The identifier is H(tag ‖ alg ‖ pk ‖ λ).
· The label is a claim, not a verified fact.
· Two agents with the same label and different keys have different identifiers.

What L1 does not specify.

· Standing (which is L4).
· Authority (which is L5).
· Reputation (which is L3).

6.2 L2 — Continuity

Question. Does the identity persist?

Inputs. InceptionRecord, RotationRecord.

Operations.

· rotate_key(S, id, new_pk, signer) -> RotationRecord.
· detect_fork(S, id) -> bool.

Specification.

· A rotation is valid only if the new key's hash equals the previous commitment.
· A fork is two valid rotations with the same predecessor and different content.
· A forked identity has status contested.

What L2 does not specify.

· Fork resolution (out of scope; see F4 residuals).
· Recovery after total key loss (out of scope for v2.0.0; see §11).

6.3 L3 — Reputation

Question. What is the behavioral history?

Inputs. ReputationRecord.

Operations.

· record_observation(S, observer, subject, evidence, outcome) -> ReputationRecord.
· reputation_of(S, id) -> ReputationVector.

Specification.

· Records are signed observations.
· The score is the fixed point of the EigenTrust-style iteration, computed in exact arithmetic.
· The score is a view over S, not a stored value.

What L3 does not specify.

· Whether reputation may influence admission (policy decision; see §6.3 in the paper).
· Whether reputation is per-task-class (open question Q10).

6.4 L4 — Sybil resistance

Question. Is one entity behind many identities?

Inputs. SybilClaim.

Operations.

· issue_sybil_claim(S, attester, target, evidence) -> SybilClaim.
· cluster_weight_of(S, id) -> float.

Specification.

· A claim is evidence-backed, not a proof.
· A cluster is formed from claims signed by at least τ distinct anchored attesters.
· The cluster weight divides each member's weight by cluster size.
· Detection is heuristic; false positives and false negatives are measured separately.

What L4 does not specify.

· Detection guarantees (none are claimed).
· Admissible evidence (open question Q13).
· The threshold τ (open question Q14).

6.5 L5 — Delegation

Question. Can authority move with bounded scope?

Inputs. DelegationRecord.

Operations.

· delegate(S, delegator, delegatee, scope, expiry) -> DelegationRecord.
· validate_delegation(S, action, chain) -> bool.

Specification.

· A delegation is valid only if S_d ⊆ S_p, e_d ≤ e_p, and the parent is valid.
· Effective scope is the intersection; effective expiry is the minimum.
· Revocation of any link invalidates all downstream links.

What L5 does not specify.

· Whether L5 is separable from AetherGovern (tested in S6; if not separable, F3 is falsified).
· The scope language (example only; open question Q16).
· Retroactive vs. prospective revocation (open question Q17).

---

7. Interfaces (I1–I4)

Interface Inputs Outputs Used by
I1 — Identity status S, id IdentityStatus L1, L2, L5
I2 — Continuity records S, id list[RotationRecord] L2, L5
I3 — Reputation records S, id ReputationVector L3, L4
I4 — Delegation records S, id list[DelegationRecord] L5

Interfaces are pure. No interface mutates S.

---

8. The simulator

8.1 Independence

The simulator does not depend on AetherMesh, AetherGovern, AetherRuntime, or AetherOrchestrate. It models replicated state as a flat list (§2).

8.2 Sequential admission

The simulator admits records sequentially, in the order they are produced. It does not model:

· Concurrent admission.
· Causal delivery.
· Fork resolution.

These are out of scope for v2.0.0.

8.3 Scenario execution

A scenario is a Python script in experiments/S*/ that:

1. Creates a Simulator.
2. Admits records.
3. Calls query functions.
4. Writes results to experiments/S*/results.json.

8.4 Consequence for falsifiability

Because admission is sequential, a test that requires concurrency cannot be written in v2.0.0. Such a test is recorded in REPORTS/v2.0.0/stop_log.md as not testable under v2.0.0.

---

9. What the specification does not specify

The following are open decisions, to be resolved in Phase 2 (INVARIANTS.md) or documented as out of scope:

# Open decision Where it is resolved
O1 Fixed iteration count K for reputation Phase 2
O2 Canonical ordering of identities Phase 2
O3 Exact arithmetic for reputation Phase 2
O4 Threshold τ for Sybil clusters Phase 2
O5 Epoch length for sponsor quotas Phase 2
O6 Whether recovery is implemented Phase 2
O7 Whether L5 is separable from AetherGovern Phase 6 (S6)

---

10. Falsifiability constraints

The specification is designed so that each of the following can fail:

Claim How it can fail
P1 Two nodes with the same S derive different views.
P2 A simulated network can bootstrap without any externally trusted identity.
F1 All R1–R6 are met by L1–L5 plus a bounded extension of one existing dimension.
F2 Every identity decision is a verified claim.
F3 L5 decisions are fully re-expressible as AetherGovern decisions.
F4 The residuals cannot be confined; a central authority is required.
F5 Every scenario is non-inferior under a baseline.

The specification does not assume any of these will fail or pass. It specifies the mechanisms that allow the test to decide.

---

11. Out of scope (v2.0.0)

· Fork resolution.
· Recovery after total key loss (guardian-based recovery is a hypothesis, not a commitment).
· Single-instance enforcement (requires bounded agreement; out of scope).
· Concurrency.
· AetherMesh integration (S7, optional).
· Production deployment.

---

12. Next phase

Phase 2 — INVARIANTS.md. The invariants will be stated in a form that can be checked mechanically. Each invariant maps to a failure condition or a proposition.

---

Appendix A — Notation

Symbol Meaning
S Flat list of admitted records
id Identity identifier
H SHA-256
canon(r) Canonical JSON serialization of record r
K Fixed iteration count (Phase 2)
τ Sybil cluster threshold (Phase 2)
Γ₀ Trust anchor set

Appendix B — Relationship to v1.0.0 paper

Paper section This specification
§3 Definitions §3 (records), §5 (queries)
§4 Failure conditions §10
§5 Requirements §6 (layers)
§6 Architecture §6
§8 Evaluation design §8 (simulator)
§11 Conclusion §12 (next phase)

