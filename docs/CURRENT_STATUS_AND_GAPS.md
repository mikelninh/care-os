# CareOS Current Status & Gap Register

Baseline: **18 August 2026**

> Purpose: separate what is demonstrated from what still requires clinicians, hospitals, vendors, production infrastructure or external assurance.

## Executive status

CareOS is best described as:

> **synthetic product research + runnable engineering proof + a manifest-driven hospital self-install/scaling scaffold + proposal-ready reference architecture**

It is **not** clinically validated, production approved or authorised for identifiable live patient data.

The newest infrastructure hypothesis is now executable: hospital capability manifest → adapter selection/maturity → local FHIR-family data plane → Docker/Helm packaging → upgrade preflight. It remains **synthetic/deidentified evidence**, not proof of zero-touch real-hospital deployment.

---

## 1. Evidence-state summary

| Dimension | Evidence state | What exists | What is still missing |
|---|---|---|---|
| Problem / workflow | **DEMONSTRATED SYNTHETICALLY** | concrete Infectiology workflow; measurable admin/search burden | observed real workflow baseline |
| Clinical UX | **DEMONSTRATED SYNTHETICALLY** | source-linked clinician demo; pending/conflict/open-work states | multi-clinician usability evidence |
| Clinical truth / provenance | **DEMONSTRATED SYNTHETICALLY** | source/time/state/contradiction/supersession contracts + tests | acceptable recall/review burden + real-source evidence |
| Agent containment | **DEMONSTRATED SYNTHETICALLY** | deterministic authority, bounded tools, delegation, audit, hostile scenarios | production identity, traffic and incident evidence |
| Adversarial evaluation | **DEMONSTRATED SYNTHETICALLY** | wrong-patient, injection, outage, stale and write-escalation tests | production regression history |
| Hospital capability manifest / preflight | **IMPLEMENTED + SYNTHETICALLY TESTED** | non-secret manifest, adapter selection, owner/identity/readiness checks | real hospital manifests and discovery accuracy |
| Adapter maturity registry | **IMPLEMENTED** | FHIR implemented; ISiK validation-path; HL7/vendor/doc/UI paths labelled contract-only | real adapter implementations + compatibility evidence |
| Hospital-local data plane | **IMPLEMENTED — NON-LIVE** | multi-source FHIR-family runtime with source-state and cross-source identity guards | real auth/MPI/vendor runtime + live approval |
| Docker / Helm install scaffold | **IMPLEMENTED — NON-LIVE** | hardened Docker Compose + Kubernetes/Helm shape, read-only config, deny-default egress | validated target-hospital deployment + approved image/release process |
| Upgrade compatibility preflight | **IMPLEMENTED + SYNTHETICALLY TESTED** | interface/identity/provenance/write capability regressions block rollout | real KIS/LIS upgrade history |
| German interoperability | **PARTIAL** | FHIR/ISiK-oriented paths and CI | real KIS/LIS/vendor sandbox |
| EU/global portability | **RESEARCH PROOF** | IPS/trust/translation/state separation | real conformance/exchange evidence |
| Hospital rollout | **PROPOSAL READY** | read-only → shadow → one-ward → copilot evidence ladder | an actual implementation |
| Recare-targeted capstone | **RUNNABLE SYNTHETIC PROOF** | FastAPI + real CareOS gateway/tool/eval path | captured provider-backed trace + production context |
| Real clinician evidence | **EXTERNAL EVIDENCE REQUIRED** | study protocol, counterbalanced UI, export + aggregator | completed clinician sessions |
| Real KIS/LIS integration | **EXTERNAL EVIDENCE REQUIRED** | discovery + manifest + connector contracts | vendor/system access |
| Production PHI operations | **BLOCKED BY DESIGN** | live-data locks + security architecture | hospital identity, KMS, SIEM, DPIA/DPA, operations |
| Multi-hospital repeatability | **NOT YET EVIDENCED** | anti-fork contract + reusable adapter/install scaffold | second independent real site/vendor |

### Claim boundary

**Safe to claim today:**

- a runnable synthetic healthcare-agent architecture;
- source-linked clinical-state semantics;
- explicit uncertainty and contradiction handling;
- deterministic agent authority outside the model;
- adversarial/replayable safety tests;
- FHIR/ISiK-oriented interoperability architecture;
- a runnable non-live hospital manifest/preflight/local-data-plane scaffold;
- explicit adapter implementation maturity rather than implied support;
- Docker/Helm packaging for synthetic/deidentified evaluation;
- fail-closed hospital upgrade compatibility checks;
- clinician-study and hospital-rollout methodology;
- global portability research preserving state/provenance/trust separation.

**Do not claim today:**

- clinical validation;
- production hospital deployment;
- production PHI handling;
- a fully self-service real-hospital install;
- generic HL7 v2 runtime support;
- a CareOS computer-use/KIS Operator implementation;
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
- [x] provider-neutral + direct-provider external-model paths for synthetic/deidentified evaluation;
- [x] machine-readable traces/evals in the Recare capstone;
- [x] six-case Recare containment suite;
- [x] global portability contract + tests;
- [x] non-secret Hospital Capability Manifest;
- [x] deterministic adapter selection + explicit implementation maturity;
- [x] governed cross-source patient-identity preflight;
- [x] hospital-local multi-source FHIR-family runtime for synthetic/deidentified evaluation;
- [x] partial-source behavior that prevents absence claims when context is incomplete;
- [x] one-command CLI surface: init / doctor / preflight / up / down / upgrade-check;
- [x] Docker Compose hospital install scaffold;
- [x] Helm/Kubernetes hospital deployment scaffold;
- [x] hospital upgrade compatibility preflight;
- [x] dedicated self-install CI workflow definition.

### Security / safety design

- [x] wrong-patient denial;
- [x] cross-source identity is explicit rather than assumed;
- [x] cross-scope agent denial;
- [x] prompt-injection containment scenarios;
- [x] source outage / degraded state;
- [x] stale-state handling;
- [x] write/tool escalation denial;
- [x] read and write adapter paths separated;
- [x] workload/delegation/revocation foundations;
- [x] deny-default egress concept + Helm default-deny policy;
- [x] audit foundations;
- [x] kill/release gates;
- [x] code-enforced live-data/live-agent locks;
- [x] hospital-local endpoint/credential values kept outside versionable manifest;
- [x] local hospital files ignored by default;
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
- [x] Recare integration-accelerator hypothesis;
- [x] explicit CareOS endgame / open interoperability fabric;
- [x] Apache-2.0 open-source license + contributor contract.

---

## 3. Remaining gaps we can still engineer without pretending they are proven

### A. Adapter breadth

Current runtime truth:

```text
FHIR R4      = implemented read runtime
ISiK/FHIR    = FHIR runtime + validation path
HL7 v2       = contract-only
vendor API   = contract-only
source feed  = contract-only
a UI bridge  = contract-only
write paths  = contract-only / globally disabled
```

The next adapter work should be triggered by real Recare/hospital integration data where possible. If a generic HL7 v2 adapter is built independently, it must ship with a synthetic conformance suite and remain labelled non-production until exercised against a real interface engine/vendor.

### B. Automatic discovery

The manifest is intentionally explicit today. Useful next automation:

- FHIR `CapabilityStatement` discovery;
- generated source/resource capability suggestions;
- safe interface-engine probes;
- compatibility registry by vendor/product/version;
- generated DPO/CISO network/data-flow artifact;
- Kubernetes/VM overlay generation.

Automation may suggest capabilities; hospital IT remains responsible for confirming identity, purpose, ownership and governance facts that cannot be discovered technically.

### C. Release distribution / fleet upgrade

Need a production-grade path for:

- signed/pinned release images;
- SBOM/provenance verification at install time;
- canary deployment;
- automatic compatibility check against the last-known-good manifest;
- rollback rehearsal;
- non-PHI fleet version/health reporting where hospitals approve it.

### D. Provider-backed synthetic model trace

The provider paths are implemented, but the public evidence package still needs one captured real-provider synthetic run to demonstrate model/version/tool/policy/eval telemetry end to end. Do not fake it with a mock and call it live.

---

## 4. Remaining gaps that require external reality

### A. Real clinician behaviour

Need several complete paired synthetic clinician sessions with actual task time, errors, pending-work misses, source checks, corrections, effort and qualitative friction.

### B. Real KIS / LIS / hospital integration

Need actual vendor/version, one real capability manifest, interface discovery, patient/encounter context launch, source lifecycle behaviour, local terminology, network/latency/partial-read behaviour and an approved sandbox/deidentified boundary.

This is now also the first real test of the self-install hypothesis:

> **How much of deployment is configuration + conformance, and how much still requires custom engineering?**

### C. Hospital privacy / security operations

Need provider evidence for IdP/role/treatment context, KMS/secrets, network controls, audit/SIEM, DLP where required, backup/recovery, AVV/DPA, DSFA/DPIA, processors/subprocessors, incident response and independent penetration testing.

### D. Clinical / regulatory / quality assurance

Need a fixed intended use and deployment context before medical-device applicability, clinical safety governance, QMS/change control, human-factors evidence and EHDS/EHR obligations can be assessed responsibly.

### E. Production GenAI operations

Need real traffic, provider configuration, latency/cost, prompt/model versioning, production traces, user-correction loops, incidents/replay, model migration behaviour and actual SLOs.

### F. Multi-site repeatability

Need:

1. Hospital A real read-only/deidentified source path;
2. Hospital B with a different vendor/version;
3. no fork of the canonical clinical context/agent contracts;
4. measured custom engineering hours/site;
5. measured adapter/test reuse;
6. upgrade regression evidence.

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
| G7 Hospital deployment | **PARTIAL** | self-install scaffold exists; provider approvals/operations missing |
| G8 Repeatability | **NOT EVIDENCED** | second real deployment required |
| G9 Germany/EU scale | **RESEARCH ONLY** | real national/cross-border integration |

No identifiable-live-data gate should be changed merely to improve a demo or installer UX.

---

## 6. What not to build before external feedback

Avoid productivity theatre:

- more specialties with no users;
- fake production integrations;
- claiming a vendor adapter exists because a standard is named in a manifest;
- autonomous diagnosis/treatment logic merely for portfolio breadth;
- another country pack without a real partner;
- a parallel Recare product;
- extra dashboards with no operational consumer;
- invented clinician time savings;
- real patient data used to accelerate evidence.

Scaling infrastructure is worth building only when it reduces repeat deployment work or turns a known failure mode into a reusable test.

---

## 7. Highest-value next actions

1. **Recare/Pavlo integration critique** — learn what their real adapter/implementation architecture already does.
2. **Clinician synthetic sessions** — collect actual paired behaviour.
3. **First real hospital capability manifest** — fill it with hospital IT without touching live patient data.
4. **Approved synthetic/deidentified KIS/LIS sandbox** — test the FHIR path and discover actual gaps.
5. **Measure integration economics** — hours, custom code, adapter reuse, conformance failures.
6. **Implement the highest-frequency real missing adapter** — probably only after seeing real integration demand.
7. **Shadow workflow**.
8. **Second site/vendor** — the first true proof of infrastructure scaling.

---

## Definition of “pre-hospital phase complete”

The pre-hospital phase is complete when the problem is concrete, one workflow is usable synthetically, trust boundaries and failure states are explicit, adversarial tests exist, model authority is bounded, interoperability direction is standards-aligned, rollout methodology and outcome metrics are explicit, and a plausible repeatable deployment contract exists without pretending it has been proven in hospitals.

CareOS now satisfies that definition.

> **The honest gap is no longer imagination. It is external evidence — especially whether the self-install/adapter model survives real hospital systems.**
