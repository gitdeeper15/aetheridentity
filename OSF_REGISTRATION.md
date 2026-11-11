# AetherIdentity: A Falsification-First Investigation of Decentralized Agent Identity in the Aether Family

---

**Registration DOI:** [10.17605/OSF.IO/B6AEN](https://doi.org/10.17605/OSF.IO/B6AEN)
**Registration Type:** OSF Preregistration
**Registry:** OSF Registries
**Date Created:** Nov 11, 2026, 11:19 AM
**Date Registered:** Nov 11, 2026, 11:19 AM
**Associated Project:** [https://osf.io/5y783](https://osf.io/5y783)
**Internet Archive:** [https://archive.org/details/osf-registrations-b6aen-v1](https://archive.org/details/osf-registrations-b6aen-v1)
**License:** CC-BY Attribution 4.0 International
**Contributor:** Samir Baladi

---

## Data / Analytic Code / Materials / Papers / Supplements

The following files were attached to this registration:

**Papers:**
- `AetherIdentity_Research_Paper.pdf` (v0.1.0, 33 pages)
- `README.md`

**Note:** No implementation, test, or experiment is attached, because none exists. The v0.1.0 preprint is a formal architecture proposal.

---

## Overview

### Research questions or hypotheses

This registration pre-specifies the evaluation plan for AetherIdentity v2.0.0, a future reference implementation of the identity architecture described in the v0.1.0 preprint (Zenodo: 10.5281/zenodo.24102739; Figshare: 10.6084/m9.figshare.34981891). No implementation, test, or experiment has been executed.

The registration fixes, before any experiment is run, the following questions:

**H1. Identity issuance accuracy (M1):** Does AetherIdentity issue inception records that verify, with recomputed identifiers matching, at a rate distinguishable from the no-identity-layer baseline (B1)?

**H2. Continuity preservation (M2):** After rotation, restart, or migration, does the identifier and its history resolve unchanged at a rate distinguishable from B1 and from the web-of-trust baseline (B3)?

**H3. Reputation accuracy (M3):** Do computed reputation scores agree with ground-truth behavior of injected agents at a rank correlation distinguishable from B1?

**H4. Sybil detection rate (M4):** Are injected Sybil clusters flagged at a stated error rate, with a reported false-positive rate on honest multi-agent operators, distinguishable from B1 and B3?

**H5. Delegation scope correctness (M5):** Are actions authorized exactly when inside the effective scope, with no over- or under-authorization, distinguishable from B3 and B5?

**H6. Convergence preservation (M9):** Is M9 exactly zero across all runs (pass/fail invariant), as required for P1?

**H7. Observable benefit (F5):** Is there any scenario class in which the best existing baseline is non-inferior to AetherIdentity on the primary metrics (M2, M4, M5, M8)? If yes, F5 is falsified.

Each hypothesis is stated so that a negative result falsifies it. No hypothesis is treated as confirmed; "not falsified" is weaker than "confirmed".

### Foreknowledge of data or evidence

Data does not yet exist. No part of the data that will be used for this analysis plan exists, and no part will be generated until after this plan is registered.

### Explanation of foreknowledge and managing unintended influences

The v0.1.0 preprint specifies the evaluation design (Section 8) but reports no data. No experiment has been run, and the testbed does not exist. The analysis plan registered here is the plan stated in the preprint, fixed before any implementation is built. The only prior knowledge is the design itself, which is public in the preprint; no outcome data exist.

To reduce risk of unintended influence, this registration fixes: the nine metrics (M1–M9), the five baselines (B1–B5), the six scenarios (S1–S6), the eight-step protocol, and the decision rule (F5 is falsified if, for every scenario, some baseline is non-inferior on the primary metrics with a pre-fixed effect-size margin, or if M9 is ever non-zero). The pre-registration is published before the implementation is written.

---

## Research Design

### Study type

**Simulation study:** Using existing or synthetic data to assess performance of a model, mimic operation of an existing or proposed system, or predict possible outcomes in a controlled context.

### Intention for causal interpretation

**No causal relationship inferred:** This study is not intended to inform a causal relationship.

### Blinding of experimental treatments

No blinding is involved.

### Additional blinding during research or analysis

No data.

### Study design

Simulation study comparing AetherIdentity against five baselines (B1–B5) across six scenarios (S1–S6), using a simulated network of controllable size, latency, loss, Byzantine fraction, and churn.

**Design:** repeated measures across scenarios. Each scenario is executed once per design per seed, with the same recorded workload and the same seeds for all designs (paired comparison at the seed level). The unit of analysis is the scenario–seed pair, not the individual agent.

**Conditions:** six designs (AetherIdentity + B1–B5) × six scenarios (S1–S6) × N seeds (N fixed in advance; N reported). Each design is run on the same workload per seed to allow paired comparison.

**Outcomes:** nine metrics (M1–M9), with M9 treated as a pass/fail invariant (must be zero) and M4 reported together with its false-positive rate on honest multi-agent operators.

**Baselines:** B1 = no identity layer; B2 = centralized certificate authority; B3 = web of trust; B4 = DID-based ledger registry; B5 = composition of existing components.

**Scenarios:** S1 = key compromise followed by rotation; S2 = Sybil flood; S3 = partition then merge; S4 = migration storm; S5 = whitewashing; S6 = delegation abuse.

No randomization of treatments is performed, because the designs are not administered to human subjects; randomness enters only through (i) the seeds, (ii) the synthetic workload generation, and (iii) the injected fault schedule. Seeds are fixed in advance and reported.

**Attached files:** `AetherIdentity_Research_Paper.pdf`, `README.md`

### Randomization

Not applicable to human-subject randomization. Seeds are fixed in advance, reported, and reused identically across all designs for each scenario, so that differences between designs cannot be attributed to seed variation. No adaptive or stratified randomization is used.

---

## Sampling

### Data collection procedures

The study generates no human-subjects data. All data are synthetic, produced by a simulated network of controllable size, latency, loss, Byzantine fraction, and churn. The sampling strategy is defined by the simulation, not by recruitment.

**Population and sampling frame.** The population is the set of agents and identities admitted to the simulated network. The sampling frame is the simulator's admission function, which admits inception records, rotation records, delegation records, revocation records, reputation records, and Sybil claims according to the deterministic rules of the paper. No human population is sampled.

**Recruiting method.** Not applicable. Agents are instantiated by the simulator with roles defined in the scenario (honest, faulty, adversarial, Sybil cluster, whitewashing, delegation abuser).

**Inclusion and exclusion criteria.** An identity is included if its inception record is admitted and, where applicable, if it has standing under the simulated sponsorship rule. It is excluded if its record fails verification, if it is revoked, or if it is outside the scenario's scope.

**Source or location.** The simulator runs on a controlled testbed of N nodes; the exact topology, latency distribution, loss rate, and Byzantine fraction are fixed per scenario and reported.

**Expected duration.** Each scenario–design–seed combination is a single run. The total number of runs is |scenarios| × |designs| × |seeds|, fixed in advance.

**Data preparation.** Telemetry, identity-layer records, and ground-truth labels (for injected agents) are logged per run. Logs are parsed by a fixed script; the parsing rules are fixed before the first run.

### Data collection procedures - File upload

No files selected.

### Sample size

Unit of analysis: the scenario–seed pair, per design.

Sample size per cell: one run per (scenario, design, seed) combination.

Total runs: |scenarios| × |designs| × |seeds| = 6 × 6 × N seeds, where N is fixed in advance and reported.

**Levels.** The design has two levels:
- Level 1 (between): scenario (S1–S6) and design (AetherIdentity, B1–B5).
- Level 2 (within): seed, paired across designs for the same scenario.

**Nesting.** Seeds are nested within scenario and paired across designs, so each seed produces six runs (one per design) for the same scenario. This yields a paired comparison at the seed level.

Sample size per scenario: 6 designs × N seeds.
Sample size per design: 6 scenarios × N seeds.

N is fixed in advance. A power analysis is not performed, because the study is a simulation and the primary outcomes are not population parameters. Instead, N is chosen so that the paired comparison has enough seeds to report distributions and effect sizes, not a single point estimate. N is reported with every result.

### Sample size rationale

No power analysis is performed, because the study is a simulation and the outcomes are not population parameters. The sample size is chosen to satisfy three constraints:

1. **Paired comparison:** N seeds per scenario, reused identically across designs, so that differences between designs cannot be attributed to seed variation.
2. **Distribution reporting:** N large enough to report distributions, effect sizes, and intervals, not single runs.
3. **Pre-specification:** N is fixed before the first run and reported with every result; it is not adjusted after observing outcomes.

The exact value of N is fixed in the pre-registered protocol (Section 8 of the preprint) and reported in every result table. No adaptive sample-size rule is used.

### Starting and stopping rules

**Starting rule.** Data collection begins only after this registration is published and the implementation is frozen at a tagged version. The first run is the first scenario–design–seed combination in the pre-specified order. No pilot run is used to adjust the design; if a pilot is run, it is reported separately and not included in the primary analysis.

**Stopping rule.** Data collection ends when all pre-specified runs are complete: |scenarios| × |designs| × |seeds|. No optional stopping is allowed. If a run fails for technical reasons, it is re-run with the same seed and the failure is reported. If a scenario cannot be executed, it is reported as missing, and the primary analysis is run both with and without it.

No interim analysis is planned. No run is added or removed after observing outcomes.

---

## Variables

### Manipulated variables

Six designs (between-condition):
- AetherIdentity (the candidate architecture).
- B1: no identity layer (bare signing keys as principals).
- B2: centralized identity provider and certificate authority (X.509 style).
- B3: web of trust.
- B4: DID-based registry anchored in a ledger.
- B5: composition of existing components (key-derived DIDs + EigenTrust-style reputation + Macaroon/Biscuit-style delegation).

Six scenarios (between-condition):
- S1: key compromise followed by rotation.
- S2: Sybil flood.
- S3: partition then merge with conflicting rotations or revocations.
- S4: migration storm.
- S5: whitewashing.
- S6: delegation abuse.

No randomization of treatments is performed. The designs are not administered to human subjects; the only randomness is in seeds, synthetic workload generation, and the injected fault schedule. Seeds are fixed in advance and reused identically across designs for each scenario.

### Measured variables

Nine outcome metrics (M1–M9), as defined in Section 8 of the preprint:

- **M1 — Identity issuance accuracy:** fraction of issued inception records that verify and whose recomputed identifier matches. Higher is better.
- **M2 — Continuity preservation:** fraction of rotations, restarts, and migrations after which the identifier and its history resolve unchanged. Higher is better.
- **M3 — Reputation accuracy:** agreement (e.g., rank correlation) between computed scores and ground-truth behavior of injected agents. Higher is better.
- **M4 — Sybil detection rate:** fraction of injected Sybil clusters flagged, reported together with the false-positive rate on honest multi-agent operators. Higher is better for detection; lower is better for false positives.
- **M5 — Delegation scope correctness:** fraction of actions authorized exactly when inside the effective scope (no over- or under-authorization). Higher is better.
- **M6 — Identity verification latency:** time to verify an identity or a chain of given length at a node. Lower is better.
- **M7 — Identity storage overhead:** bytes of identity-layer state per identity and per record. Lower is better.
- **M8 — Revocation propagation latency:** time from revocation record creation to its effect at a quantile q of honest nodes. Lower is better.
- **M9 — Convergence preservation:** count of runs in which honest nodes hold different admitted sets or different derived views after delivery. Must be zero (pass/fail invariant).

**Covariates and subsetting variables:** scenario (S1–S6), design (AetherIdentity, B1–B5), seed, network size, latency distribution parameters, loss rate, Byzantine fraction, churn rate, scenario-specific parameters (e.g., number of injected Sybil clusters, number of compromised keys).

No human-subjects variables are measured.

### Measured variables - File upload

No files selected.

### Indices

No composite indices are constructed. Each metric (M1–M9) is reported separately, as defined in the preprint. Two derived quantities are reported alongside their base metric:

- **M4 false-positive rate:** fraction of honest multi-agent operators flagged as Sybil, reported together with M4. A detector that flags every identity would score perfectly on M4 alone; the false-positive rate prevents this.
- **M9 pass/fail:** M9 is treated as an invariant, not a quantity. A run with non-zero M9 is reported as a failure of convergence preservation and takes precedence over every other metric.

No aggregation across metrics is performed. No weighted score is constructed. No index is used to rank designs.

### Indices - File upload

No files selected.

---

## Analysis Plan

### Statistical models

The study is a simulation with a repeated-measures design (scenario × design × seed). No human-subjects statistical model is used. The analysis proceeds in three layers:

**Layer 1 — Paired comparison per scenario.** For each scenario S and metric M, the paired difference between AetherIdentity and each baseline B is computed per seed: d_S,B,M(seed) = M(AetherIdentity, S, seed) − M(B, S, seed). The paired difference is reported as a distribution across seeds (mean, median, 95% interval, effect size), not as a single point estimate.

**Layer 2 — Non-inferiority test (F5 decision rule).** For each scenario S and each baseline B, AetherIdentity is declared non-inferior if the paired difference on the primary metrics (M2, M4, M5, M8) is within a pre-fixed effect-size margin δ. F5 is falsified if, for every scenario, some baseline is non-inferior on the primary metrics, or if M9 is ever non-zero.

**Layer 3 — Invariant check (M9).** M9 is a pass/fail invariant. A single non-zero M9 in any run is reported as a failure of convergence preservation and takes precedence over every other metric.

No ANOVA, regression, SEM, or Bayesian model is used. No subgroup analysis, pairwise contrast, or omnibus test is planned. No positive or negative control is used beyond the baselines B1–B5. No manipulation check is used, because there are no human subjects.

**Assumption checks.** The paired differences are reported with distributional summaries, not p-values, because the study is a simulation and the outcomes are not population parameters. If a paired difference distribution is degenerate (all zeros), it is reported as such.

### Statistical models - File upload

No files selected.

### Transformations

No transformation, centering, or recoding is performed on the outcome metrics (M1–M9). They are reported in their native units.

Categorical variables are coded as follows:
- Scenario: nominal, six levels (S1–S6).
- Design: nominal, six levels (AetherIdentity, B1–B5).
- Seed: integer, fixed in advance, reused identically across designs.

No derived score, no standardization, no log transform, no rank transform is applied. M9 is reported as a binary pass/fail, not as a continuous variable.

### Inference criteria

No p-values, Bayes factors, or model fit indices are used, because the study is a simulation and the outcomes are not population parameters.

**Inference criteria:**

1. **Paired difference distributions:** reported as mean, median, 95% interval (percentile bootstrap over seeds), and effect size (Cohen's d for paired samples). Intervals are reported, not used as decision thresholds.
2. **Non-inferiority margin δ:** fixed in advance, reported with every result. A baseline B is non-inferior to AetherIdentity on a primary metric if the 95% interval of the paired difference lies entirely within [−δ, +δ].
3. **F5 decision rule:** F5 is falsified if, for every scenario S, at least one baseline B is non-inferior to AetherIdentity on all primary metrics (M2, M4, M5, M8) simultaneously, or if M9 is ever non-zero. Otherwise F5 is "not falsified", never "confirmed".
4. **Multiple comparisons:** the non-inferiority test is applied per scenario × baseline × metric. No family-wise correction is applied, because the decision rule is conjunctive (all scenarios must fail for F5 to be falsified), not disjunctive. The number of comparisons is reported.
5. **One-tailed vs two-tailed:** non-inferiority is inherently one-tailed (the interval must lie within [−δ, +δ], which is a two-sided interval but a one-sided decision). Reported as such.

### Data inclusion and exclusion

**Inclusion criteria:**

1. A run is included if it completes without technical failure and its logs parse under the fixed parsing script.
2. A scenario–design–seed combination is included if all six designs produced a run for that combination. If one design failed for a seed, the seed is excluded from the paired comparison for that scenario, and the exclusion is reported.

**Exclusion criteria:**

1. Technical failures (simulator crash, log corruption) are excluded from the primary analysis and reported separately. Failed runs are re-run with the same seed; if the re-run also fails, the failure is reported and the run is excluded.
2. No outlier exclusion is applied. All completed runs are reported. If a run produces an extreme value, it is reported, not removed.
3. No subject exclusion is applied, because there are no human subjects.

No post-hoc exclusion is allowed. The exclusion rules are fixed before the first run and reported with every result.

### Missing data

No missing data is expected at the run level, because each run produces a complete log.

If a metric is undefined for a run (for example, M4 false-positive rate when no honest multi-agent operator is present in the scenario), the metric is reported as "not applicable" for that run and excluded from the aggregate for that metric. The exclusion is reported.

If a scenario cannot be executed, it is reported as missing, and the primary analysis is run both with and without it. The version with and without is reported.

No imputation is performed. No model is fit to incomplete data. No data is dropped silently.

### Other planned analysis

Secondary analyses, reported alongside the primary analysis but not used in the F5 decision:

1. **Per-seed trajectories:** for each scenario and design, the time series of M1–M8 over the simulation horizon. Reported as plots, not as a test.
2. **Sensitivity to N:** the primary analysis is repeated for N/2 seeds (first half) and N/2 seeds (second half), to check that the reported distributions are not driven by a small subset of seeds. Reported as a robustness check, not as a decision criterion.
3. **Sensitivity to δ:** the F5 decision rule is re-evaluated for δ/2 and 2δ, to check that the conclusion is not sensitive to the choice of margin. Reported as a robustness check, not as a decision criterion.
4. **Ablation:** each identity layer (L1–L5) is removed in turn, and the primary metrics are reported. This tests whether each layer is needed. Reported as exploratory, not as a confirmatory test.

No exploratory analysis is used to modify the primary analysis. All secondary analyses are reported, whether or not they support the candidate.

---

## Other

### Context and additional information

**Relation to the published preprint.** This registration is a pre-registered evaluation plan for AetherIdentity v2.0.0, a future reference implementation of the architecture specified in the v0.1.0 preprint. The preprint is published and citable:

- Zenodo: 10.5281/zenodo.24102739
- Figshare: 10.6084/m9.figshare.34981891

The preprint is a formal architecture proposal. It reports no implementation, test, or experiment. F1–F4 are not falsified by argument, each with a stated reservation; F5 is untested. "Not falsified" is weaker than "confirmed". No condition is confirmed.

**What this registration is not.** This registration is not a registration of the preprint. It is not a registration of results. It is a plan for a future evaluation, submitted before any implementation is built. OSF requires that registrations contain research plans, not papers or preprints; the preprint is therefore cited here but not registered.

**Why a pre-registration.** The preprint's Section 8 specifies an evaluation design (nine metrics M1–M9, five baselines B1–B5, six scenarios S1–S6, an eight-step protocol). That design was stated before any experiment, but it was not registered. This registration fixes the design before the first run, so that a future v2.0.0 evaluation cannot adjust the metrics, baselines, scenarios, or decision rule after observing outcomes.

**Known limitations carried into the plan.**

1. F3 is the most fragile failure condition: delegation (L5) overlaps strongly with AetherGovern's authority chains. The evaluation plan therefore includes B5 (composition of existing components) as the strongest baseline, and the non-inferiority test on M5 (delegation scope correctness) is the most likely to falsify the candidate.
2. M4 (Sybil detection rate) is reported with its false-positive rate on honest multi-agent operators. A detector that flags every identity would score perfectly on M4 alone.
3. M9 (convergence preservation) is a pass/fail invariant, not a quantity. A single non-zero M9 falsifies P1's claim that the identity layer preserves convergence.
4. The evaluation is a simulation, not a deployment. No real-world causal claim is made. The results will support statements about differences between designs in the simulated scenarios, not about deployment outcomes.
5. The author of the preprint is also the author of this plan, and will be the author of the implementation and the evaluation. Independent review is the most useful next step, and is listed as the first item in the preprint's future work.

**What would count as failure.** F5 is falsified if, for every scenario, some baseline is non-inferior to AetherIdentity on the primary metrics (M2, M4, M5, M8) with the pre-fixed effect-size margin δ, or if M9 is ever non-zero. If F5 is falsified, the candidate is rejected as a separate dimension, and the preprint's Section 4 (Failure Conditions) records the falsification.

**What would count as survival.** If F5 is not falsified, the candidate survives as a candidate, not as a confirmed dimension. "Not falsified" remains weaker than "confirmed" in every case.

**Materials.** The v0.1.0 preprint (PDF) and its README are attached to this registration. No implementation, test, or experiment is attached, because none exists.

---

## Metadata

### Contributors

Samir Baladi

### Resource type

No resource type

### Description

AetherIdentity is a candidate eighth functional dimension of the Aether family. It investigates whether identity proof, continuity, reputation, Sybil resistance, and delegation in multi-agent software ecosystems constitute a genuine gap not already covered by the seven existing dimensions. The method is falsification-first: five failure conditions (F1–F5) and six requirements (R1–R6) are stated before the candidate is described. No implementation, test, or experiment is reported. F1–F4 are not falsified by argument, each with a stated reservation; F5 is untested. AetherIdentity is a candidate, not a result.

### Registration Type

OSF Preregistration

### Registry

OSF Registries

### Associated project

https://osf.io/5y783

### Internet Archive

https://archive.org/details/osf-registrations-b6aen-v1

### Date Created

Nov 11, 2026, 11:19 AM

### Date registered

Nov 11, 2026, 11:19 AM

### Subjects

- Computer Sciences
- Physical Sciences and Mathematics

### Tags

- AetherIdentity
- decentralized identity
- evaluation plan
- pre-registration
- Sybil resistance

### Affiliated Institutions

No affiliated institutions

### Funder Names

No information

### Language

No language

### License

CC-By Attribution 4.0 International

### Registration DOI

10.17605/OSF.IO/B6AEN

---

## Citations

### APA

Baladi, S. (2026, November 11). AetherIdentity: A Falsification-First Investigation of Decentralized Agent Identity in the Aether Family. OSF. https://doi.org/10.17605/OSF.IO/B6AEN

### MLA

Baladi, Samir. "AetherIdentity: A Falsification-First Investigation of Decentralized Agent Identity in the Aether Family." OSF, 11 Nov. 2026. Web.

### Chicago

Baladi, Samir. 2026. "AetherIdentity: A Falsification-First Investigation of Decentralized Agent Identity in the Aether Family." OSF. November 11. doi:10.17605/OSF.IO/B6AEN.

### BibTeX

```bibtex
@misc{baladi2026aetheridentity_osf,
  author       = {Baladi, Samir},
  title        = {{AetherIdentity: A Falsification-First Investigation of Decentralized Agent Identity in the Aether Family}},
  year         = {2026},
  month        = nov,
  day          = {11},
  publisher    = {OSF},
  doi          = {10.17605/OSF.IO/B6AEN},
  url          = {https://doi.org/10.17605/OSF.IO/B6AEN},
  note         = {OSF Preregistration. Associated project: https://osf.io/5y783}
}
```

---

Source: Center for Open Science · OSF Registries
Retrieved: 2026-11-11
