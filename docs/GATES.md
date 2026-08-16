# CareOS Production Readiness Gates

CareOS graduates by **evidence-backed gates, not version number**.

The machine-readable source is `GET /api/readiness/gates` in `app/readiness_gates.py`.

| Gate | Current status | Release question |
|---|---|---|
| G0 Scope & safety boundary | EXTERNAL REVIEW | Is the intended purpose explicit, stable and independently reviewed? |
| G1 Clinical truth | BLOCKED | Can every surfaced fact be traced, timed, reconciled and safely marked unknown/review? |
| G2 German interoperability | PARTIAL | Does CareOS validate against applicable German profiles and a real vendor/hospital read-only source? |
| G3 Privacy & security | PARTIAL | Are identity, authorization, audit, encryption, privacy artifacts and independent security review real? |
| G4 Production reliability | PARTIAL | Can dependencies fail without CareOS silently showing false success/currentness? |
| G5 Regulatory & quality | EXTERNAL REVIEW | Is the regulatory position documented and is lifecycle/risk/change control appropriate? |
| G6 Invisible workflow integration | BLOCKED | Can clinicians use CareOS in the same login/patient context without duplicate work? |
| G7 Hospital deployment kit | PARTIAL | Can CIO, CISO, DSB and clinical leadership review one coherent assurance package? |
| G8 Repeatable deployment | BLOCKED | Can a second independent hospital/vendor deploy without a CareOS core fork? |
| G9 National/EU scale | BLOCKED | Does CareOS integrate with the relevant national/EU rails rather than bypass them? |

## Evidence added in the first gate-hardening pass

- canonical `ClinicalFact` / `TruthEnvelope` model with mandatory source identity;
- document-derived facts require exact evidence spans;
- cross-patient truth envelopes fail validation;
- source-native FHIR is now converted to the truth layer before timeline rendering;
- FHIR resource version and effective/recorded time are preserved where supplied;
- fail-closed treatment-context policy contract with elevated break-glass audit semantics;
- explicit current/stale/unavailable source states; unavailable data cannot become a reassuring empty result;
- pinned gematik reference validator + ISiK5 plugin workflow with SHA-256 verification;
- synthetic ISiK5 Patient fixture validated successfully in GitHub Actions;
- full Python regression suite green after these changes.

These move G2–G4 to `PARTIAL`; they do **not** make a live-data pilot safe yet.

## Live-data lock

The prototype must keep identifiable live patient data **locked** while any of G0–G5 is not `PASS`.

Passing a unit test is not sufficient evidence for an assurance gate. External-review gates require named qualified reviewers and documented findings.

## Current work order

1. G0: commission independent regulatory qualification/classification + clinical-safety review against the written intended purpose and safety case.
2. G1: migrate all downstream ingestion to `ClinicalFact` / `TruthEnvelope`; replace brittle document extraction; add contradiction engine, terminology/unit normalization and a new frozen holdout.
3. G2: add terminology validation outside known ISiK validator exclusions; then connect one real read-only KIS/LIS/vendor sandbox.
4. G3: implement real OIDC/JWT verification and trusted hospital claim mapping; replace local audit prototype with central immutable audit; complete privacy/security assurance pack.
5. G4: failure injection across KIS/FHIR/identity/audit/model dependencies; wire freshness to real sources; add backup/restore, RPO/RTO, SLOs and rollback/kill switch.
6. G5: formal regulatory/quality/risk programme appropriate to actual classification.
7. G6–G9 only advance without weakening G0–G5.

## Evidence rule

Every `PASS` must link to evidence such as:

- automated test/CI artifact;
- validation report;
- architecture/risk record;
- independent assessment;
- penetration-test report;
- deployment acceptance record;
- measured workflow evidence.

A screenshot or implementation claim alone cannot pass a gate.
