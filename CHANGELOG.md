# Changelog

All notable changes to AetherIdentity are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] — 2026-11-11

**Experimental Reference Implementation.**

### Added

- Python package `aetheridentity` (8 modules under `src/aetheridentity/`).
- L1 — Identity (`identity.py`).
- L2 — Continuity (`continuity.py`).
- L3 — Reputation (`reputation.py`).
- L4 — Sybil resistance (`sybil.py`).
- L5 — Delegation (`delegation.py`).
- Simulator (`simulator.py`).
- Abstract Signer with `FakeSigner` and `Ed25519Signer` (`signer.py`).
- Record types and canonical JSON serialization (`records.py`).
- 35 tests (93% coverage).
- S1 — Bootstrap (P2) executed.
- S6 — Governance overlap (F3) executed.
- `SPECIFICATION.md`, `INVARIANTS.md`, `TESTS.md`, `ROADMAP_v2.md`.
- `REPORTS/v2.0.0/` (test report, evaluation report, amendments, phase log, stop log).
- `RELEASE/RELEASE.md`.

### Changed

- README updated to reflect v2.0.0 (was v0.1.0).
- Version series fixed: v0.1.0 (hypothesis), v1.0.0 (paper), v2.0.0 (implementation).

### Not implemented

- Network transport, consensus.
- AetherMesh integration.
- Fork resolution.
- Recovery after total key loss.
- Single-instance enforcement.
- Byzantine behavior.

### Deferred

- S2, S3, S4, S5 (out of scope for v2.0.0).
- F1, F2, F4, F5 (not evaluated in v2.0.0).
- Machine-checked proofs of P1 and P2.

## [1.0.0] — 2026-11-10

**Formal Architecture Proposal.**

- 33-page paper published on Zenodo and Figshare.
- OSF Preregistration for v2.0.0 evaluation plan.
- 5 failure conditions (F1–F5), 6 requirements (R1–R6).
- 4 formal definitions, 2 propositions (proof sketches).
- 5 identity layers (L1–L5).
- 9 metrics, 5 baselines, 6 scenarios, 7 threats, 20 open questions.

## [0.1.0] — 2026-11-09

**Architectural Hypothesis (original draft).**

- Initial falsification-first methodology.
- Draft P1 and P2.
