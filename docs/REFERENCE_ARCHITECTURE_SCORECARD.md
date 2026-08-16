# CareOS Reference Architecture Readiness Scorecard

Baseline date: **2026-08-16**.

This scorecard answers one narrow question:

> **Is the CareOS architecture package complete enough to take into serious government, hospital-CIO, clinical-leadership and public-sector architecture discussions?**

It does **not** answer whether CareOS is production-approved for identifiable live patient data. That remains governed separately by G0–G9.

## Score

# **10 / 10 — proposal/reference-architecture readiness**

The score is justified by documentation and reviewability, not by self-certification.

| Dimension | Score | Evidence |
|---|---:|---|
| Clear product/system boundary | 1/1 | `ARCHITECTURE_V2.md`, safety case |
| Federated national architecture | 1/1 | `GOVERNMENT_REFERENCE_ARCHITECTURE.md` |
| Trust/data-flow boundaries | 1/1 | `TRUST_AND_DATA_FLOW.md` |
| Deployment patterns | 1/1 | `DEPLOYMENT_PATTERNS.md` |
| Clinical truth/provenance contract | 1/1 | clinical truth code + Architecture V2 |
| Security/identity/failure model | 1/1 | Architecture V2 + threat/security docs |
| German/EU integration map | 1/1 | `NATIONAL_INTEGRATION_MAP.md` |
| Technical documentation/conformity mapping | 1/1 | `TECHNICAL_DOCUMENTATION_INDEX.md` |
| Durable architecture decisions | 1/1 | `docs/adr/` |
| Machine-readable + CI-enforced architecture invariants | 1/1 | `architecture/reference-architecture.json` + tests |

## Why this can be 10/10 while production gates are not PASS

There are two different maturity questions.

### A. Reference architecture readiness

Can a serious reviewer understand:

- what the system is;
- what it is not;
- where patient data lives;
- how it connects;
- who is trusted;
- how source truth is preserved;
- what happens on failure;
- how Germany/EU infrastructure fits;
- what deployment patterns exist;
- which decisions are fixed;
- which claims are explicitly not being made?

For CareOS, that package is now complete enough for proposal/review discussions.

### B. Production readiness

Can the system process identifiable patient data in a real hospital safely and legally?

That still requires evidence CareOS cannot self-generate:

- real provider IdP/context;
- real KIS/LIS integration;
- independent regulatory/classification review;
- hospital-specific Datenschutz approval/DSFA/AVV where applicable;
- production KMS/audit/SIEM/backup/monitoring;
- penetration test;
- target-environment resilience evidence;
- clinically useful G1 recall/review burden;
- shadow/live evaluation;
- second-hospital repeatability.

Therefore **reference architecture = 10/10** does not change `live_patient_data_allowed=false`.

## What to show each audience

### Chefarzt / clinical lead

Use:

1. synthetic demo;
2. 30-second product architecture;
3. one workflow hypothesis;
4. safety boundaries;
5. tiny read-only discovery ask.

Do not lead with national architecture.

### CIO / hospital architecture

Use:

- `ARCHITECTURE_V2.md`;
- `DEPLOYMENT_PATTERNS.md`;
- `TRUST_AND_DATA_FLOW.md`;
- `NATIONAL_INTEGRATION_MAP.md`;
- hospital assurance pack;
- current gate board.

### CISO / Datenschutz

Use:

- trust/data-flow document;
- threat model;
- access/audit/identity controls;
- deployment pattern;
- DSFA/AVV support material;
- explicit live-data blockers.

### Government / gematik / public-sector architecture

Use:

- `GOVERNMENT_REFERENCE_ARCHITECTURE.md` as front door;
- `ARCHITECTURE_V2.md` as canonical technical design;
- `NATIONAL_INTEGRATION_MAP.md` for alignment;
- ADRs for non-negotiable design choices;
- technical-documentation index for assurance;
- production gates to demonstrate non-hype discipline.

## Proposal claim language

Recommended:

> **CareOS provides a proposal-ready federated reference architecture for a source-grounded clinical context layer above heterogeneous German healthcare systems. The architecture package is complete enough for institutional review; production deployment remains gated by real integration, independent assurance and clinical evidence.**

Do not say:

- “CareOS is production-ready in Germany.”
- “CareOS is DSGVO certified.”
- “CareOS is EHDS compliant.”
- “CareOS is medically certified.”
- “CareOS has solved hospital interoperability.”
- “CareOS can already use live patient data.”
