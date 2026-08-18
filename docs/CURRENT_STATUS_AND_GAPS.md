# CareOS Current Status & Gap Register

Baseline: **18 August 2026**

> Purpose: separate what has genuinely been built from what still requires clinicians, hospitals, vendors, production infrastructure or external assurance.

## Executive status

CareOS is now best described as:

> **synthetic product research + runnable engineering proof + proposal-ready reference architecture + hospital implementation playbook**

It is **not** clinically validated, production approved or authorised for identifiable live patient data.

The most important conclusion is that the remaining high-value gaps are increasingly **external evidence gaps**, not missing speculative features.

---

# 1. Re-rating

| Dimension | Current rating | Why |
|---|---:|---|
| Problem understanding | **10 / 10** | clear clinician/admin problem and measurable outcome |
| Product thinking | **9.5 / 10** | workflow-first, role-aware, explicit failure states |
| Clinical UX concept | **9.2 / 10** | source-linked synthetic workflow; needs real user evidence |
| Clinical truth / provenance architecture | **9.6 / 10** | source/time/state/contradiction are first-class |
| Agent safety architecture | **9.6 / 10** | model is untrusted; authority outside model; bounded tools/budgets |
| Adversarial evaluation | **9.5 / 10** | hostile/wrong-patient/outage/stale/write cases are replayable |
| German interoperability architecture | **9.3 / 10** | FHIR/ISiK path + national map; real vendor evidence missing |
| EU/global portability architecture | **9.1 / 10** | IPS/trust/translation/state separation; conformance + real exchange missing |
| Hospital rollout methodology | **9.4 / 10** | read-only/shadow/pilot/evidence ladder now explicit |
| Recare-targeted work sample | **9.6 / 10** | real components composed into runnable synthetic capstone |
| Real clinician evidence | **2 / 10** | study exists; real paired sessions still needed |
| Real KIS/LIS integration | **1 / 10** | interface architecture and synthetic validation only |
| Production PHI operations | **0 / 10** | intentionally locked |
| Multi-hospital deployment evidence | **0 / 10** | requires deployments |

Two roll-up ratings:

- **Ready for serious Recare / engineering / hospital architecture discussion:** **~9.8 / 10**
- **Ready for live hospital production deployment:** **~4 / 10**

The second score should stay low until external evidence exists.

---

# 2. Gaps closed as far as responsibly possible outside a hospital

## Clinical/product

- [x] one concrete first specialty/workflow;
- [x] clinician-first information hierarchy;
- [x] source-linked facts;
- [x] pending/unavailable/contradiction semantics;
- [x] human review/approval boundaries;
- [x] clinician study protocol/UI;
- [x] structured anonymous result export;
- [x] study aggregator where safety gates override speed.

## Engineering

- [x] Python/FastAPI/Pydantic backend;
- [x] FHIR integration path;
- [x] ISiK-oriented validation path;
- [x] typed clinical truth contracts;
- [x] conservative evidence verification;
- [x] agent runtime and deterministic gateway;
- [x] trusted tool proxy;
- [x] provider-neutral external model adapter for synthetic/deidentified evaluation;
- [x] machine-readable traces/evals in Recare capstone;
- [x] six-case Recare containment suite;
- [x] focused CI workflow;
- [x] global portability contract + tests;
- [x] global interoperability CI.

## Security / safety design

- [x] wrong-patient denial;
- [x] cross-scope agent denial;
- [x] prompt-injection containment scenarios;
- [x] source outage/degraded state;
- [x] stale-state handling;
- [x] write/tool escalation denial;
- [x] workload/delegation/revocation foundations;
- [x] deny-default egress concept;
- [x] audit foundations;
- [x] kill/release gates;
- [x] code-enforced live-data/live-agent locks;
- [x] dependency lock, container and supply-chain foundations.

## Architecture / governance

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
- [x] Recare overlap/collaboration map.

---

# 3. Remaining gaps that require real external access

## A. Real clinician behavior

Need:

- at least several complete paired synthetic clinician sessions;
- observed workflow behavior rather than hypothetical feedback;
- real time/error/source-check/correction metrics;
- qualitative implementation friction;
- ideally multiple clinician roles.

Cannot be substituted by more synthetic code.

## B. Real KIS / LIS / hospital integration

Need:

- actual vendor/version;
- real interface capability discovery;
- source lifecycle behavior;
- patient/encounter context launch;
- local code/terminology mapping;
- network/latency/partial-read behavior;
- real sandbox/deidentified fixtures;
- interface support escalation paths.

Cannot be inferred reliably from public standards alone.

## C. Hospital identity / privacy / security operations

Need provider evidence for:

- IdP / role / organisational identity;
- treatment-context assertions;
- KMS/secrets;
- network segmentation / proxies / egress;
- audit/SIEM integration;
- DLP if required;
- backup/recovery;
- AVV/DPA;
- DSFA/DPIA;
- processor/subprocessor review;
- operational incident management;
- independent penetration testing.

## D. Clinical / regulatory / quality assurance

Need the final intended use and deployment to determine:

- medical-device / software classification applicability;
- clinical safety governance;
- formal quality lifecycle;
- human-factors evidence;
- change-control expectations;
- EHDS/EHR-system obligations where applicable;
- hospital-specific legal assessment.

Do not guess these before intended use is fixed.

## E. Production GenAI experience

Need:

- real traffic patterns;
- production model/provider configuration;
- token/cost/latency observations;
- prompt/model versioning in operations;
- production traces;
- user corrections linked to evals;
- incident/replay workflows;
- model migration behavior;
- actual reliability and availability targets.

## F. Multi-site repeatability

Need:

- second ward/specialty;
- second KIS/vendor configuration;
- second hospital;
- measured connector effort;
- evidence that core contracts survive without forks.

---

# 4. Current production gates

The repository's production-gate posture remains intentionally conservative.

| Gate | State | Why it cannot close synthetically |
|---|---|---|
| G0 Scope & clinical safety | external review | intended use + independent clinical review |
| G1 Clinical truth | blocked | recall/review burden + real workflow evidence |
| G2 German interoperability | partial | real vendor/sandbox needed |
| G3 Privacy & security | partial | provider controls + independent evidence |
| G4 Reliability | partial | target-environment load/recovery/SLO |
| G5 Regulatory & quality | external review | classification / QMS lifecycle |
| G6 Invisible workflow | partial | actual KIS-context launch |
| G7 Hospital deployment | partial | provider approvals and operations |
| G8 Repeatability | partial | second deployment |
| G9 Germany/EU scale | blocked | real national/cross-border integrations |

No identifiable-live-data gate should be changed merely to improve a demo.

---

# 5. What not to do now

Avoid productivity theatre:

- adding more specialties with no users;
- inventing fake production integrations;
- claiming standards conformance where only a preview exists;
- claiming a CI run was green unless verified;
- inventing clinician time savings;
- using real patient data to accelerate evidence;
- building a parallel Recare product merely to make the portfolio larger;
- implementing country-specific features without a real use case;
- turning every architecture idea into product code before external feedback.

---

# 6. Highest-value next actions

In order:

1. **External engineering critique** — Recare/Pavlo or equivalent production team.
2. **Clinician synthetic sessions** — collect real paired behavior.
3. **Workflow observation** — watch real hospital work before proposing more product.
4. **Technical discovery** — KIS/LIS/identity/network/governance.
5. **Synthetic/deidentified integration sandbox**.
6. **Shadow workflow**.
7. **Read-only pilot only when gates permit**.
8. **Second site/vendor**.

---

# 7. Definition of “pre-hospital phase complete”

We consider the pre-hospital phase complete when:

- the problem is concrete;
- one workflow is usable synthetically;
- the architecture has clear trust boundaries;
- failure states are modeled;
- adversarial tests exist;
- model authority is bounded;
- interoperability direction is standards-aligned;
- deployment/rollout methodology is explicit;
- success metrics are measurable;
- limitations are documented;
- the remaining uncertainties require external reality.

CareOS now satisfies that definition.

> **The honest gap is no longer imagination. It is access.**
