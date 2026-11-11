# Contributing to AetherIdentity

**Status:** v2.0.0 is an experimental reference implementation. It is not a
production system. The paper (v1.0.0) is the authoritative hypothesis record.

Contributions at this stage take two forms:
- Review and correction of the paper (v1.0.0).
- Review and correction of the reference implementation (v2.0.0).

---

## What is welcome

**For the paper (v1.0.0):**
- Independent review of F1–F4. The failure conditions are the author's own,
  and independent assessment is the most useful next step.
- Literature pointers.
- Bibliographic corrections.
- Errata.

**For the implementation (v2.0.0):**
- Bug reports (with a minimal reproduction).
- Coverage improvements (currently 93%; the uncovered lines are edge cases).
- New tests for the deferred scenarios (S2–S5).
- Extensions to the simulator (concurrency, causal delivery) — documented as
  out of scope in v2.0.0.

## What is not applicable at this stage

- Production deployment reports (none exist).
- Performance benchmarks (none have been run).
- AetherMesh integration (out of scope for v2.0.0).
- Fork resolution, recovery, single-instance enforcement (out of scope).

## How to contribute

For the paper: open an issue on the repository and describe:
1. The section of the paper affected.
2. What you believe is incorrect or missing.
3. A reference or argument supporting your view.

For the implementation: open an issue or pull request and describe:
1. The module affected.
2. The test that demonstrates the problem.
3. The proposed change.

## What to expect

The paper is not peer reviewed. The implementation is a research artifact,
not a product. The author will review issues in good faith, but no timeline is
promised.

## Code of conduct

Be specific, be charitable, and cite evidence. Disagreement about the
architecture or the implementation is welcome; disagreement about the author
is not.
