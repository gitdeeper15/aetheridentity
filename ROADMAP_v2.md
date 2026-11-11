# AetherIdentity v2.0.0 — Roadmap

**Status:** Planning approved
**Parent paper:** v1.0.0 (Formal Architecture Proposal, 33 pages, Zenodo 10.5281/zenodo.24102739)
**Target release:** v2.0.0 (Experimental Reference Implementation)
**Language:** Python
**Method:** Falsification-first. The reference implementation must allow the architecture to fail.

---

## 1. Version numbering

The version series is fixed as follows:

| Version | Status | Artifact |
|---|---|---|
| **v0.1.0** | Architectural Hypothesis | Original draft |
| **v1.0.0** | Formal Architecture Proposal | 33-page paper, published on Zenodo and Figshare |
| **v2.0.0** | Experimental Reference Implementation | Code, tests, experiments, report |

The paper is **not** renumbered. v1.0.0 is the authoritative hypothesis record. v2.0.0 is an implementation *of* it, not a replacement.

The existing Zenodo record `10.5281/zenodo.24102739` is labeled `0.1.0` in its metadata. This is a metadata inconsistency carried over from the preprint release; it does not change the version series above. Future deposits should use the series in this table.

---

## 2. Scope

### 2.1 In scope

- **Layer L1 — Identity.** Self-certifying identifiers; inception records; verification of key control.
- **Layer L2 — Continuity.** Key rotation with pre-committed next keys; fork detection; recovery (guardian-based, conditional).
- **Layer L3 — Reputation.** Signed observation records; deterministic score computation over the admitted set.
- **Layer L4 — Sybil Resistance.** Sponsor quotas; evidence-backed claims; cluster down-weighting; false-positive and false-negative measurement.
- **Layer L5 — Delegation.** Attenuating delegation chains; scope and expiry narrowing; revocation in the causal closure.
- **Interfaces (I1–I4).** Identity status, continuity records, reputation records, delegation records.
- **Simulator.** An independent, minimal simulator of replicated, causally ordered state. **Not** a dependency on AetherMesh.

### 2.2 Conditional scope

The following are *studied*, not committed to:

- **L5 independence from AetherGovern.** If the study shows that L5 cannot be specified without duplicating AetherGovern's authority chains, L5 is reported as **not separable**, and the architecture is revised accordingly. The reference implementation must allow this outcome.
- **L4 without a cost mechanism.** If the study shows that Sybil resistance without cost or attestation is not measurable, L4 is reported as **not evaluable under the stated assumptions**, and the corresponding metrics are reported as `not applicable`.
- **Recovery after total key loss.** If the guardian-based design proves unsafe under the stated threat model, recovery is reported as **not implementable without an anchor**, and the corresponding test is skipped with a documented reason.

### 2.3 Out of scope

- Production deployment.
- Integration with AetherMesh, AetherGovern, AetherRuntime, or AetherOrchestrate (integration is studied as an optional test, not as a requirement).
- Real-world data (synthetic data only).
- Guaranteed Sybil detection (heuristic only).
- Removal of the trust anchor (P2 is irreducible).
- Machine-checked proofs of P1 and P2 (future work).

### 2.4 What v2.0.0 is not allowed to do

- It is not allowed to claim that the architecture is confirmed.
- It is not allowed to hide a failed test by adjusting the metric.
- It is not allowed to change the OSF-preregistered protocol without a documented amendment.
- It is not allowed to depend on AetherMesh for its primary evaluation.

---

## 3. The Seven Phases

### Phase 1 — Architectural Specification

**Input:** v1.0.0 paper, sections 3–6.
**Output:** `SPECIFICATION.md` (v2.0.0). Operational specification: modules, interfaces, data types, invariants.

**Exit criterion:** Every definition in the paper (D1–D4) has a corresponding specification entry. Every layer (L1–L5) has a corresponding module specification. Every interface (I1–I4) is defined with its inputs and outputs.

**Stop condition:** If a layer cannot be specified without a decision that the paper does not make, the decision is recorded in `SPECIFICATION.md` as an *open decision*, and Phase 1 does not exit until it is resolved or explicitly deferred.

---

### Phase 2 — Invariant Definition

**Input:** `SPECIFICATION.md`.
**Output:** `INVARIANTS.md`. A numbered list of invariants (I1–I*n*) that every run must satisfy.

**Exit criterion:** Each invariant is stated in a form that can be checked mechanically. Each invariant is mapped to a failure condition (F1–F5) or a proposition (P1–P2).

**Stop condition:** If an invariant cannot be checked by the simulator, it is either weakened to a checkable form or reported as *not checkable* with a documented reason.

---

### Phase 3 — Test Design

**Input:** `INVARIANTS.md`.
**Output:** `TESTS.md`. Test names, preconditions, postconditions, and expected outcomes.

**Exit criterion:** Every invariant has at least one test. Every failure condition (F1–F5) has at least one test that would falsify it. The test count is *determined by the invariants*, not assumed in advance.

**Stop condition:** If a test cannot be written without an implementation decision that the specification does not make, the test is deferred with a documented reason.

---

### Phase 4 — Reference Implementation

**Input:** `SPECIFICATION.md`, `INVARIANTS.md`, `TESTS.md`.
**Output:** `src/aetheridentity/`. Python modules for L1–L5 and interfaces.

**Exit criterion:** All modules import without error. All tests run. The simulator can execute a minimal scenario end-to-end.

**Stop condition:** If a module cannot be implemented without violating an invariant, the invariant is re-examined in Phase 2, and the implementation is paused until the conflict is resolved.

---

### Phase 5 — Test Execution

**Input:** `tests/`.
**Output:** `REPORTS/v2.0.0/test_report.md`. Test results, coverage, and a list of failing tests with diagnoses.

**Exit criterion:** All tests pass, or all failures are documented with a root-cause analysis.

**Stop condition:** If more than a stated fraction of tests fail (threshold set in Phase 3), the implementation returns to Phase 4.

---

### Phase 6 — Experimental Evaluation

**Input:** `experiments/`, `DATA/synthetic/`.
**Output:** `ANALYSIS/`, `REPORTS/v2.0.0/evaluation_report.md`. Results for S1–S6.

**Exit criterion:** All six scenarios have been executed at least once. All results are reported, whether or not they support the architecture. F5 is assessed against the pre-registered decision rule.

**Stop condition:** If the OSF-preregistered protocol cannot be followed, an amendment is documented in `OSF/final_report/amendment.md` *before* the affected experiment is run.

---

### Phase 7 — Release

**Input:** All artifacts.
**Output:** v2.0.0 tag, PyPI package (conditional), Zenodo record, updated website.

**Exit criterion:** All artifacts are present and consistent. The release report states what the architecture supports and what it does not.

**Stop condition:** If any artifact is missing or inconsistent, release is deferred.

---

## 4. Phase outputs

| Phase | Primary output | Secondary outputs |
|---|---|---|
| 1 | `SPECIFICATION.md` | `docs/architecture/` |
| 2 | `INVARIANTS.md` | — |
| 3 | `TESTS.md` | — |
| 4 | `src/aetheridentity/` | `pyproject.toml` |
| 5 | `REPORTS/v2.0.0/test_report.md` | coverage data |
| 6 | `REPORTS/v2.0.0/evaluation_report.md` | `ANALYSIS/`, `DATA/synthetic/` |
| 7 | `RELEASE/RELEASE.md` | PyPI, Zenodo, website |

---

## 5. Phase transition criteria

A phase is considered complete only when:

1. Its primary output exists.
2. Its exit criterion is met.
3. No stop condition is active.
4. The output is committed to version control.

A phase may be **reopened** if a later phase reveals a contradiction. Reopening is recorded in `REPORTS/v2.0.0/phase_log.md`.

---

## 6. Stop and redesign conditions

The project stops, or a phase is redesigned, if any of the following occurs:

- **S1.** A layer cannot be specified without contradicting the paper.
- **S2.** An invariant cannot be checked mechanically.
- **S3.** A test cannot be written without an implementation decision the specification does not make.
- **S4.** A module cannot be implemented without violating an invariant.
- **S5.** More than the threshold of tests fail in Phase 5.
- **S6.** An experiment cannot be run under the OSF-preregistered protocol.
- **S7.** An experiment result contradicts a claim in the paper, and the contradiction cannot be resolved by re-reading the paper.

In any of these cases, the project records the condition in `REPORTS/v2.0.0/stop_log.md` and does one of:

- **Redesign** the affected phase.
- **Narrow** the scope.
- **Report** the architecture as falsified on the affected condition.

---

## 7. The six concerns (from the planning decision)

### 7.1 P1 and P2

- P1 is not translated directly into a Python function. It is translated into a **test**: given a set of admitted records, two independent nodes must derive the same identifier, status, reputation vector, and cluster weights. The test fails if they diverge.
- P2 is not translated into a theorem. It is translated into a **measurement**: the minimum number of externally trusted identities required to bootstrap a simulated network. The measurement is reported, not asserted.

### 7.2 F3 (delegation vs. governance)

L5 gets an independent test scenario (**S6_delegation**) that measures the overlap with a simulated AetherGovern. The test reports:

- The fraction of L5 decisions that can be re-expressed as AetherGovern decisions.
- The fraction that cannot.
- The sensitivity of this fraction to the authority-chain depth.

If the first fraction is high, F3 is reported as **falsified** (L5 folds into governance).

### 7.3 F4 residuals

The five residuals identified in the paper (trust anchor, fork resolution, total-key-loss recovery, single-instance enforcement, Sybil assumptions) are **not hidden** in the simulator. Each is exposed as:

- A configuration parameter.
- A test that measures its effect.
- A line in the evaluation report.

If a residual cannot be measured, it is reported as *not measurable under the current simulator*.

### 7.4 Sybil detection

- **False positives** and **false negatives** are measured separately.
- The report does not claim that all Sybil identities can be detected.
- The report states the conditions under which the measured rates hold.

### 7.5 AetherMesh

- The simulator is **independent**. It does not require AetherMesh.
- Integration with AetherMesh is studied in **S7** (optional), and reported separately.
- A failure of AetherIdentity is not attributed to AetherMesh, and vice versa.

### 7.6 OSF

- The experiments follow the OSF-preregistered protocol (`10.17605/OSF.IO/B6AEN`).
- Any deviation is documented in `OSF/final_report/amendment.md` *before* the affected experiment is run.
- The final report (`OSF/final_report/`) mirrors the preregistration's structure.

---

## 8. Relationship to the published paper

| Paper section | v2.0.0 phase | Output |
|---|---|---|
| §3 Definitions | Phase 1 | `SPECIFICATION.md` |
| §4 Failure conditions | Phase 2, Phase 6 | `INVARIANTS.md`, evaluation report |
| §5 Requirements | Phase 1, Phase 3 | `SPECIFICATION.md`, `TESTS.md` |
| §6 Architecture (five layers) | Phase 1, Phase 4 | `SPECIFICATION.md`, `src/aetheridentity/` |
| §8 Evaluation design | Phase 6 | `REPORTS/v2.0.0/evaluation_report.md` |
| §9 Threats | Phase 6 | evaluation report |
| §10 Open questions | All phases | `REPORTS/v2.0.0/open_questions.md` |

**The paper is not modified.** v2.0.0 implements it, or reports where it cannot be implemented.

---

## 9. What success and failure look like

### Success (v2.0.0 is a research success)

- All seven phases are completed, or stopped with documented reasons.
- All experiments are run and reported.
- The evaluation report states clearly which claims of the paper are supported, which are not, and which are untested.
- The reference implementation is reproducible from `REPORTS/v2.0.0/`.

### Failure (v2.0.0 is a research failure, not a project failure)

- The architecture is shown to be **not separable** from an existing dimension (F1 or F3 falsified).
- The architecture is shown to require a central authority or strong consistency (F4 falsified).
- The architecture is shown to have no observable benefit (F5 falsified).

A research failure is reported as a result. It is not hidden.

### What v2.0.0 must not do

- It must not claim "confirmed" for any failure condition.
- It must not adjust a metric after observing the result.
- It must not describe a heuristic as a guarantee.
- It must not present a simulation as a deployment.

---

## 10. Implementation principles

1. **Falsification-first.** Every test must be able to fail. A test that cannot fail is not a test.
2. **Determinism.** Given the same inputs and the same seed, the simulator produces the same outputs, bit for bit.
3. **Explicit assumptions.** Every assumption is a configuration parameter, named and documented.
4. **No hidden dependencies.** The simulator does not require AetherMesh, AetherGovern, or any other Aether component for its primary evaluation.
5. **Reproducibility.** Every result in the evaluation report can be regenerated from the committed code and data.
6. **Documented deviations.** Any deviation from the paper or from the OSF protocol is recorded before the affected test or experiment is run.

---

## 11. Planning status

**Status:** Approved.
**Next step:** Phase 1 — `SPECIFICATION.md`.

No code is written until Phase 1 exits.
