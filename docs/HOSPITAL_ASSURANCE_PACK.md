# CareOS Hospital Assurance Pack

This is the **review index** a hospital should receive before an identifiable live-data pilot is even proposed.

It is designed so clinical leadership, CIO/integration, Informationssicherheit/CISO, Datenschutz, operations and regulatory/quality reviewers can inspect the same system from different accountability perspectives.

> Reference Architecture readiness is proposal-grade. **No hospital production approval is implied.** Live patient data remains gated by G0–G5 and provider approval.

## Start here

1. `README.md` — product thesis, evidence and current blockers.
2. `docs/ARCHITECTURE_V2.md` — canonical reference architecture.
3. `docs/TRUST_AND_DATA_FLOW.md` — trust zones and patient-data flows.
4. `docs/DEPLOYMENT_PATTERNS.md` — on-prem/private, dedicated provider tenant, federated managed service.
5. `docs/GATES.md` — what is still not allowed.
6. `docs/RESPONSIBILITY_MODEL.md` — who owns which control.
7. `docs/TECHNICAL_DOCUMENTATION_INDEX.md` — evidence index.

## A. Product & clinical boundary

Required package:

- `README.md`;
- `docs/ARCHITECTURE_V2.md`;
- `docs/SAFETY_CASE.md`;
- `docs/REFERENCE_ARCHITECTURE_SCORECARD.md`;
- `docs/adr/` architecture decisions;
- written intended-purpose statement;
- specialty workflow definition for the proposed department;
- explicit prohibited/autonomous-action list;
- current gate manifest.

Reviewer must be able to answer:

- Is CareOS system of record? **No.**
- Does CareOS autonomously diagnose/select treatment? **Not in current intended-use boundary.**
- Can production write-back occur? **No, current release boundary is read-only.**
- Can a sponsor waive the safety gates? **No.**

## B. Architecture / deployment dossier

- `docs/ARCHITECTURE_V2.md`;
- `docs/DEPLOYMENT_PATTERNS.md`;
- `docs/TRUST_AND_DATA_FLOW.md`;
- `architecture/reference-architecture.json`;
- `docs/RESPONSIBILITY_MODEL.md`;
- provider-specific deployment selection record.

Hospital-specific completion must name:

- deployment pattern;
- network zones;
- processing locations;
- hosting/provider/subprocessors;
- provider data-plane location;
- source systems;
- identity provider;
- audit/SIEM destination;
- key/KMS owner;
- backup/restore owner;
- browser/Citrix/VDI/device surfaces;
- kill-switch and rollback owners.

## C. Interoperability dossier

- `docs/FHIR_INTEGRATION.md`;
- `docs/CONNECTOR_SDK.md`;
- `docs/NATIONAL_INTEGRATION_MAP.md`;
- pinned ISiK validation evidence;
- exact ISiK/plugin/validator versions;
- hospital/vendor capability matrix;
- resources/fields requested from each source;
- source identifiers/versions/timestamps;
- paging/version/freshness behavior;
- source outage/degraded-mode behavior;
- terminology validation/mapping evidence;
- read/write capability separation.

A green generic FHIR or ISiK structural test is not sufficient. The target hospital's actual KIS/LIS interfaces and lifecycle semantics must be demonstrated.

## D. Clinical truth / data-quality dossier

- `docs/BENCHMARK.md`;
- canonical `ClinicalFact` / `TruthEnvelope` contract;
- patient identity policy;
- source evidence/provenance contract;
- terminology/unit policy;
- temporal/lifecycle semantics;
- reconciliation/contradiction rules;
- review/abstention behavior;
- frozen holdout evidence;
- target workflow shadow-study protocol.

Before live use, the reviewer must understand both **what CareOS gets right and where it abstains/fails**.

Current G1 remains blocked because synthetic Holdout #3 has high precision/provenance but insufficient recall and 100% review burden.

## E. Datenschutz dossier

- `docs/TRUST_AND_DATA_FLOW.md`;
- `docs/DATA_FLOW_AND_PRIVACY.md`;
- `docs/DPIA_SUPPORT.md`;
- `docs/AVV_DPA_REQUIREMENTS.md`;
- `docs/RESPONSIBILITY_MODEL.md`;
- provider-specific purpose + data-category register;
- controller/processor role assessment;
- legal-basis assessment by responsible parties;
- AVV/DPA where appropriate;
- subprocessor register;
- hosting/processing locations;
- retention/deletion schedule;
- patient/staff transparency and rights process where applicable;
- final DSFA/DPIA and DSB review where required;
- §393 SGB V/C5/customer-control evidence where applicable.

Reference architecture preference: routine identifiable clinical data remains provider-side or in a provider-controlled dedicated tenant rather than a shared national CareOS PHI database.

## F. Information-security dossier

- `SECURITY.md`;
- `docs/THREAT_MODEL.md`;
- `docs/TRUST_AND_DATA_FLOW.md`;
- authentication/authorization design;
- patient/treatment-context policy;
- break-glass policy;
- protected central audit/SIEM design;
- encryption/KMS/secrets design;
- tenant-isolation evidence;
- CodeQL results;
- dependency vulnerability audit;
- CycloneDX SBOM;
- Dependabot/update process;
- penetration-test scope/report;
- incident/breach workflow;
- backup/restore evidence;
- security monitoring/alerting.

Internal security CI is evidence of engineering discipline, **not a substitute for a target-environment penetration test or hospital CISO acceptance**.

## G. Reliability / operations dossier

- `docs/DEPLOYMENT_RUNBOOK.md`;
- `docs/INCIDENT_RESPONSE.md`;
- `docs/SLO_POLICY.md`;
- dependency inventory;
- explicit current/stale/unavailable/unknown source semantics;
- safety failure-injection results;
- container smoke/live-lock evidence;
- RPO/RTO;
- measured backup/restore test;
- source-specific freshness policy;
- operational dashboards/alerts;
- rollback/kill-switch procedure;
- maintenance/update process;
- support/on-call/escalation model.

Required target-environment exercise:

- source outage;
- IdP outage;
- audit outage;
- network partition;
- stale source;
- partial response;
- deployment rollback;
- restore from backup where state is persisted.

## H. Regulatory / quality dossier

- `docs/REGULATORY_BASELINE_DE.md`;
- `docs/TECHNICAL_DOCUMENTATION_INDEX.md`;
- `docs/ASSURANCE_CROSSWALK.md`;
- `docs/RISK_REGISTER.md`;
- `docs/CHANGE_CONTROL.md`;
- independent MDR/MDSW qualification/classification assessment;
- AI Act applicability assessment;
- EHDS applicability/interoperability/logging assessment where relevant;
- reviewed clinical risk-management file;
- software/model/data versioning and release records;
- QMS/lifecycle evidence appropriate to the resulting classification.

CareOS does not self-certify these questions.

## I. Supply-chain / release dossier

Current internal foundations:

- pinned direct Python dependencies;
- scheduled `pip-audit` vulnerability scan;
- CycloneDX SBOM artifact;
- Dependabot for dependencies and Actions;
- CodeQL static analysis;
- non-root container runtime;
- health check;
- CI proving synthetic startup and live-readonly lock.

Before production, extend this with deployment-appropriate artifact integrity/signing/provenance, release approval and rollback evidence.

## J. Pilot evidence dossier

Before scaling, report at least:

- usability/task completion;
- median time-to-required-fact;
- searches/logins/calls/faxes avoided;
- duplicate documentation avoided;
- correction rate;
- provenance coverage;
- unsupported-claim rate;
- wrong-source rate;
- wrong-patient rate;
- critical silent miss/contradiction rate;
- false-alert/review burden;
- clinician cognitive-effort score;
- source availability/freshness;
- repeated/would-use-again behavior.

Do not substitute user enthusiasm for measured workflow evidence.

## K. Public-sector / procurement dossier

For hospital groups or public bodies, add:

- `docs/GOVERNMENT_REFERENCE_ARCHITECTURE.md`;
- `docs/NATIONAL_INTEGRATION_MAP.md`;
- `docs/PROCUREMENT_REQUIREMENTS.md`;
- `docs/adr/ADR-009-national-rails-first.md`;
- `docs/adr/ADR-010-open-connector-contract.md`.

The procurement model intentionally allows the state/provider to require open safety/interoperability properties from CareOS **or another implementation** rather than creating new lock-in.

## Pilot go/no-go rule

No one document, scan, architecture score or sponsor makes CareOS safe.

An identifiable live-data pilot is eligible for a go/no-go decision only when:

1. machine-readable core gates G0–G5 are `PASS`;
2. the target provider's accountable clinical/IT/security/privacy/regulatory reviewers accept the deployment;
3. the intended scope and data flows are fixed;
4. stop thresholds and rollback are agreed before activation;
5. required independent assurance evidence is closed.
