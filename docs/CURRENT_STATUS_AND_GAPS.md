# CareOS Current Status & Gap Register

Baseline: **18 August 2026**

> Purpose: separate what is demonstrated from what still requires clinicians, hospitals, vendors, production infrastructure or external assurance.

## Executive status

CareOS is best described as:

> **synthetic product research + runnable engineering proof + proposal-ready reference architecture + hospital implementation playbook**

It is **not** clinically validated, production approved or authorised for identifiable live patient data.

The remaining high-value gaps are now primarily **external evidence gaps**, not missing speculative product features.

---

## 1. Evidence-state summary

| Dimension | Evidence state | What exists | What is still missing |
|---|---|---|---|
| Problem / workflow | **DEMONSTRATED SYNTHETICALLY** | concrete Infectiology workflow; measurable admin/search burden | observed real workflow baseline |
| Clinical UX | **DEMONSTRATED SYNTHETICALLY** | source-linked clinician demo; pending/conflict/open-work states | multi-clinician usability evidence |
| Clinical truth / provenance | **DEMONSTRATED SYNTHETICALLY** | source/time/state/contradiction/supersession contracts + tests | acceptable recall/review burden + real-source evidence |
| Agent containment | **DEMONSTRATED SYNTHETICALLY** | deterministic authority, bounded tools, delegation, audit, hostile scenarios | production identity, traffic and incident evidence |
| Adversarial evaluation | **DEMONSTRATED SYNTHETICALLY** | wrong-patient, injection, outage, stale and write-escalation tests | production regression history |
| German interoperability | **PARTIAL** | FHIR/ISiK-oriented paths and CI | real KIS/LIS/vendor sandbox |
| EU/global portability | **RESEARCH PROOF** | IPS/trust/translation/state separation | real conformance/exchange evidence |
| Hospital rollout | **PROPOSAL READY** | read-only → shadow → one-ward → copilot evidence ladder | an actual implementation |
| Recare-targeted capstone | **RUNNABLE SYNTHETIC PROOF** | FastAPI + real CareOS gateway/tool/eval path | live provider-backed trace + production context |
| Real clinician evidence | **EXTERNAL EVIDENCE REQUIRED** | study protocol, counterbalanced UI, export + aggregator | completed clinician sessions |
| Real KIS/LIS integration | **EXTERNAL EVIDENCE REQUIRED** | discovery checklist + connector contracts | vendor/system access |
| Production PHI operations | **BLOCKED BY DESIGN** | live-data locks + security architecture | hospital identity, KMS, SIEM, DPIA/DPA, operations |
| Multi-hospital repeatability | **NOT YET EVIDENCED** | reusable contracts | second site/vendor deployment |

### Claim boundary

**Safe to claim today:**

- a runnable synthetic healthcare-agent architecture;
- source-linked clinical-state semantics;
- explicit uncertainty and contradiction handling;
- deterministic agent authority outside the model;
- adversarial/replayable safety tests;
- FHIR/ISiK-oriented interoperability architecture;
- clinician-study and hospital-rollout methodology;
- global portability research preserving state/provenance/trust separation.

**Do not claim today:**

- clinical validation;
- production hospital deployment;
- production PHI handling;
- production-scale GenAI reliability;
- real KIS/LIS interoperability;
- measured clinician time savings;
- multi-hospital repeatability;
- regulatory approval.

---

## 2. Gaps closed as far as responsibly possible outside a hospital

### Clinical / product

- [x] one concrete first specialty/workflow;
- [x] clinician-first information hierarchy;
- [x] source-linked facts;
- [x] pending / unavailable / stale / contradiction semantics;
- [x] preliminary → final → corrected / cancelled reconciliation behaviour;
- [x] human review / approval boundaries;
- [x] clinician study protocol/UI;
- [x] structured anonymous result export;
- [x] study aggregator where safety gates override speed.

### Engineering

- [x] Python / FastAPI / Pydantic backend;
- [x] FHIR integration path;
- [x] ISiK-oriented validation path;
- [x] typed clinical-truth contracts;
- [x] conservative evidence verification;
- [x] agent runtime + deterministic gateway;
- [x] trusted tool proxy;
- [x] provider-neutral external-model adapter for synthetic/deidentified evaluation;
- [x] machine-readable traces/evals in the Recare capstone;
- [x] six-case Recare containment suite;
- [x] focused CI workflows;
- [x] global portability contract + tests.

### Security / safety design

- [x] wrong-patient denial;
- [x] cross-scope agent denial;
- [x] prompt-injection containment scenarios;
- [x] source outage / degraded state;
- [x] stale-state handling;
- [x] write/tool escalation denial;
- [x] workload/delegation/revocation foundations;
- [x] deny-default egress concept;
- [x] audit foundations;
- [x] kill/release gates;
- [x] code-enforced live-data/live-agent locks;
- [x] dependency lock, container and supply-chain foundations.

### Architecture / governance

- [x] provider/control-plane separation;
- [x] systems of record remain authoritative;
- [x] responsibility model;
- [x] trust/data-flow documentation;
- [x] deployment patterns;
- [x] hospital assurance pack;
- [x] German government reference architecture;
- [x] ISiK/ePA/TI/EHDS integration map;
- [x] international comparison / global blueprint;
- [x] hospital implementation playbook;
- [x] Recare overlap/collaboration map;
- [x] Apache-2.0 open-source license + contributor contract.

---

## 3. One remaining model-proof gap we can close without a hospital

The real external-model adapter is implemented, but the public evidence package does **not yet include a captured provider-backed synthetic execution** through the entire path.

A useful captured run should record:

```text
synthetic task
→ provider/model + version
→ structured tool proposal
→ deterministic policy decision
→ trusted tool call(s)
→ evidence IDs
→ draft
→ safety/eval result
→ latency + token/cost metadata when available
```

This is **not** required to begin the Recare conversation, but it is the last high-value technical proof that does not require hospital access. It requires an approved external-model endpoint/credential; do not fake it with a recorded mock and call it live.

---

## 4. Remaining gaps that require external reality

### A. Real clinician behaviour

Need several complete paired synthetic clinician sessions with actual task time, errors, pending-work misses, source checks, corrections, effort and qualitative friction.

### B. Real KIS / LIS / hospital integration

Need actual vendor/version, interface discovery, patient/encounter context launch, source lifecycle behaviour, local terminology, network/latency/partial-read behaviour and an approved sandbox/deidentified boundary.

### C. Hospital privacy / security operations

Need provider evidence for IdP/role/treatment context, KMS/secrets, network controls, audit/SIEM, DLP where required, backup/recovery, AVV/DPA, DSFA/DPIA, processors/subprocessors, incident response and independent penetration testing.

### D. Clinical / regulatory / quality assurance

Need a fixed intended use and deployment context before medical-device applicability, clinical safety governance, QMS/change control, human-factors evidence and EHDS/EHR obligations can be assessed responsibly.

### E. Production GenAI operations

Need real traffic, provider configuration, latency/cost, prompt/model versioning, production traces, user-correction loops, incidents/replay, model migration behaviour and actual SLOs.

### F. Multi-site repeatability

Need a second ward/specialty, second vendor configuration and second hospital without forking the core contracts.

---

## 5. Production gates

| Gate | State | Why it cannot close synthetically |
|---|---|---|
| G0 Scope & clinical safety | **EXTERNAL REVIEW** | intended use + independent clinical review |
| G1 Clinical truth | **BLOCKED** | recall/review burden + real workflow evidence |
| G2 German interoperability | **PARTIAL** | real vendor/sandbox needed |
| G3 Privacy & security | **PARTIAL** | provider controls + independent evidence |
| G4 Reliability | **PARTIAL** | target-environment load/recovery/SLO |
| G5 Regulatory & quality | **EXTERNAL REVIEW** | classification / QMS lifecycle |
| G6 Invisible workflow | **PARTIAL** | actual KIS-context launch |
| G7 Hospital deployment | **PARTIAL** | provider approvals and operations |
| G8 Repeatability | **NOT EVIDENCED** | second deployment |
| G9 Germany/EU scale | **RESEARCH ONLY** | real national/cross-border integration |

No identifiable-live-data gate should be changed merely to improve a demo.

---

## 6. What not to build before external feedback

Avoid productivity theatre:

- more specialties with no users;
- fake production integrations;
- autonomous diagnosis/treatment logic merely for portfolio breadth;
- another country pack without a real partner;
- a parallel Recare product;
- extra dashboards with no operational consumer;
- invented clinician time savings;
- real patient data used to accelerate evidence.

---

## 7. Highest-value next actions

1. **External engineering critique** — Recare/Pavlo or equivalent production team.
2. **Clinician synthetic sessions** — collect actual paired behaviour.
3. **Workflow observation** — watch hospital work before proposing more product.
4. **Technical discovery** — KIS/LIS/identity/network/governance.
5. **Synthetic/deidentified integration sandbox**.
6. **Shadow workflow**.
7. **Read-only pilot only when gates permit**.
8. **Second site/vendor**.

---

## Definition of “pre-hospital phase complete”

The pre-hospital phase is complete when the problem is concrete, one workflow is usable synthetically, trust boundaries and failure states are explicit, adversarial tests exist, model authority is bounded, interoperability direction is standards-aligned, rollout methodology and outcome metrics are explicit, limitations are documented, and the remaining uncertainty requires external reality.

CareOS satisfies that definition.

> **The honest gap is no longer imagination. It is access and external evidence.**
