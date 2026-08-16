# CareOS Production Readiness Gates

CareOS graduates by **evidence-backed gates, not version number**.

Machine-readable source: `GET /api/readiness/gates` in `app/readiness_gates.py`.

| Gate | Status | What still blocks PASS |
|---|---|---|
| G0 Scope & safety boundary | **EXTERNAL REVIEW** | Independent MDR/MDSW + clinical-safety review |
| G1 Clinical truth | **BLOCKED** | Replace/evaluate legacy document extractor, new untouched holdout, release-grade critical-miss results |
| G2 German interoperability | **PARTIAL** | Terminology coverage, version/incremental sync, real KIS/LIS/vendor sandbox |
| G3 Privacy & security | **PARTIAL** | Real hospital IdP/context, immutable audit, KMS/encryption, hospital DSFA/agreements, C5 evidence where applicable, pentest |
| G4 Production reliability | **PARTIAL** | Full failure injection, real-source freshness policies, backup/restore + measured RPO/RTO, monitoring/SLO exercise |
| G5 Regulatory & quality | **EXTERNAL REVIEW** | Formal qualification/classification, AI Act/EHDS assessment, reviewed risk/QMS lifecycle |
| G6 Invisible workflow integration | **PARTIAL** | Real KIS/portal context launcher, Citrix/VDI/managed-browser proof, measured no-copy/no-second-search workflow |
| G7 Hospital deployment kit | **PARTIAL** | Fill with one hospital's actual systems, contacts, approvals, network/security evidence and stop thresholds |
| G8 Repeatable deployment | **PARTIAL** | Hospital A + different Hospital B/vendor without a CareOS core fork |
| G9 National/EU scale | **BLOCKED** | Actual ePA/TI/KIM/ISiP/outpatient/EHDS paths and multi-site operating evidence |

## Evidence now implemented

### Clinical truth
- mandatory `ClinicalFact` / `TruthEnvelope` contract;
- exact source identity/version/time semantics where supplied;
- document/model outputs are **untrusted candidates** until exact source offsets/quotes are mechanically verified;
- cross-patient truth rejected;
- ambiguous/unknown facts routed to review;
- explicit governed contradiction rules do not silently choose a winning source.

### Interoperability
- real HAPI FHIR integration path;
- bounded same-origin FHIR Bundle pagination;
- cross-origin continuation, loops and silent max-page truncation fail closed;
- vendor-neutral `ConnectorReadResult = SourceState + TruthEnvelope` contract;
- pinned gematik reference validator **2.16.6** + ISiK5 plugin **1.0.4**, SHA-256 verified in CI;
- synthetic ISiK5 Patient validation workflow green.

### Security / privacy
- asymmetric OIDC JWT verifier with issuer/audience/expiry/signature checks;
- symmetric/`none` algorithms rejected for hospital OIDC;
- role/scope/treatment-context authorization policy;
- short-lived identity/organisation/patient-bound context-launch contract;
- break-glass requires reason and elevated audit semantics;
- secure read coordinator withholds patient truth on denial, source failure/staleness, patient mismatch or required audit failure;
- provider-data-plane privacy architecture, DSFA support and AVV requirements package.

### Reliability / operations
- explicit `current / stale / unavailable / unknown` source state;
- source outage cannot become a normal empty patient result;
- global and connector-specific runtime kill switch;
- deployment/rollback and incident-response runbooks;
- reliability/SLO framework;
- `CAREOS_DATA_MODE=live-readonly` **refuses application startup while G0–G5 are incomplete**;
- transactional/write-back mode is unsupported by release policy.

### Assurance / scale
- living safety case;
- risk register;
- safety-aware change control;
- hospital assurance-pack index;
- pilot measurement protocol;
- connector SDK contract;
- Germany/EU scale roadmap;
- external-review brief and dedicated GitHub issue.

## Live-data lock

Identifiable live patient data remains **locked** while any of G0–G5 is not `PASS`.

This is now enforced in code, not only documented.

A green unit test is not sufficient to pass an assurance gate. External-review and real-deployment gates require named qualified reviewers, real infrastructure and linked evidence.

## Immediate critical path

1. **G1:** implement/evaluate the replacement document extraction pipeline and create a new untouched holdout.
2. **G0/G5:** obtain independent clinical-safety + MDR/software-regulatory review.
3. **G2:** secure one real read-only KIS/LIS/vendor sandbox and complete terminology/synchronization semantics.
4. **G3:** connect a real hospital IdP/context source, immutable audit/KMS, complete hospital-specific privacy/security evidence, then external pentest.
5. **G4:** run failure injection, backup/restore and incident/rollback exercises in the target deployment.

Only then does a read-only live-data pilot become eligible for a go/no-go decision.
