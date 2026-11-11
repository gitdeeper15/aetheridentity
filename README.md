# 🛡️ AetherIdentity v2.0.0

### A Falsification-First Investigation of Decentralized Agent Identity in the Aether Family

*Identity Proof, Continuity, Reputation, Sybil Resistance, and Delegation in Multi-Agent Software Ecosystems*

---

<!-- Core -->
[![DOI Zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.24102739.svg)](https://doi.org/10.5281/zenodo.24102739)
[![DOI Figshare](https://img.shields.io/badge/DOI%20Figshare-10.6084%2Fm9.figshare.34981891-blue)](https://doi.org/10.6084/m9.figshare.34981891)
[![OSF Preregistration](https://img.shields.io/badge/OSF-Preregistered-blue?logo=osf&logoColor=white)](https://doi.org/10.17605/OSF.IO/B6AEN)
[![License: MIT + CC-BY-4.0](https://img.shields.io/badge/License-MIT%20%2B%20CC--BY--4.0-crimson.svg)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0003--8903--0029-a6ce39)](https://orcid.org/0009-0003-8903-0029)

<!-- Status -->
[![Status](https://img.shields.io/badge/Status-Experimental%20Reference%20Implementation-blue)](https://doi.org/10.5281/zenodo.24102739)
[![Version](https://img.shields.io/badge/Version-v2.0.0-green)](https://doi.org/10.5281/zenodo.24102739)
[![Tests](https://img.shields.io/badge/Tests-35%20passed-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/Coverage-93%25-brightgreen)](ANALYSIS/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)

<!-- Family -->
[![Aether Family](https://img.shields.io/badge/Aether%20Family-8%20dimensions%20(candidate)-purple)](https://aetheridentity.netlify.app)
[![Pages](https://img.shields.io/badge/Pages-33-blue)](paper/)
[![References](https://img.shields.io/badge/References-29-blue)](paper/)

<!-- Repositories -->
[![GitHub](https://img.shields.io/badge/GitHub-gitdeeper15%2Faetheridentity-181717?logo=github&logoColor=white)](https://github.com/gitdeeper15/aetheridentity)
[![GitLab](https://img.shields.io/badge/GitLab-gitdeeper15%2Faetheridentity-FC6D26?logo=gitlab&logoColor=white)](https://gitlab.com/gitdeeper15/aetheridentity)
[![Codeberg](https://img.shields.io/badge/Codeberg-gitdeeper15%2Faetheridentity-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/gitdeeper15/aetheridentity)
[![Bitbucket](https://img.shields.io/badge/Bitbucket-gitdeeper15%2Faetheridentity-0052CC?logo=bitbucket&logoColor=white)](https://bitbucket.org/gitdeeper15/aetheridentity)

<!-- Publication -->
[![Paper](https://img.shields.io/badge/Paper-Zenodo-blue)](https://doi.org/10.5281/zenodo.24102739)
[![Website](https://img.shields.io/badge/Website-aetheridentity.netlify.app-00C7B7?logo=netlify&logoColor=white)](https://aetheridentity.netlify.app)

---

> *"AetherIdentity is a candidate, not a result."*

> *"Not falsified is a weaker status than confirmed."*

---

## Table of Contents

- [Overview](#overview)
- [Version series](#version-series)
- [What v2.0.0 supports](#what-v200-supports)
- [Test results](#test-results)
- [Experimental results](#experimental-results)
- [What v2.0.0 does not claim](#what-v200-does-not-claim)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Reproduction](#reproduction)
- [Citation](#citation)
- [Author](#-author)
- [License](#️-license)

---

## Overview

**AetherIdentity** is the **eighth functional dimension (candidate, provisional)** of the Aether family — a formal architecture for identity proof, continuity, reputation, Sybil resistance, and delegation in multi-agent software ecosystems.

The Aether family currently comprises seven foundational dimensions (AetherGit, AetherFlow, AetherProof, AetherMesh, AetherGovern, AetherRuntime, AetherOrchestrate). All rely on a notion of *who acts*, but none treats identity itself.

The framework investigates whether those five concerns amount to a genuine gap that justifies an eighth dimension, or are an artifact of how the existing dimensions were scoped.

---

## Version series

| Version | Status | Artifact |
|---|---|---|
| **v0.1.0** | Architectural Hypothesis | Original draft |
| **v1.0.0** | Formal Architecture Proposal | 33-page paper, published on Zenodo and Figshare |
| **v2.0.0** | Experimental Reference Implementation | Code, tests, experiments, report |

**The paper (v1.0.0) is not modified by v2.0.0.** v2.0.0 implements it, and reports where it cannot be implemented.

---

## What v2.0.0 supports

| Component | Status |
|---|---|
| L1 — Identity | ✅ Implemented |
| L2 — Continuity | ✅ Implemented |
| L3 — Reputation | ✅ Implemented |
| L4 — Sybil resistance | ✅ Implemented |
| L5 — Delegation | ✅ Implemented |
| Simulator | ✅ Implemented |
| Signer interface | ✅ Implemented |
| Record types | ✅ Implemented |

**Not implemented** (out of scope for v2.0.0):
- Network transport, consensus.
- AetherMesh integration (optional, S7).
- Fork resolution.
- Recovery after total key loss.
- Single-instance enforcement.
- Byzantine behavior.

See `SPECIFICATION.md` §11.

---

## Test results

| Metric | Value |
|---|---|
| Tests collected | 35 |
| Tests passed | 35 |
| Tests failed | 0 |
| Coverage | **93%** |

All 12 core invariants (I1–I12) are covered. See `REPORTS/v2.0.0/test_report.md`.

---

## Experimental results

| Scenario | Purpose | Result |
|---|---|---|
| **S1 — Bootstrap** | Test P2 (irreducible trust anchor) | **P2 not falsified** (bootstrap requires an anchor) |
| **S6 — Governance overlap** | Test F3 (boundary with governance) | **F3 inconclusive** (fragile: holds in some uses, fails in others) |

Four scenarios (S2–S5) are **deferred** and reported as such. See `REPORTS/v2.0.0/evaluation_report.md`.

---

## What v2.0.0 does not claim

- It does not claim that AetherIdentity is confirmed.
- It does not claim that F1–F5 are "not falsified".
- It does not claim that P1–P2 are proven.
- It does not claim that the architecture is production-ready.
- It does not claim that the simulator is representative of real deployments.

This is a **research artifact**, not a product.

---

## Project Structure

```text
AetherIdentity/
├── README.md
├── SPECIFICATION.md
├── INVARIANTS.md
├── TESTS.md
├── ROADMAP_v2.md
├── pyproject.toml
├── src/
│   └── aetheridentity/
│       ├── __init__.py
│       ├── records.py
│       ├── signer.py
│       ├── simulator.py
│       ├── identity.py
│       ├── continuity.py
│       ├── reputation.py
│       ├── sybil.py
│       └── delegation.py
├── tests/
│   ├── conftest.py
│   ├── test_smoke.py
│   ├── test_continuity.py
│   ├── test_reputation.py
│   ├── test_sybil.py
│   └── test_delegation.py
├── experiments/
│   ├── S1_bootstrap/
│   └── S6_governance_overlap/
├── DATA/
│   └── synthetic/
├── ANALYSIS/
│   └── coverage.json
├── REPORTS/
│   └── v2.0.0/
├── RELEASE/
│   └── RELEASE.md
├── docs/
│   └── figures/
└── paper/
    └── AetherIdentity_Research_Paper.pdf
```

---

Installation

```bash
# From source (development)
git clone https://github.com/gitdeeper15/aetheridentity.git
cd aetheridentity
pip install -e ".[dev]"

# Run tests
pytest

# Run experiments
python experiments/S1_bootstrap/run.py
python experiments/S6_governance_overlap/run.py
```

Requires Python 3.10+. Runtime dependency: cryptography >= 41.0.

---

Reproduction

```bash
# Full test run with coverage
pytest tests/ -v --cov=src/aetheridentity --cov-report=term-missing

# S1 — Bootstrap (P2)
python experiments/S1_bootstrap/run.py
cat experiments/S1_bootstrap/results.json

# S6 — Governance overlap (F3)
python experiments/S6_governance_overlap/run.py
cat experiments/S6_governance_overlap/results.json
```

The expected output matches REPORTS/v2.0.0/test_report.md and REPORTS/v2.0.0/evaluation_report.md.

---

Citation

Paper — AetherIdentity v1.0.0 (Zenodo)

https://zenodo.org/badge/DOI/10.5281/zenodo.24102739.svg

```bibtex
@techreport{baladi2026aetheridentity,
  author       = {Baladi, Samir},
  title        = {AetherIdentity: A Falsification-First Investigation of
                  Decentralized Agent Identity in the Aether Family},
  institution  = {Ronin Institute / Rite of Renaissance},
  type         = {Research Paper},
  year         = {2026},
  month        = {November},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.24102739},
  url          = {https://doi.org/10.5281/zenodo.24102739},
  note         = {Formal Architecture Proposal --- No implementation claimed.}
}
```

Software — AetherIdentity v2.0.0

```bibtex
@software{baladi2026aetheridentity_v2,
  author       = {Baladi, Samir},
  title        = {{AetherIdentity} v2.0.0: Reference Implementation of the
                  Falsification-First Identity Architecture},
  year         = {2026},
  month        = {November},
  version      = {2.0.0},
  doi          = {10.5281/zenodo.24102739},
  url          = {https://doi.org/10.5281/zenodo.24102739},
  note         = {Reference implementation. Paper: v1.0.0.}
}
```

OSF Preregistration

https://img.shields.io/badge/OSF-Preregistered-blue?logo=osf&logoColor=white

```bibtex
@misc{baladi2026aetheridentity_osf,
  author       = {Baladi, Samir},
  title        = {{AetherIdentity: A Falsification-First Investigation of
                  Decentralized Agent Identity in the Aether Family}},
  year         = {2026},
  month        = nov,
  day          = {11},
  publisher    = {OSF},
  doi          = {10.17605/OSF.IO/B6AEN},
  url          = {https://doi.org/10.17605/OSF.IO/B6AEN},
  note         = {OSF Preregistration for the v2.0.0 evaluation plan.
                  Associated project: https://osf.io/5y783}
}
```

Related Aether Records

Dimension DOI
AetherGit 10.5281/zenodo.23976986
AetherFlow 10.5281/zenodo.23979129
AetherProof 10.5281/zenodo.24013124
AetherMesh 10.5281/zenodo.24038038
AetherGovern 10.5281/zenodo.24054524
AetherRuntime 10.5281/zenodo.24078477
AetherOrchestrate 10.5281/zenodo.24095399

---

👤 Author

Samir Baladi
Interdisciplinary AI Researcher — Ronin Institute / Rite of Renaissance

 
Research Area Distributed Systems / Security / Multi-Agent Systems
Research Domain Identity, Continuity, Reputation, Sybil Resistance, Delegation
Research Type Formal Architecture Proposal + Reference Implementation
📧 Email gitdeeper@gmail.com
🔗 ORCID 0009-0003-8903-0029
🐙 GitHub gitdeeper15/aetheridentity
🦊 GitLab gitlab.com/gitdeeper15/aetheridentity
🟦 Codeberg codeberg.org/gitdeeper15/aetheridentity
🪣 Bitbucket bitbucket.org/gitdeeper15/aetheridentity
🌐 Official Site aetheridentity.netlify.app

---

⚖️ License

Scope License
Code MIT License — Copyright © 2026 Samir Baladi
Documentation, manuscript, and figures CC-BY-4.0

<details>
<summary><b>MIT License — full text</b></summary>

```text
MIT License

Copyright (c) 2026 Samir Baladi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

</details>

---

AetherIdentity v2.0.0 — Experimental Reference Implementation
© 2026 Samir Baladi — Ronin Institute / Rite of Renaissance — MIT (code) + CC-BY-4.0 (docs)
Zenodo: 10.5281/zenodo.24102739 | Figshare: 10.6084/m9.figshare.34981891 | OSF: 10.17605/OSF.IO/B6AEN | Website: aetheridentity.netlify.app
