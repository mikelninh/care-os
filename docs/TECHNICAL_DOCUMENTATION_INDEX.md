# CareOS Technical Documentation Index

Purpose: provide one reviewable index for hospital, government, security, privacy and future conformity-assessment discussions.

Status: **living technical documentation package**. Mapping does not claim legal applicability or conformity.

Baseline date: **2026-08-16**.

## 1. Product identity and intended purpose

| Required information | CareOS evidence |
|---|---|
| Product / system description | `README.md` |
| Intended-use boundary | `docs/SAFETY_CASE.md`, `docs/ARCHITECTURE_V2.md` |
| Explicit prohibited/autonomous actions | `docs/SAFETY_CASE.md`, `docs/ARCHITECTURE_V2.md` |
| Current release/gate state | `docs/GATES.md`, `app/readiness_gates.py` |
| Current target specialty | `docs/SPECIALTY_PACKS.md`, SJK synthetic reference pack |

## 2. Architecture

| Required information | CareOS evidence |
|---|---|
| Logical architecture | `docs/ARCHITECTURE_V2.md` |
| Government/national architecture | `docs/GOVERNMENT_REFERENCE_ARCHITECTURE.md` |
| Deployment patterns | `docs/DEPLOYMENT_PATTERNS.md` |
| Trust boundaries / data flows | `docs/TRUST_AND_DATA_FLOW.md` |
| Country/global composition | `docs/GLOBAL_ARCHITECTURE.md` |
| National/EU integration map | `docs/NATIONAL_INTEGRATION_MAP.md` |
| Architecture decisions | `docs/adr/` |

## 3. Data structures and processing

| Required information | CareOS evidence |
|---|---|
| Canonical clinical fact contract | `app/clinical_truth.py`, `docs/ARCHITECTURE_V2.md` |
| Patient identity rules | `app/patient_identity.py` |
| Document/model candidate boundary | `app/document_pipeline.py`, `app/extractors/model_schema.py` |
| Temporal handling | temporal normalizer / truth contract tests |
| Unit normalization | `app/unit_normalization.py` |
| Contradictions/reconciliation | `app/contradictions.py`, reconciliation modules/tests |
| Source state/freshness | `app/source_state.py` |

## 4. External interfaces

| Interface | Evidence/status |
|---|---|
| FHIR | `app/fhir_adapter.py`, integration tests |
| Connector contract | `app/connectors/base.py`, `docs/CONNECTOR_SDK.md` |
| ISiK validation | `.github/workflows/isik5-validation.yml` + pinned validator/plugin evidence |
| Provider OIDC | `app/auth_oidc.py` |
| Context launch | `app/context_launch.py` |
| ePA/TI/KIM/ISiP | architecture only; see `docs/NATIONAL_INTEGRATION_MAP.md` |

## 5. Security and privacy

| Required information | CareOS evidence |
|---|---|
| Threat model | `docs/THREAT_MODEL.md` |
| Authentication | `app/auth_oidc.py` + tests |
| Authorization/treatment context | `app/access_policy.py` + tests |
| Secure read orchestration | `app/clinical_session.py` + tests |
| Kill switch | `app/kill_switch.py` |
| Audit design | `app/audit.py`, `app/audit_chain.py` |
| Data-flow/privacy model | `docs/DATA_FLOW_AND_PRIVACY.md`, `docs/TRUST_AND_DATA_FLOW.md` |
| DPIA/DSFA support | `docs/DPIA_SUPPORT.md` |
| AVV/DPA requirements | `docs/AVV_DPA_REQUIREMENTS.md` |
| Hospital assurance package | `docs/HOSPITAL_ASSURANCE_PACK.md` |
| Production security blockers | `docs/GATES.md`, Issue #3 |

## 6. Reliability and operations

| Required information | CareOS evidence |
|---|---|
| Deployment/rollback | `docs/DEPLOYMENT_RUNBOOK.md` |
| Incident response | `docs/INCIDENT_RESPONSE.md` |
| SLO policy | `docs/SLO_POLICY.md` |
| Source stale/unavailable semantics | `app/source_state.py` |
| Failure injection | `.github/workflows/safety-failure-injection.yml` |
| Pagination/partial-read behavior | FHIR paging tests |
| Backup/restore evidence | **external/target-environment blocker** |
| Production monitoring | **external/target-environment blocker** |

## 7. Verification and validation

| Evidence | Purpose |
|---|---|
| Unit/integration CI | regression evidence |
| HAPI FHIR integration | real FHIR-server transport evidence |
| ISiK validator CI | structural/profile validation evidence |
| G1 synthetic benchmarks | extraction/reconciliation failure measurement |
| Holdout #3 | frozen unseen-format benchmark |
| safety failure-injection CI | fail-closed behavior |
| SJK synthetic team protocol | workflow/usability hypothesis test |
| future real shadow study | **not yet performed** |

## 8. Clinical truth performance evidence

Current frozen Holdout #3 evidence is documented in `docs/BENCHMARK.md`.

The result demonstrates conservative safety behavior but insufficient recall/review burden for production. This is intentionally recorded as a blocker rather than hidden.

## 9. Regulatory / quality documentation

| Required information | CareOS evidence |
|---|---|
| Current regulatory baseline | `docs/REGULATORY_BASELINE_DE.md` |
| External review questions | `docs/EXTERNAL_REVIEW_BRIEF.md` |
| Risk register | `docs/RISK_REGISTER.md` |
| Change control | `docs/CHANGE_CONTROL.md` |
| Intended-purpose review | safety/architecture docs |
| MDR/MDSW classification | **qualified external review required** |
| AI Act applicability | **qualified external review required** |
| EHDS applicability | **qualified external review required** |
| QMS/lifecycle | **must match resulting classification** |

## 10. Lifecycle and change history

Git history provides implementation history, but production-grade lifecycle evidence must additionally capture:

- release identifier;
- architecture version;
- connector versions;
- model/parser versions;
- terminology versions;
- policy versions;
- safety-impact assessment;
- validation evidence;
- rollout decision;
- rollback decision;
- post-release incidents/corrections.

`docs/CHANGE_CONTROL.md` defines the initial discipline.

## 11. EHDS-oriented documentation mapping

Regulation (EU) 2025/327 Annex III includes technical-documentation expectations for EHR systems/components within scope, including system description, intended purpose, hardware/software interaction, versions, architecture, technical specifications, lifecycle changes, instructions, performance evaluation, standards/common specifications, verification/validation results, information sheet and declaration of conformity.

CareOS maps these categories as follows **without claiming that CareOS is currently an EHR system in scope or that conformity has been established**:

| EHDS-style category | CareOS location |
|---|---|
| system description / intended purpose | README + safety case |
| software interactions | Architecture V2 + integration map |
| versions/update requirements | Git/release/change-control records |
| architecture diagrams | Architecture V2 + trust/data-flow docs |
| data structures/I/O | Clinical truth + connector contracts |
| lifecycle changes | change-control + release history |
| instructions | deployment/runbook/user/pilot documentation |
| performance evaluation | benchmark + pilot protocols |
| standards/common specifications | national integration map |
| verification/validation | CI + benchmark artifacts |
| information sheet | future formal artifact if applicable |
| declaration of conformity | not applicable until legal scope and evidence support it |

## 12. Missing evidence before live-data production

This index intentionally exposes missing evidence:

- real hospital IdP and authorization mapping;
- real KIS/LIS/vendor integration;
- production KMS/secrets/encryption evidence;
- protected central audit/SIEM integration;
- backup/restore RPO/RTO test;
- real target-environment failure injection;
- penetration test;
- hospital-specific DSFA/AVV approvals;
- regulatory/classification determination;
- classification-appropriate QMS;
- shadow/live clinical evaluation;
- second independent hospital/vendor deployment.

Those are release blockers, not documentation omissions to be papered over.
