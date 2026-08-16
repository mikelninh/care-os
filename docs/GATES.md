# CareOS Production Readiness Gates

CareOS graduates by **evidence-backed gates, not version number**.

Machine-readable source: `GET /api/readiness/gates` in `app/readiness_gates.py`.

> **Reference Architecture readiness is 10/10 for proposal completeness/reviewability. Production readiness is a different question. No production gate is PASS yet.**

| Gate | Status | What still blocks PASS |
|---|---|---|
| G0 Scope & safety boundary | **EXTERNAL REVIEW** | Independent MDR/MDSW + clinical-safety review |
| G1 Clinical truth | **BLOCKED** | Holdout #3: 26.3% recall + 100% review burden; next extractor needs fresh development and future untouched holdout |
| G2 German interoperability | **PARTIAL** | Production terminology, incremental sync, real SJK/KIS/LIS/vendor sandbox |
| G3 Privacy & security | **PARTIAL** | Real hospital IdP/context, protected audit/SIEM, KMS/encryption, hospital DSFA/agreements, applicable C5/customer controls, pentest |
| G4 Production reliability | **PARTIAL** | Real-dependency failure injection, backup/restore RPO/RTO, production monitoring/SLO exercise |
| G5 Regulatory & quality | **EXTERNAL REVIEW** | Formal qualification/classification, AI Act/EHDS assessment, reviewed risk/QMS lifecycle |
| G6 Invisible workflow integration | **PARTIAL** | Real KIS/portal context launcher, Citrix/VDI proof, measured no-copy/no-second-search workflow |
| G7 Hospital deployment kit | **PARTIAL** | Actual hospital systems/owners/approvals, target security evidence, pentest, accepted stop thresholds |
| G8 Repeatable deployment | **PARTIAL** | Hospital A + different Hospital B/vendor without a CareOS core fork |
| G9 National/EU scale | **BLOCKED** | Actual ePA/TI/KIM/ISiP/outpatient/EHDS integrations and multi-site operating evidence |

## Reference architecture evidence

The proposal package now includes:

- `docs/ARCHITECTURE_V2.md` — canonical technical reference architecture;
- `docs/GOVERNMENT_REFERENCE_ARCHITECTURE.md` — German public-sector architecture;
- `docs/GOVERNMENT_ONE_PAGER_DE.md`;
- `docs/DEPLOYMENT_PATTERNS.md`;
- `docs/TRUST_AND_DATA_FLOW.md`;
- `docs/NATIONAL_INTEGRATION_MAP.md`;
- `docs/TECHNICAL_DOCUMENTATION_INDEX.md`;
- `docs/ASSURANCE_CROSSWALK.md`;
- `docs/RESPONSIBILITY_MODEL.md`;
- `docs/PROCUREMENT_REQUIREMENTS.md`;
- ten Architecture Decision Records under `docs/adr/`;
- machine-readable `architecture/reference-architecture.json` with CI invariants.

The architecture score is intentionally **not used to unlock live data**.

## G1 — Clinical truth

Implemented safeguards include:

- mandatory `ClinicalFact` / `TruthEnvelope` contract;
- source identity/version/time semantics where supplied;
- document/model outputs are untrusted until source evidence is mechanically verified;
- exact source quote independently located by CareOS;
- model-proposed effective clinical time is not trusted;
- assertion maturity is separate from extraction confidence;
- confidence never silently chooses a winner between conflicting clinical assertions;
- deterministic case reconciliation is downstream of extractors;
- a newer unresolved high-risk source can block older parsed state from appearing current;
- cross-patient truth is rejected;
- ambiguous/unknown facts route to review.

### Frozen Holdout #3

**ID:** `g1-holdout3-2026-08-16`  
**Fingerprint:** `e21633181e2d592c9a16653c9a99fb5a0c96dcf787e716dc4ea155cedbfa3ea4`

Across 500 synthetic unseen-format cases:

- precision **100%**;
- recall **26.32%**;
- F1 **41.67%**;
- unsupported claims **0**;
- wrong-source claims **0**;
- provenance coverage **100%**;
- critical silent field misses **0**;
- critical silent contradiction misses **0**;
- review case rate **100%**.

This remains **BLOCKED**: the safety behavior improved, but the recall/review burden is unusable. Holdout #3 is historical evidence and is not tuning data.

## G2 — German interoperability

Internal evidence:

- real HAPI FHIR integration path;
- bounded same-origin Bundle pagination;
- cross-origin continuation, loops and silent truncation fail closed;
- vendor-neutral `ConnectorReadResult = SourceState + TruthEnvelope` contract;
- pinned gematik reference-validator + ISiK5 plugin workflow;
- structural/profile validation kept separate from terminology validation;
- explicit national/EU integration map.

A real hospital/vendor path is still required.

## G3 — Security & privacy

Internal evidence now includes:

- asymmetric OIDC/JWT verification foundation;
- role/scope/treatment-context authorization;
- short-lived user/organisation/patient context launch;
- break-glass semantics;
- secure-read coordinator that can withhold truth on authorization, source, identity or required-audit failure;
- keyed audit pseudonyms + recursive PHI-key rejection;
- tamper-evident local audit chain;
- provider-side PHI / control-plane separation;
- threat/data-flow/responsibility/DSFA/AVV assurance documentation;
- **CodeQL static security analysis in CI**;
- **scheduled dependency vulnerability audit**;
- **CycloneDX SBOM artifact**;
- **Dependabot** for Python and GitHub Actions;
- remediated dependency advisory discovered by the new supply-chain gate.

Still external: real provider IdP, production audit/SIEM, KMS/encryption, hospital agreements/approval, applicable C5/customer-control evidence and independent pentest.

## G4 — Reliability / operations

Internal evidence now includes:

- explicit `current / stale / unavailable / unknown` source state;
- fail-closed pagination/partial reads;
- global and connector-specific kill switches;
- deployment/rollback and incident-response runbooks;
- SLO framework;
- safety failure-injection CI;
- non-root container image;
- container health check;
- container CI proving synthetic startup;
- container CI proving `live-readonly` **does not start** while G0–G5 are incomplete;
- transactional/write-back mode remains unsupported.

Still external: target-environment dependency failures, recovery drills, RPO/RTO, production monitoring and incident exercises.

## G5 — Regulatory / quality

Internal preparation includes:

- intended-purpose/safety boundary;
- regulatory baseline;
- risk register;
- change-control discipline;
- technical-documentation index with EHDS-style categories;
- assurance crosswalk.

CareOS does not self-award MDR/MDSW classification, AI Act/EHDS applicability or QMS sufficiency.

## G6/G7 — SJK reference pathway

Prepared:

- synthetic SJK Infectiology reference environment;
- low-spec/mobile browser test;
- 5-minute team-test protocol + measurement tooling;
- Chefarzt decision brief/page;
- read-only integration discovery checklist;
- staged `SJK_END_TO_END_PLAN.md`;
- hospital assurance pack;
- trust/data-flow model;
- responsibility matrix;
- deployment patterns;
- procurement requirements;
- safety-aware change control and pilot protocol.

## G8 — Repeatability

The anti-consultancy architecture is explicit:

- stable connector contract;
- stable clinical-fact/provenance/failure semantics;
- one core + specialty/country/language/audience composition;
- vendor-specific logic behind connectors;
- multiple deployment patterns with the same safety contracts.

The gate still requires real Hospital A + different Hospital B evidence.

## G9 — National / EU scale

The **reference architecture is now proposal-grade** and includes national rails, procurement/anti-lock-in principles and EHDS-forward technical documentation.

G9 remains **BLOCKED** because proposal completeness is not national operating evidence.

## Live-data lock

Identifiable live patient data remains **locked** while any of G0–G5 is not `PASS`.

This is enforced in application startup policy and tested again in the container runtime workflow.

A green unit test, security scan or architecture score is not sufficient to pass an assurance gate. External-review and real-deployment gates require named qualified reviewers, real infrastructure and linked evidence.

## Immediate critical path

1. **G1:** improve recall/review burden on a fresh development corpus without tuning Holdout #3.
2. **SJK Stage 0:** collect measured synthetic clinician workflow evidence.
3. **G0/G5:** independent clinical-safety + medical-software regulatory review.
4. **G2:** earn and obtain one real read-only KIS/LIS/vendor sandbox.
5. **G3:** real hospital IdP/context, protected audit/KMS, hospital-specific Datenschutz/security evidence, independent pentest.
6. **G4:** target-environment failure, backup/restore and incident/rollback exercises.
7. **G8:** reproduce at a second hospital/vendor without a core fork.

Only after G0–G5 PASS does an identifiable read-only live-data pilot become eligible for a go/no-go decision.
