# CareOS Technical Documentation Index

Purpose: provide one reviewable index for hospital, government, security, privacy, healthcare-AI and future conformity-assessment discussions.

Status: **living technical documentation package**. Mapping does not claim legal applicability, production approval or conformity.

Baseline date: **2026-08-18**.

## 0. Canonical review path

| Reviewer question | Start here |
|---|---|
| What is the complete pre-hospital package? | `docs/PRE_HOSPITAL_HANDOFF.md` |
| What is genuinely ready vs still external? | `docs/CURRENT_STATUS_AND_GAPS.md` |
| How does this relate to Recare rather than duplicate it? | `docs/RECARE_COLLABORATION_MAP.md` |
| How would we implement this in a hospital? | `docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md` |
| What is the Recare-targeted runnable proof? | `docs/RECARE_CAPSTONE.md` |
| How does Germany connect to EU/global interoperability? | `docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md` |

## 1. Product identity and intended purpose

| Required information | CareOS evidence |
|---|---|
| Product / system description | `README.md` |
| Pre-hospital research boundary | `docs/PRE_HOSPITAL_HANDOFF.md` |
| Current readiness / gap register | `docs/CURRENT_STATUS_AND_GAPS.md` |
| Intended-use boundary | `docs/SAFETY_CASE.md`, `docs/ARCHITECTURE_V2.md` |
| Explicit prohibited/autonomous actions | `docs/SAFETY_CASE.md`, `docs/ARCHITECTURE_V2.md` |
| Current release/gate state | `docs/GATES.md`, `app/readiness_gates.py` |
| Current target specialty | `docs/SPECIALTY_PACKS.md`, SJK synthetic reference pack |
| Targeted hiring/engineering proof | `docs/RECARE_CAPSTONE.md`, `app/recare_api.py`, `app/recare_capstone.py` |

## 2. Architecture

| Required information | CareOS evidence |
|---|---|
| Logical architecture | `docs/ARCHITECTURE_V2.md` |
| Government/national architecture | `docs/GOVERNMENT_REFERENCE_ARCHITECTURE.md` |
| Germany → global reference model | `docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md` |
| Deployment patterns | `docs/DEPLOYMENT_PATTERNS.md` |
| Hospital rollout methodology | `docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md` |
| Trust boundaries / data flows | `docs/TRUST_AND_DATA_FLOW.md` |
| Country/global composition | `docs/GLOBAL_ARCHITECTURE.md`, `app/global_packs.py` |
| Cross-border clinical-state/trust envelope | `app/global_interop.py` |
| National/EU integration map | `docs/NATIONAL_INTEGRATION_MAP.md` |
| Recare collaboration / overlap hypothesis | `docs/RECARE_COLLABORATION_MAP.md` |
| Architecture decisions | `docs/adr/` |

## 3. Data structures and processing

| Required information | CareOS evidence |
|---|---|
| Canonical clinical fact contract | `app/clinical_truth.py`, `docs/ARCHITECTURE_V2.md` |
| Patient identity rules | `app/patient_identity.py` |
| Document/model candidate boundary | `app/document_pipeline.py`, `app/extractors/model_schema.py` |
| Temporal handling | temporal normalizer / truth contract tests |
| Unit normalization | `app/unit_normalization.py` |
| Contradictions/reconciliation | reconciliation modules + `tests/test_reconciliation.py` |
| Source state/freshness | `app/source_state.py` |
| Portable clinical item / trust state | `app/global_interop.py` |
| IPS-shaped portability preview | `app/portability.py` |

## 4. External interfaces and model boundaries

| Interface | Evidence/status |
|---|---|
| FHIR | `app/fhir_adapter.py`, integration tests |
| Connector contract | `app/connectors/base.py`, `docs/CONNECTOR_SDK.md` |
| ISiK validation | `.github/workflows/isik5-validation.yml` + validator evidence |
| Provider OIDC | `app/auth_oidc.py` |
| Context launch | `app/context_launch.py` |
| ePA/TI/KIM/ISiP | architecture only; see `docs/NATIONAL_INTEGRATION_MAP.md` |
| Global portability API/contract | `app/global_interop.py`, global-interoperability tests/CI |
| Recare capstone API | `app/recare_api.py` |
| Provider-neutral model gateway | `app/agent_model_adapter.py` |
| Direct OpenAI Responses adapter | `app/openai_responses_worker.py` — synthetic/deidentified only; `store:false`; structured output; no model authority |
| Provider-backed evidence capture | `scripts/capture_recare_model_run.py` — requires a real credential/run; no mock may be relabelled as provider evidence |

## 5. Security and privacy

| Required information | CareOS evidence |
|---|---|
| Threat model | `docs/THREAT_MODEL.md` |
| Agent threat/authority model | `docs/AGENT_SECURITY_MODEL.md` |
| Authentication | `app/auth_oidc.py` + tests |
| Authorization/treatment context | `app/access_policy.py` + tests |
| Agent delegation / tool authority | `app/agent_policy.py`, `app/agent_runtime.py`, `app/agent_tool_proxy.py` |
| Secure read orchestration | `app/clinical_session.py` + tests |
| Kill switch | `app/kill_switch.py` |
| Audit design | `app/audit.py`, `app/audit_chain.py` |
| Data-flow/privacy model | `docs/DATA_FLOW_AND_PRIVACY.md`, `docs/TRUST_AND_DATA_FLOW.md` |
| DPIA/DSFA support | `docs/DPIA_SUPPORT.md` |
| AVV/DPA requirements | `docs/AVV_DPA_REQUIREMENTS.md` |
| Hospital assurance package | `docs/HOSPITAL_ASSURANCE_PACK.md` |
| Production security blockers | `docs/GATES.md`, `docs/CURRENT_STATUS_AND_GAPS.md`, Issue #3 |

## 6. Reliability and operations

| Required information | CareOS evidence |
|---|---|
| Deployment/rollback | `docs/DEPLOYMENT_RUNBOOK.md` |
| Hospital implementation sequence | `docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md` |
| Incident response | `docs/INCIDENT_RESPONSE.md` |
| SLO policy | `docs/SLO_POLICY.md` |
| Source stale/unavailable semantics | `app/source_state.py` |
| Failure injection | `.github/workflows/safety-failure-injection.yml` |
| Pagination/partial-read behavior | FHIR paging tests |
| Agent tool-handler failure termination | `app/agent_tool_proxy.py` + regression tests |
| Backup/restore evidence | **external/target-environment blocker** |
| Production monitoring | **external/target-environment blocker** |

## 7. Verification and validation

| Evidence | Purpose |
|---|---|
| Full pytest workflow | regression evidence |
| HAPI FHIR integration | FHIR-server transport evidence |
| ISiK validator CI | structural/profile validation evidence |
| G1 synthetic benchmarks | extraction/reconciliation failure measurement |
| Holdout #3 | frozen unseen-format benchmark |
| safety failure-injection CI | fail-closed behavior |
| platform red-team CI | cross-layer adversarial evidence |
| agent red-team CI | compromised-worker containment |
| Recare capstone CI | focused API/provider-adapter/model-gateway/tool-boundary/containment proof |
| `tests/test_openai_responses_worker.py` | direct-provider request contract, structured output, no-live-mode and redirect-denial tests |
| six-case Recare eval suite | happy path + wrong patient + injection + outage + stale + write denial |
| global-interoperability CI | cross-border state/trust/translation regression evidence |
| SJK synthetic team protocol | workflow/usability hypothesis test |
| paired study local export + aggregator | `scripts/aggregate_recare_study.py` |
| real provider-backed capstone run | **capture path implemented; evidence only after a real credential/run** |
| future real shadow study | **not yet performed** |

## 8. Clinical truth performance evidence

Current frozen synthetic evidence is documented in `docs/BENCHMARK.md`.

The result demonstrates conservative safety behavior but insufficient recall/review burden for production. This is intentionally recorded as a blocker rather than hidden.

The Recare work sample adds a separate containment/evaluation proof; it must not be confused with clinical efficacy validation. See `docs/RECARE_CAPSTONE.md`.

## 9. International interoperability evidence

The global interoperability layer distinguishes:

- **content** — FHIR/IPS/terminology/language;
- **trust** — issuer identity/signature/trust framework;
- **policy** — whether the receiving context may use the data for the intended purpose.

Current evidence:

- `docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md`;
- `app/global_interop.py`;
- global interoperability tests;
- `.github/workflows/global-interoperability.yml`;
- IPS-shaped preview in `app/portability.py`.

Limitations remain explicit: no claimed IPS conformance and no real cross-border issuer/trust-network verification.

## 10. Regulatory / quality documentation

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

## 11. Lifecycle and change history

Git history provides implementation history, but production-grade lifecycle evidence must additionally capture:

- release identifier;
- architecture version;
- connector/model/parser/terminology/policy versions;
- safety-impact assessment;
- validation evidence;
- rollout / rollback decisions;
- post-release incidents/corrections.

`docs/CHANGE_CONTROL.md` defines the initial discipline.

## 12. EHDS-oriented documentation mapping

CareOS maintains an EHDS-oriented documentation map **without claiming that CareOS is currently an EHR system in scope or that conformity has been established**.

| EHDS-style category | CareOS location |
|---|---|
| system description / intended purpose | README + safety case + pre-hospital handoff |
| software interactions | Architecture V2 + integration map |
| versions/update requirements | Git/release/change-control records |
| architecture diagrams | Architecture V2 + trust/data-flow docs |
| data structures/I/O | clinical truth + connector contracts + global interop contract |
| lifecycle changes | change-control + release history |
| instructions | deployment/runbook/implementation/pilot documentation |
| performance evaluation | benchmark + pilot protocols + paired-study aggregator |
| standards/common specifications | national integration map + global blueprint |
| verification/validation | CI + benchmark + capstone/global workflows |
| information sheet | future formal artifact if applicable |
| declaration of conformity | not applicable until legal scope and evidence support it |

## 13. Missing evidence before live-data production

- real clinician paired-study results;
- a captured real-provider synthetic model run if that proof is desired;
- real hospital IdP/authorization mapping;
- real KIS/LIS/vendor integration;
- real terminology/local-code governance;
- production KMS/secrets/encryption evidence;
- protected central audit/SIEM integration;
- backup/restore RPO/RTO test;
- target-environment failure injection;
- penetration test;
- hospital-specific DSFA/AVV approvals;
- regulatory/classification determination;
- classification-appropriate QMS;
- shadow/live clinical evaluation;
- actual IPS conformance evidence;
- actual EU/global trust/issuer verification;
- second independent hospital/vendor deployment.

Those are release blockers or external evidence dependencies, not omissions to paper over.

See `docs/CURRENT_STATUS_AND_GAPS.md` for the canonical gap register.
