# AetherIdentity — Gap Analysis

**Version:** 0.1.0
**Status:** Analysis derived from the paper. Not an empirical result.

---

## 1. The Gap Being Investigated

The Aether family comprises seven preprints on how agent-generated software
changes are stored, integrated and verified, specified and evidenced,
synchronized, authorized, monitored, and orchestrated. All of them rely on a
notion of *who acts*, but none treats identity itself.

The gap is narrow: whether identity, continuity, reputation, Sybil resistance,
and delegation can be specified over replicated, causally ordered state, so
that the parts that need no agreement are separated from the parts that do,
and the irreducible anchor is named.

It is a gap in **specification and scoping**, not a claim that existing
identity mechanisms are inadequate.

---

## 2. Five Observations About the Existing Records

These are statements about the records as the author reads them. Each can be
checked against the preprints.

| # | Observation |
|:-:|---|
| 1 | Identity is used everywhere and specified nowhere. AetherGit assumes signed changesets with author keys; AetherMesh's admission includes signature checks; AetherGovern's authority chains name principals; AetherRuntime and AetherOrchestrate records are signed by agents. None specifies how an identity is created, rotated, or ended. |
| 2 | Continuity is not addressed. A key rotation, a migration, or a restart appears in no preprint as a first-class event; an agent that changes its key is, by the existing records, a different principal. |
| 3 | Reputation is not aggregated. AetherRuntime records signed observations; AetherOrchestrate records declared capabilities. Neither aggregates observations into a reputation or checks that declared capabilities are truthful. |
| 4 | Sybil resistance is deferred. AetherRuntime and AetherOrchestrate both rely on committees of distinct agents and both list Sybil-resistant sampling as an open question. |
| 5 | Delegation overlaps with governance. AetherGovern provides authority chains and revocation. Whether these already cover delegation of scoped authority between identities is not settled by the records. |

---

## 3. What Each Literature Leaves Open

| Literature | What it supplies | What remains open |
|---|---|---|
| Decentralized identity and PKI | Identifiers, documents, resolution, self-certifying IDs, compact signatures | Key change and recovery; reputation; Sybil resistance; specification over replicated, causally ordered state |
| Reputation and trust | Aggregation schemes, trust computation | Deterministic, bit-for-bit reproducible scores over replicated state; dependence on a trust anchor |
| Sybil resistance | Cost, attestation, social-graph bounds | Fit for agent populations; the difference between many agents and many *posing as independent* identities |
| Delegation and capabilities | Attenuation, chained caveats, public-key tokens | Revocation in a replicated, partitionable system; identity of the root |

---

## 4. Assessment Against the Failure Conditions

| ID | Claim under test | Status | Reservation |
|:-:|---|:-:|---|
| F1 | Non-redundancy | Not falsified | Identity lifecycle missing; a bounded extension of AetherGovern might absorb R1, R2, R5 |
| F2 | Orthogonality to verification | Not falsified (narrowly) | Artifact checks fold into verification; aggregates, Sybil claims, and the anchor do not |
| F3 | Boundary with governance | Not falsified | **Most fragile:** delegation and revocation overlap; the anchor may be governance's root |
| F4 | Decentralizability | Not falsified (with residuals) | Anchor, Sybil assumptions, total key loss, cloning, and the revocation window cannot be removed |
| F5 | Observable benefit | **Untested** | Requires an experiment; scenario design by the proposer is circular |

---

## 5. What Would Falsify the Candidate

- **F1 falsified:** every requirement R1–R6 is met by the existing mechanisms,
  or by a bounded extension of exactly one existing dimension.
- **F2 falsified:** every identity decision and every trust anchor can be
  encoded as a verified claim.
- **F3 falsified:** identity reduces to governance plus conventional
  verification.
- **F4 falsified:** any design preserving the required properties needs a
  central authority or strong consistency.
- **F5 falsified:** no scenario class can be built in which the best existing
  baseline fails and AetherIdentity succeeds.

A negative answer on any one is sufficient to reject the candidate as a
separate dimension, though it may survive as a feature of another.

---

## 6. What the Paper Does Not Claim

- That the architecture works, performs, or scales.
- That the candidate is necessary.
- That Sybil attacks can be detected.
- That any table in the paper is empirical.
- Any causal effect of identity mechanisms on outcomes.

---

## 7. Recommended Next Steps

1. Independent review of the F1–F4 assessment, especially F3.
2. Joint treatment of the revocation and coordination windows shared across
   four Aether preprints, and of the trust anchor shared with AetherGovern.
3. Systematic review of applied identity systems.
4. Pre-registered simulation study (Section 8 of the paper).
5. Machine-checking of P1 and P2, if the candidate survives.
