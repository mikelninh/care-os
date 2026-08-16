# CareOS Production Readiness Gates

CareOS graduates by **evidence-backed gates, not version number**.

The machine-readable source is `GET /api/readiness/gates` in `app/readiness_gates.py`.

| Gate | Current status | Release question |
|---|---|---|
| G0 Scope & safety boundary | EXTERNAL REVIEW | Is the intended purpose explicit, stable and independently reviewed? |
| G1 Clinical truth | BLOCKED | Can every surfaced fact be traced, timed, reconciled and safely marked unknown/review? |
| G2 German interoperability | BLOCKED | Does CareOS validate against applicable German profiles and a real vendor/hospital read-only source? |
| G3 Privacy & security | BLOCKED | Are identity, authorization, audit, encryption, privacy artifacts and independent security review real? |
| G4 Production reliability | BLOCKED | Can dependencies fail without CareOS silently showing false success/currentness? |
| G5 Regulatory & quality | EXTERNAL REVIEW | Is the regulatory position documented and is lifecycle/risk/change control appropriate? |
| G6 Invisible workflow integration | BLOCKED | Can clinicians use CareOS in the same login/patient context without duplicate work? |
| G7 Hospital deployment kit | PARTIAL | Can CIO, CISO, DSB and clinical leadership review one coherent assurance package? |
| G8 Repeatable deployment | BLOCKED | Can a second independent hospital/vendor deploy without a CareOS core fork? |
| G9 National/EU scale | BLOCKED | Does CareOS integrate with the relevant national/EU rails rather than bypass them? |

## Live-data lock

The prototype must keep identifiable live patient data **locked** while any of G0–G5 is not `PASS`.

Passing a unit test is not sufficient evidence for an assurance gate. External-review gates require named qualified reviewers and documented findings.

## Current work order

1. G0: freeze intended purpose, architecture and safety case; commission regulatory/clinical safety review.
2. G1: migrate all downstream views toward `ClinicalFact` / `TruthEnvelope`; replace brittle extraction; build a third frozen holdout.
3. G2: add version-pinned ISiK validation and one real read-only vendor/hospital sandbox.
4. G3: implement real OIDC/JWT + policy enforcement + immutable audit + privacy/security assurance pack.
5. G4: failure injection, stale/degraded-state semantics, backup/restore and SLOs.
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
