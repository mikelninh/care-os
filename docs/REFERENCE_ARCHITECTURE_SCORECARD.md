# CareOS Reference Architecture Review Checklist

Baseline date: **2026-08-18**.

> Historical filename retained for stable links. This document no longer assigns a self-score; it records which proposal-level questions have reviewable evidence and which production questions remain external.

This checklist answers one narrow question:

> **Is the CareOS architecture package coherent enough to take into serious government, hospital-CIO, clinical-leadership and public-sector architecture discussions?**

It does **not** answer whether CareOS is production-approved for identifiable live patient data. That remains governed by G0–G9 and external evidence.

## Proposal-review evidence

| Dimension | Evidence state | Evidence |
|---|---|---|
| Clear product/system boundary | **DOCUMENTED** | `ARCHITECTURE_V2.md`, safety case |
| Federated national architecture | **DOCUMENTED** | `GOVERNMENT_REFERENCE_ARCHITECTURE.md` |
| Trust/data-flow boundaries | **DOCUMENTED** | `TRUST_AND_DATA_FLOW.md` |
| Deployment patterns | **DOCUMENTED** | `DEPLOYMENT_PATTERNS.md` |
| Clinical truth/provenance contract | **IMPLEMENTED + SYNTHETICALLY TESTED** | clinical truth/reconciliation code + tests |
| Security/identity/failure model | **IMPLEMENTED IN RESEARCH BOUNDARY** | agent/security code + threat/security docs |
| German/EU integration map | **DOCUMENTED / PARTIAL EVIDENCE** | `NATIONAL_INTEGRATION_MAP.md` |
| Technical documentation/conformity mapping | **DOCUMENTED** | `TECHNICAL_DOCUMENTATION_INDEX.md` |
| Durable architecture decisions | **DOCUMENTED** | `docs/adr/` |
| Machine-readable architecture invariants | **IMPLEMENTED + TESTED** | `architecture/reference-architecture.json` + tests |

### Proposal-level conclusion

The package is **ready for institutional critique and architecture discussion** because a reviewer can inspect the boundary, data/trust flows, failure semantics, deployment patterns, national alignment, machine-readable invariants and explicit limitations.

That is not a production-readiness claim.

## Production evidence still required

A live hospital deployment still requires evidence CareOS cannot self-generate:

- real provider IdP/context;
- real KIS/LIS integration;
- independent regulatory/classification review;
- hospital-specific Datenschutz/DSFA/AVV review where applicable;
- production KMS/audit/SIEM/backup/monitoring;
- independent penetration/security testing;
- target-environment resilience evidence;
- clinically useful recall/review burden;
- shadow/live evaluation;
- second-hospital repeatability.

`live_patient_data_allowed=false` remains the correct posture while those gates are incomplete.

## What to show each audience

### Clinical lead

1. synthetic demo;
2. 30-second product architecture;
3. one workflow hypothesis;
4. safety boundaries;
5. small read-only discovery ask.

Do not lead with national architecture.

### CIO / hospital architecture

- `ARCHITECTURE_V2.md`;
- `DEPLOYMENT_PATTERNS.md`;
- `TRUST_AND_DATA_FLOW.md`;
- `NATIONAL_INTEGRATION_MAP.md`;
- hospital assurance pack;
- current gate board.

### CISO / Datenschutz

- trust/data-flow document;
- threat model;
- access/audit/identity controls;
- deployment pattern;
- DSFA/AVV support material;
- explicit live-data blockers.

### Government / gematik / public-sector architecture

- `GOVERNMENT_REFERENCE_ARCHITECTURE.md` as front door;
- `ARCHITECTURE_V2.md` as canonical technical design;
- `NATIONAL_INTEGRATION_MAP.md` for alignment;
- ADRs for design decisions;
- technical-documentation index for assurance;
- production gates to make claim boundaries explicit.

## Recommended claim language

> **CareOS provides a proposal-ready federated reference architecture for a source-grounded clinical context layer above heterogeneous German healthcare systems. The architecture is available for institutional review; production deployment remains gated by real integration, independent assurance and clinical evidence.**

Do not say:

- “CareOS is production-ready in Germany.”
- “CareOS is DSGVO certified.”
- “CareOS is EHDS compliant.”
- “CareOS is medically certified.”
- “CareOS has solved hospital interoperability.”
- “CareOS can already use live patient data.”
