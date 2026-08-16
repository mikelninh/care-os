# CareOS Production Readiness Gates

CareOS graduates by **evidence-backed gates, not version number**.

Machine-readable source: `GET /api/readiness/gates` in `app/readiness_gates.py`.

| Gate | Status | What still blocks PASS |
|---|---|---|
| G0 Scope & safety boundary | **EXTERNAL REVIEW** | Independent MDR/MDSW + clinical-safety review |
| G1 Clinical truth | **BLOCKED** | Holdout #3 is safely conservative but only 26.3% micro recall with 100% review burden; model-assisted next generation still needs fresh development + a future untouched holdout |
| G2 German interoperability | **PARTIAL** | Terminology coverage, version/incremental sync, real SJK/KIS/LIS/vendor sandbox |
| G3 Privacy & security | **PARTIAL** | Real hospital IdP/context, immutable audit, KMS/encryption, hospital DSFA/agreements, C5 evidence where applicable, pentest |
| G4 Production reliability | **PARTIAL** | Failure injection against real dependencies, real-source freshness, backup/restore + measured RPO/RTO, monitoring/SLO exercise |
| G5 Regulatory & quality | **EXTERNAL REVIEW** | Formal qualification/classification, AI Act/EHDS assessment, reviewed risk/QMS lifecycle |
| G6 Invisible workflow integration | **PARTIAL** | Real KIS/portal context launcher, Citrix/VDI/managed-browser proof, measured no-copy/no-second-search workflow |
| G7 Hospital deployment kit | **PARTIAL** | SJK actual systems/contacts/data flow, responsible approvals, network/security evidence, pentest and accepted stop thresholds |
| G8 Repeatable deployment | **PARTIAL** | Hospital A + different Hospital B/vendor without a CareOS core fork |
| G9 National/EU scale | **BLOCKED** | Actual ePA/TI/KIM/ISiP/outpatient/EHDS paths and multi-site operating evidence |

## Evidence now implemented

### G1 — Clinical truth

- mandatory `ClinicalFact` / `TruthEnvelope` contract;
- exact source identity/version/time semantics where supplied;
- document/model outputs are **untrusted candidates** until source evidence is mechanically verified;
- model-assisted boundary requires an exact source quote that CareOS independently locates; fuzzy/paraphrase evidence is rejected;
- model-proposed effective clinical time is not admitted without a governed temporal normalizer;
- assertion maturity (`preliminary / final / corrected / cancelled`) is separate from extraction confidence;
- confidence never selects a winner between conflicting clinical assertions;
- deterministic case-level reconciliation is downstream of all extractors;
- recency is allowed only for explicitly governed state-snapshot fact families;
- a newer unresolved high-risk source can block older parsed state from appearing current;
- cross-patient truth is rejected;
- ambiguous/unknown facts are routed to review;
- explicit governed contradiction rules do not silently choose a winning source.

### Frozen G1 Holdout #3

**ID:** `g1-holdout3-2026-08-16`  
**Fingerprint:** `e21633181e2d592c9a16653c9a99fb5a0c96dcf787e716dc4ea155cedbfa3ea4`

First/locked result across 500 synthetic unseen-format cases:

- micro precision **100%**;
- micro recall **26.32%**;
- F1 **41.67%**;
- unsupported-claim rate **0%**;
- wrong-source count **0**;
- provenance coverage **100%**;
- critical silent field misses **0**;
- critical silent contradiction misses **0**;
- review case rate **100%**;
- all-fields exact **0%**.

This keeps G1 **BLOCKED**. The safety failure mode has shifted toward explicit abstention, but the review burden/recall are not usable. Holdout #3 is frozen historical evidence and must not be used as tuning data.

### G2 — Interoperability
- real HAPI FHIR integration path;
- bounded same-origin FHIR Bundle pagination;
- cross-origin continuation, loops and silent max-page truncation fail closed;
- vendor-neutral `ConnectorReadResult = SourceState + TruthEnvelope` contract;
- pinned gematik reference validator **2.16.6** + ISiK5 plugin **1.0.4**, SHA-256 verified in CI;
- synthetic ISiK5 Patient validation workflow green;
- profile validation and terminology validation explicitly separated.

### G3 — Security / privacy
- asymmetric OIDC JWT verifier with issuer/audience/expiry/signature checks;
- symmetric/`none` algorithms rejected for hospital OIDC;
- role/scope/treatment-context authorization policy;
- short-lived identity/organisation/patient-bound context-launch contract;
- break-glass requires reason and elevated audit semantics;
- secure read coordinator withholds patient truth on denial, source failure/staleness, patient mismatch or required audit failure;
- keyed audit pseudonyms + recursive PHI-key rejection;
- tamper-evident local audit chain;
- provider-data-plane privacy architecture, DSFA support and AVV requirements package.

### G4 — Reliability / operations
- explicit `current / stale / unavailable / unknown` source state;
- source outage cannot become a normal empty patient result;
- global and connector-specific runtime kill switch;
- deployment/rollback and incident-response runbooks;
- reliability/SLO framework;
- dedicated safety failure-injection CI;
- `CAREOS_DATA_MODE=live-readonly` **refuses application startup while G0–G5 are incomplete**;
- transactional/write-back mode is unsupported by release policy.

### G6/G7 — SJK reference pathway
- synthetic SJK Infectiology reference environment;
- low-spec/mobile browser test;
- 5-minute team-test protocol;
- Chefarzt one-page decision brief;
- read-only integration discovery checklist;
- full staged `SJK_END_TO_END_PLAN.md` from synthetic test through gated live-read-only pilot;
- hospital assurance pack, risk register, safety-aware change control and pilot measurement protocol.

## Live-data lock

Identifiable live patient data remains **locked** while any of G0–G5 is not `PASS`.

This is enforced in code, not only documented.

A green unit test is not sufficient to pass an assurance gate. External-review and real-deployment gates require named qualified reviewers, real infrastructure and linked evidence.

## Immediate critical path

1. **G1:** integrate/evaluate the evidence-first model-assisted extractor on a **fresh development corpus**; do not tune Holdout #3. Freeze a future untouched holdout only after the next architecture is fixed.
2. **SJK Stage 0:** run the synthetic team test and collect measured task evidence.
3. **G0/G5:** obtain independent clinical-safety + MDR/software-regulatory review.
4. **G2:** if the SJK workflow test earns it, run the IT discovery and secure one real read-only KIS/LIS/vendor sandbox.
5. **G3:** connect a real hospital IdP/context source, central protected audit/KMS, complete hospital-specific privacy/security evidence, then external pentest.
6. **G4:** run failure injection, backup/restore and incident/rollback exercises in the target deployment.

Only then does a read-only identifiable live-data pilot become eligible for a go/no-go decision.
