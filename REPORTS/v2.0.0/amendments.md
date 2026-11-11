# AetherIdentity v2.0.0 — Amendments

This file records any amendment to the decisions made in `SPECIFICATION.md`,
`INVARIANTS.md`, or the OSF preregistration.

## Format

For each amendment:

- **Date:** YYYY-MM-DD
- **Affected document:** SPECIFICATION.md / INVARIANTS.md / OSF
- **Affected decision:** D-S / D-T / D-G / O1–O7 / other
- **Reason:** why the amendment is needed
- **Change:** what changes
- **Impact:** which phases are affected
- **Approved by:** the author

## Entries

### A1 — Partial execution of the OSF preregistration

- **Date:** 2026-11-11
- **Affected document:** OSF preregistration (`10.17605/OSF.IO/B6AEN`)
- **Affected decision:** the full evaluation protocol (S1–S6, M1–M9, B1–B5)
- **Reason:** v2.0.0 is a reference implementation, not a full deployment. Four
  scenarios (S2–S5) require an adversarial model, concurrency, churn, and a
  ground-truth Sybil model that are out of scope for v2.0.0.
- **Change:** only S1 and S6 are executed. The results are reported in
  `REPORTS/v2.0.0/evaluation_report.md`. The remaining scenarios are reported
  as **deferred**, not as **passing**.
- **Impact:** Phase 6. F1, F2, F4, and F5 are **not** evaluated in v2.0.0.
  F3 is reported as **inconclusive**.
- **Approved by:** the author.
