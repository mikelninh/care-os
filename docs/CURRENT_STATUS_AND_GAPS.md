# CareOS Current Status & Gap Register

Baseline: **18 August 2026**

> Purpose: one concise source of truth for what CareOS has demonstrated, what is implemented but non-live, and what still requires clinicians, hospitals, vendors, production infrastructure or independent assurance.

## Executive status

CareOS is best described as:

> **synthetic product research + runnable engineering proof + a manifest-driven hospital integration/scaling scaffold + proposal-ready reference architecture.**

It is **not** clinically validated, production approved, authorised for identifiable live patient data, or proven across hospitals.

The pre-hospital engineering question is now largely coherent. The decisive unknown is external reality: do the workflow, clinical-state, agent-safety and repeatable-integration ideas survive real clinicians, Recare's production architecture and real hospital systems?

---

# 1. Evidence-state summary

| Dimension | Current evidence state | What exists | What is still missing |
|---|---|---|---|
| Problem / workflow | **DEMONSTRATED SYNTHETICALLY** | concrete Infectiology workflow + golden journey | observed real workflow baseline |
| Clinical UX | **DEMONSTRATED SYNTHETICALLY** | changed/pending/conflict/source-linked views | multi-clinician usability evidence |
| Clinical truth / provenance | **DEMONSTRATED SYNTHETICALLY — G1 BLOCKED** | source/time/lifecycle/contradiction/supersession contracts | useful recall/review burden + real-source variation |
| Patient-local graph | **IMPLEMENTED + TESTED** | hard patient partition, evidence-linked derived relations | real source/event volume |
| Stale-artifact invalidation | **IMPLEMENTED + TESTED** | corrected/superseded facts reopen dependent unsigned content | real clinical workflow evidence |
| Agent containment | **DEMONSTRATED SYNTHETICALLY** | deterministic gateway/tool proxy/delegation/audit | production identity, traffic and incident evidence |
| Adversarial evaluation | **DEMONSTRATED SYNTHETICALLY** | wrong patient, injection, outage, stale, write escalation | production regression history + independent red team |
| Resilience / recovery | **IMPLEMENTED + TESTED SYNTHETICALLY** | NORMAL/DEGRADED/OFFLINE/RECOVERY + reconciliation | target-hospital downtime/recovery exercise |
| Patient/family experience | **IMPLEMENTED SYNTHETICALLY** | source-linked explanation, pending state, teach-back, proxy grant | patient/family usability + real access infrastructure |
| Cross-provider lifecycle | **IMPLEMENTED CONTRACT** | acknowledged request lifecycle + purpose-limited context | real KIM/FHIR/vendor/network transport |
| Hospital manifest / preflight | **IMPLEMENTED + TESTED** | non-secret capability manifest, adapter/identity/owner checks | real hospital manifests + discovery accuracy |
| Hospital-local FHIR-family data plane | **IMPLEMENTED — NON-LIVE** | multi-source source-state-aware runtime | real auth/vendor/MPI + live approval |
| Trusted MPI/source-ID resolver | **IMPLEMENTED CONTRACT** | deterministic source-specific ID resolution, fail-closed states | approved real hospital resolver integration |
| Hospital review pack | **IMPLEMENTED + TESTED** | JSON/Markdown/Mermaid generated from non-secret manifest | real DPO/CISO/IT review feedback |
| Canary / rollback controller | **IMPLEMENTED + TESTED** | preflight→conformance→canary→promote/rollback evidence gates | target-environment rollout evidence |
| Compatibility registry | **IMPLEMENTED + TESTED** | vendor/product/version evidence classes + explicit version matching | real vendor/version records |
| HL7 v2 ADT/ORU library connector | **IMPLEMENTED SYNTHETICALLY** | read-only parsing, lifecycle, dedup, wrong-patient/malformed handling | real transport/interface engine + vendor/profile evidence |
| Docker / Helm install scaffold | **IMPLEMENTED — NON-LIVE** | hardened local/cluster deployment shape | validated target-hospital deployment + release operations |
| Time Returned to Care study | **IMPLEMENTED — EVIDENCE PENDING** | counterbalanced matched-case UI, export, aggregator, safety gates | actual participant sessions |
| Recare-targeted capstone | **RUNNABLE SYNTHETIC PROOF** | FastAPI + CareOS gateway/tool/eval path | provider-backed trace + production context |
| German interoperability | **PARTIAL** | FHIR/ISiK path, national integration blueprint | real KIS/LIS/vendor sandbox |
| EU/global portability | **RESEARCH PROOF** | state/provenance/trust/translation separation | real conformance/exchange evidence |
| Production PHI operations | **BLOCKED BY DESIGN** | live-data locks + security architecture | hospital IdP/KMS/SIEM/DPIA/DPA/operations |
| Multi-hospital repeatability | **NOT EVIDENCED** | anti-fork architecture + reuse contracts | two independent real sites/vendors |
| Clinical/regulatory assurance | **EXTERNAL REVIEW REQUIRED** | safety/risk/regulatory question set | fixed intended use + qualified independent review |

---

# 2. Claim boundary

## Safe to claim today

- a runnable synthetic healthcare-agent/workflow architecture;
- source-linked clinical-state semantics with explicit lifecycle and uncertainty;
- deterministic agent authority outside the model;
- replayable adversarial/failure scenarios;
- patient-local graph + downstream invalidation on source correction;
- explicit degraded/offline/recovery behavior;
- a source-linked synthetic patient/family experience;
- transport-agnostic cross-provider workflow state;
- FHIR/ISiK-oriented interoperability architecture;
- a runnable non-live hospital manifest/preflight/local-data-plane scaffold;
- deterministic trusted-MPI/source-ID resolver contract;
- generated non-secret hospital review artifacts;
- evidence-gated rollout/rollback contract;
- vendor/product/version compatibility registry;
- narrow synthetic/deidentified HL7 v2 ADT/ORU library connector;
- Docker/Helm packaging for synthetic/deidentified evaluation;
- a paired Time Returned to Care study with counterbalanced order + matched case variants;
- clinician-study and hospital-rollout methodology;
- global portability research preserving content/state/provenance/trust/policy distinctions.

## Do not claim today

- clinical validation or clinical effectiveness;
- measured clinician time savings;
- production hospital deployment;
- production PHI handling;
- fully self-service real-hospital installation;
- a production-ready generic HL7 v2 transport/interface-engine integration;
- compatibility with a named KIS/LIS/MPI merely because the contract exists;
- a CareOS computer-use/KIS Operator implementation;
- production-scale GenAI reliability;
- real KIS/LIS interoperability;
- zero-downtime rollout;
- 24/7 contractual service;
- multi-hospital repeatability;
- regulatory approval or certification.

---

# 3. What is closed as far as responsibly possible outside a hospital

## Clinical/product foundation

- [x] one bounded first specialty/workflow;
- [x] clinician-first changed/pending/conflict/source hierarchy;
- [x] patient-facing source-linked presentation;
- [x] explicit preliminary/final/corrected/cancelled/pending/stale/unavailable semantics;
- [x] patient-local graph;
- [x] downstream stale-artifact invalidation;
- [x] cross-provider request lifecycle;
- [x] paired workflow study protocol/UI/export/aggregator;
- [x] safety-stop metrics that override speed;
- [x] golden end-to-end regression story.

## Engineering/scaling foundation

- [x] Python / FastAPI / Pydantic backend;
- [x] FHIR integration path;
- [x] ISiK-oriented validation path;
- [x] clinical-truth contracts;
- [x] zero-trust agent gateway + trusted tool proxy;
- [x] hostile-worker/failure test cases;
- [x] hospital capability manifest;
- [x] deterministic adapter selection/maturity;
- [x] FHIR capability discovery;
- [x] shared-enterprise-ID multi-source runtime;
- [x] trusted MPI/source-ID resolver contract;
- [x] partial-source behavior that forbids false absence;
- [x] hospital review-pack generation;
- [x] upgrade compatibility preflight;
- [x] canary/promotion/rollback state/evidence contract;
- [x] compatibility registry;
- [x] narrow HL7 v2 ADT/ORU library connector;
- [x] Docker Compose + Helm deployment scaffolds;
- [x] CI for hospital platform, future foundation and adversarial agent behavior.

## Security/safety architecture

- [x] wrong-patient denial;
- [x] no fuzzy/model patient matching;
- [x] patient/encounter/task/tool agent scope;
- [x] prompt-injection containment scenarios;
- [x] unavailable/stale state preserved;
- [x] read/write separated;
- [x] hidden/consequential write disabled;
- [x] deny-default egress reference posture;
- [x] audit/revocation/kill-switch foundations;
- [x] code-enforced live-data/live-agent locks;
- [x] endpoint/credential values outside versionable manifests;
- [x] dependency lock, CodeQL, container and supply-chain foundations.

---

# 4. What we can still improve without external access

These are legitimate engineering improvements, but they are now secondary to real feedback.

### Clinical-truth development

G1 is the largest internal blocker. Improve recall/review burden on a **fresh development corpus** while preserving precision, provenance and critical-silent-miss reporting. Do not tune against the frozen holdout.

### Builder/observability UX

A local trace explorer can make model → policy → tool → evidence → draft → eval behavior easier to inspect. Useful for reviewers, but not a substitute for production observability.

### Accessibility

Complete keyboard, focus, 200% zoom, reduced-motion and assistive-technology checks on the synthetic clinician surface.

### HL7 transport abstraction

The ADT/ORU parser exists. A transport/interface-engine layer can be designed, but real MLLP/channel/auth/ACK/retry behavior should be informed by an actual integration environment rather than invented.

### Documentation consistency

Keep this file + `FOUNDATION_IMPLEMENTATION_STATUS.md` + `GATES.md` as the current-state sources. The master plan/endgame describe the future and should not be read as evidence that future-state capabilities exist.

---

# 5. Gaps that require external reality

## Real clinicians / users

Need complete paired synthetic sessions with actual task time, errors, pending-work misses, source checks, corrections, effort and observed friction.

## Recare / production architecture

Need expert critique of overlap and assumptions: actual adapter SDKs, configuration vs custom integration, source lifecycle, provenance, Agent/Patient Overview architecture, rollout/versioning and real implementation bottlenecks.

## Real KIS / LIS / hospital integration

Need a named vendor/version, one real capability manifest, interface discovery, source lifecycle behavior, identity/context launch, local terminology, latency/partial-read behavior and an approved sandbox/deidentified boundary.

## Privacy/security operations

Need provider evidence for IdP/role/treatment context, KMS/secrets, network controls, protected audit/SIEM, backup/restore, DPA/AVV, DPIA/DSFA where applicable, incident response and independent penetration testing.

## Clinical/regulatory/quality assurance

Need fixed intended use and deployment context before medical-device applicability, clinical safety governance, QMS/change control, human factors and applicable EU/German obligations can be assessed responsibly.

## Production GenAI operations

Need real provider configuration, traffic, latency/cost, model/prompt versioning, production traces, correction loops, incidents, model migrations and actual SLO evidence.

## Repeatability

Need at least:

1. Hospital A real approved read-only/deidentified source path;
2. Hospital B with another vendor/version;
3. no core contract fork;
4. custom engineering hours/site;
5. adapter/conformance reuse measurement;
6. upgrade regression evidence.

---

# 6. Production gates

| Gate | State | Why it cannot close synthetically |
|---|---|---|
| G0 Scope & clinical safety | **EXTERNAL REVIEW** | intended use + independent clinical/regulatory review |
| G1 Clinical truth | **BLOCKED** | recall/review burden + workflow evidence |
| G2 German interoperability | **PARTIAL** | real vendor/sandbox required |
| G3 Privacy & security | **PARTIAL** | provider controls + independent evidence |
| G4 Reliability | **PARTIAL** | target-environment load/recovery/SLO evidence |
| G5 Regulatory & quality | **EXTERNAL REVIEW** | classification + quality/risk lifecycle |
| G6 Invisible workflow | **PARTIAL** | real KIS-context launch / actual devices |
| G7 Hospital deployment | **PARTIAL** | provider approvals + target operations |
| G8 Repeatability | **NOT EVIDENCED** | two real independent sites/vendors |
| G9 Germany/EU scale | **RESEARCH ONLY** | real national/cross-border integration |

No identifiable-live-data gate changes merely to make the demo or installer look more complete.

---

# 7. Highest-value next actions

1. **Pavlo/Recare critique.** Learn what production already solves better and where the real integration pain lives.
2. **Run real synthetic user sessions.** Start with clinician morning review; capture paired behavior rather than opinions.
3. **Turn feedback into issues/regressions.** Every recurring friction or safety misunderstanding becomes a concrete change/test.
4. **First real hospital capability manifest.** Fill it with hospital IT without accessing live patient data.
5. **Approved synthetic/deidentified KIS/LIS/vendor sandbox.** Discover actual interoperability gaps.
6. **Measure integration economics.** Configuration vs custom engineering, conformance failures, time to first useful workflow.
7. **Shadow workflow only after governance.** No dependency first.
8. **Second site/vendor.** The first real proof that the architecture is infrastructure rather than one-off consulting.

---

# 8. What not to build before external feedback

Avoid productivity theatre:

- more specialties with no users;
- another broad AI feature;
- fake production integrations;
- autonomous diagnosis/treatment logic for portfolio breadth;
- another country pack just to make the roadmap longer;
- a parallel Recare product;
- extra dashboards with no user;
- invented time savings;
- patient data used to accelerate evidence;
- self-awarded architecture/production scores.

---

## Definition of pre-hospital phase complete

The pre-hospital phase is complete when the problem is concrete, one workflow is usable synthetically, trust/failure boundaries are explicit, adversarial tests exist, model authority is bounded, interoperability direction is standards-aligned, rollout/evaluation methods are explicit, and a plausible repeatable deployment contract exists **without claiming it has been proven in hospitals**.

**CareOS now satisfies that definition.**

> The honest gap is no longer imagination. It is external evidence — especially whether the workflow and integration model survive Recare and real hospital systems.