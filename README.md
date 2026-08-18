# CareOS

> **Patient history without the hunt. Document once, reuse safely.**

[![tests](https://github.com/mikelninh/care-os/actions/workflows/test.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/test.yml)
[![platform-redteam](https://github.com/mikelninh/care-os/actions/workflows/platform-redteam.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/platform-redteam.yml)
[![agent-redteam](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml)
[![recare-capstone](https://github.com/mikelninh/care-os/actions/workflows/recare-capstone.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/recare-capstone.yml)
[![global-interoperability](https://github.com/mikelninh/care-os/actions/workflows/global-interoperability.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/global-interoperability.yml)
[![supply-chain](https://github.com/mikelninh/care-os/actions/workflows/supply-chain-security.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/supply-chain-security.yml)

CareOS is a **clinician-first, federated clinical-context research architecture** for fragmented healthcare systems.

It sits conceptually beside KIS/PVS/EHR/LIS/RIS/ePA systems rather than replacing them: bring the relevant patient story together, keep consequential information traceable to its source, preserve uncertainty and pending work, and return time to care without creating another system of record.

**First specialty:** Infectiology  
**Current stage:** **pre-hospital synthetic phase complete enough for serious external review; real-world validation is next**  
**Safety boundary:** synthetic/public prototype only · not for clinical use · no identifiable patient data in public demos · no production write-back

---

# Start here

| If you are… | Start with… |
|---|---|
| reviewing the whole project | **[Pre-Hospital Handoff](docs/PRE_HOSPITAL_HANDOFF.md)** |
| Recare / healthcare AI engineering | **[Recare Collaboration Map](docs/RECARE_COLLABORATION_MAP.md)** + **[Recare Capstone](docs/RECARE_CAPSTONE.md)** |
| a clinician / Infectiology team | **[Synthetic workflow demo](https://mikelninh.github.io/careos/sjk/)** |
| testing clinician usefulness | **[Paired synthetic A/B study](https://mikelninh.github.io/careos/sjk/ab.html)** |
| medical leadership | **[Leadership view](https://mikelninh.github.io/careos/sjk/chef.html)** |
| implementing in a hospital | **[Hospital Implementation Playbook](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md)** |
| senior engineering / CIO / CISO / Datenschutz | **[Reference Architecture V2](docs/ARCHITECTURE_V2.md)** |
| checking what is actually ready | **[Current Status & Gaps](docs/CURRENT_STATUS_AND_GAPS.md)** |
| German public sector / gematik / policy | **[Government Reference Architecture](docs/GOVERNMENT_REFERENCE_ARCHITECTURE.md)** |
| EU / global interoperability | **[Germany → Global Interoperability Blueprint](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md)** |

Public Recare-targeted work sample: **https://mikelninh.github.io/recare/**

---

# The question

> **Can we make clinicians materially faster without making clinical information less trustworthy or reducing source verification?**

CareOS treats usefulness and safety as one outcome, not two independent scorecards.

A time saving does **not** compensate for:

- wrong-patient context;
- unsupported clinical claims;
- pending information being interpreted as negative/complete;
- stale information being presented as current;
- source failure being interpreted as absence;
- agent output being confused with source truth;
- unauthorised clinical write/send behavior.

North-star outcome: **Time Returned to Care — safety gated.**

---

# What exists right now

## 1. Clinician workflow

- synthetic Infectiology morning-review / discharge-prep workflows;
- microbiology, medication, hygiene/isolation, trends and open tasks;
- source-linked clinical facts;
- explicit review and contradiction states;
- source jumps / evidence inspection;
- paired clinician study measuring time, errors, pending-work retention, source checks, corrections, effort and verification decay;
- local-only pseudonymous JSON/CSV study export + paired aggregator.

Core clinical semantics:

> **Pending ≠ negative. Unavailable ≠ absent. Stale ≠ current. Documented therapy ≠ AI recommendation.**

## 2. Clinical truth / evidence

A surfaced fact is designed to preserve:

```text
patient / encounter binding
source organisation / system / resource
original value / wording
clinical effective time
recorded / ingestion time
version / freshness
preliminary / final / corrected / cancelled / pending / stale / unavailable state
terminology / units / mapping lineage
evidence span where document-derived
contradiction / supersession / review state
```

Models may propose structure but do **not** become the authority that creates trusted clinical truth.

### Frozen synthetic holdout

| Metric | Result |
|---|---:|
| Precision | **100%** |
| Provenance coverage | **100%** |
| Unsupported claims | **0** |
| Wrong-source claims | **0** |
| Critical silent field misses | **0** |
| Critical silent contradiction misses | **0** |
| Recall | **26.32%** |
| Review case rate | **100%** |

This is deliberately **not** called a production pass. The conservative truth path fails safely but currently recalls too little and creates too much review burden. G1 therefore remains blocked.

See [Benchmark](docs/BENCHMARK.md).

## 3. German interoperability

- FHIR transport and bounded pagination;
- FHIR source-state handling;
- ISiK-oriented structural/profile validation;
- vendor-neutral connector boundary;
- explicit patient/encounter context;
- integration map for ISiK / ISiP / TI / ePA / KIM / EHDS;
- no attempt to replace national infrastructure.

Architecture rule:

> **Keep systems of record. Standardize trustworthy context above them.**

See [National / EU Integration Map](docs/NATIONAL_INTEGRATION_MAP.md).

## 4. Zero-trust agent runtime

CareOS assumes the reasoning model can be wrong or compromised.

```text
clinician / approved workflow
        ↓ narrow delegation
workload identity
        ↓
┌──────────────────────────────────┐
│       CAREOS AGENT GATEWAY       │
│ identity + revocation            │
│ patient/encounter/task binding   │
│ versioned tool registry          │
│ deterministic authorization      │
│ record/page/tool/runtime budgets │
│ deny-default egress              │
│ audit                            │
└──────────────┬───────────────────┘
               │ admitted request only
               ▼
       trusted Tool Proxy
               │
               ▼
       source-linked result
               │
               ▼
      untrusted draft candidate
               │
               ▼
          draft firewall
               │
               ▼
          human review
```

The model cannot authoritatively choose a different patient, encounter, organisation, break-glass state, arbitrary tool, network destination or write permission.

See:

- [Agent Security Model](docs/AGENT_SECURITY_MODEL.md)
- [Agent Production Programme](docs/AGENT_PRODUCTION_PROGRAM.md)
- [Agent Phases 1–7](docs/AGENT_PHASES_1_7.md)

## 5. Recare-targeted runnable capstone

The hiring/work-sample layer composes the real CareOS components into one synthetic clinical task.

API surface:

```text
GET  /health
GET  /api/capabilities
GET  /api/eval-suite
POST /api/run
```

Six regression scenarios:

- happy path;
- wrong patient;
- prompt injection;
- source unavailable;
- stale result;
- unauthorised write.

A hostile run that is correctly denied counts as a **safety pass**, not as a failed completion.

The provider-neutral external-model adapter can be enabled for synthetic/deidentified evaluation without changing the deterministic authority boundary.

See [Recare Capstone](docs/RECARE_CAPSTONE.md).

## 6. Global portability

CareOS now separates three interoperability questions:

```text
CONTENT — what does this clinical information mean?
TRUST   — who issued it and can that issuer be verified?
POLICY  — may the receiving context use it for this purpose?
```

The global portability prototype preserves:

- original clinical wording/language;
- clinical state;
- provenance;
- terminology mappings;
- translated presentation separately from source truth;
- issuer trust state separately from data-format validity.

So a result that is **pending in Berlin remains pending after translation or cross-border exchange**; a contradiction remains a contradiction; an unverified issuer stays visibly unverified.

Target direction:

```text
Provider / hospital
        ↓
Germany: FHIR / ISiK / ePA / TI
        ↓
EU: EHDS / EEHRxF / MyHealth@EU
        ↓
Global: FHIR / International Patient Summary + trust verification
```

See [Germany as a Global Health Interoperability Reference Model](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md).

---

# Recare: collaborate, do not duplicate

Publicly, Recare already offers substantial parts of the clinical product layer CareOS independently converged toward: Patient Overview, Extract, Docs, Voice, Agent, Operator, Discharge and Predict.

Therefore the intended posture is **not**:

> "Replace Recare's product with CareOS."

It is:

> **Bring the clinical-state, provenance, agent-authority, adversarial-eval, interoperability and implementation work into contact with a real production platform; retire duplicate ideas; keep only what survives reality.**

The collaboration map includes a 30/60/90-day plan centered on real integrations and hospital implementation.

See [Recare x CareOS Collaboration Map](docs/RECARE_COLLABORATION_MAP.md).

---

# Hospital rollout: zero drama

The implementation path is now explicit:

```text
0. observe the real workflow
        ↓
1. technical / governance preflight
        ↓
2. read-only context
        ↓
3. shadow mode
        ↓
4. one workflow / one ward
        ↓
5. human-approved copilot
        ↓
6. legacy bridge where necessary
        ↓
7. bounded execution only when earned
        ↓
8. measure benefit + safety
        ↓
9. second ward / vendor / hospital
```

Default integration preference:

1. FHIR / ISiK / HL7 where appropriate;
2. stable vendor API;
3. provider integration engine;
4. controlled file/document path;
5. computer-use/UI automation as a pragmatic legacy bridge, with its different risks made explicit.

See [Hospital Implementation Playbook](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md).

---

# Germany as an international reference model

CareOS proposes that Germany should **not** build another proprietary national EHR or integration bus.

Instead, combine strong ideas already demonstrated internationally:

- Estonia: auditability / once-only / citizen transparency;
- Finland: executable interoperability certification;
- Denmark: national services embedded into local clinical software;
- Netherlands: technical standards + shared trust framework;
- NHS England: standardised AI assurance with local deployment accountability;
- Germany/EU: ISiK/ePA/TI/EHDS foundations;
- global: FHIR / IPS + verifiable issuer/trust boundaries.

The proposed German reference model adds:

- **Open Clinical Context Contract**;
- national executable conformance lab;
- patient/clinician transparency ledger including agents;
- machine-readable **Agent Capability Manifest**;
- **Time Returned to Care** as a procurement/outcome contract;
- global portability without product lock-in.

See [Germany → Global Health Interoperability Blueprint](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md).

---

# Current readiness — honest version

CareOS graduates by **evidence**, not version numbers.

| Dimension | Status |
|---|---:|
| Problem understanding | **10 / 10** |
| Product thinking | **9.5 / 10** |
| Clinical truth / provenance architecture | **9.6 / 10** |
| Agent safety architecture | **9.6 / 10** |
| Adversarial evaluation | **9.5 / 10** |
| German interoperability architecture | **9.3 / 10** |
| EU/global portability architecture | **9.1 / 10** |
| Hospital rollout methodology | **9.4 / 10** |
| Recare-targeted work sample | **9.6 / 10** |
| Real clinician evidence | **2 / 10** |
| Real KIS/LIS integration | **1 / 10** |
| Production PHI operations | **0 / 10** |
| Multi-hospital deployment evidence | **0 / 10** |

Two different questions:

- **Ready for serious Recare / hospital / architecture discussion:** ~**9.8 / 10**
- **Ready for a live hospital production deployment:** ~**4 / 10**

That gap is intentional and honest. The missing evidence now requires real clinicians, actual hospital systems, provider security/privacy infrastructure, formal review and deployment experience.

See [Current Status & Gap Register](docs/CURRENT_STATUS_AND_GAPS.md).

---

# Production-readiness gates

| Gate | Current state | Main remaining evidence |
|---|---|---|
| G0 Scope & clinical safety | **EXTERNAL REVIEW** | intended use + independent clinical-safety assessment |
| G1 Clinical truth | **BLOCKED** | higher recall with low review burden + preserved safety |
| G2 German interoperability | **PARTIAL** | real KIS/LIS/vendor sandbox + terminology/sync evidence |
| G3 Privacy & security | **PARTIAL** | provider IdP/KMS/audit/DSFA/pentest evidence |
| G4 Reliability | **PARTIAL** | target-environment load/recovery/SLO evidence |
| G5 Regulatory & quality | **EXTERNAL REVIEW** | formal applicability/classification + quality lifecycle |
| G6 Invisible workflow | **PARTIAL** | real KIS patient-context launch/no-second-search proof |
| G7 Hospital deployment | **PARTIAL** | provider-specific review and approvals |
| G8 Repeatability | **PARTIAL** | second hospital/vendor without core fork |
| G9 Germany/EU scale | **BLOCKED** | real national/EU + multi-site evidence |

**No normal production gate is PASS. Identifiable live patient data remains locked.**

`CAREOS_DATA_MODE=live-readonly` refuses startup while G0–G5 are incomplete. Transactional/write-back mode remains unsupported.

See [GATES](docs/GATES.md) and [Hospital Assurance Pack](docs/HOSPITAL_ASSURANCE_PACK.md).

---

# Architecture / assurance package

| Question | Document |
|---|---|
| Canonical pre-hospital bundle | [Pre-Hospital Handoff](docs/PRE_HOSPITAL_HANDOFF.md) |
| Current score + remaining gaps | [Current Status & Gaps](docs/CURRENT_STATUS_AND_GAPS.md) |
| Recare overlap / collaboration | [Recare Collaboration Map](docs/RECARE_COLLABORATION_MAP.md) |
| Recare runnable agent work sample | [Recare Capstone](docs/RECARE_CAPSTONE.md) |
| Hospital rollout | [Hospital Implementation Playbook](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md) |
| Full logical architecture | [Reference Architecture V2](docs/ARCHITECTURE_V2.md) |
| German public-sector model | [Government Reference Architecture](docs/GOVERNMENT_REFERENCE_ARCHITECTURE.md) |
| Germany → global strategy | [Global Interoperability Blueprint](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md) |
| ISiK / TI / ePA / EHDS path | [National / EU Integration Map](docs/NATIONAL_INTEGRATION_MAP.md) |
| PHI / trust boundaries / flows | [Trust & Data Flow](docs/TRUST_AND_DATA_FLOW.md) |
| Deployment patterns | [Deployment Patterns](docs/DEPLOYMENT_PATTERNS.md) |
| Agent threat / authority model | [Agent Security Model](docs/AGENT_SECURITY_MODEL.md) |
| Safety evidence | [Safety Case](docs/SAFETY_CASE.md) |
| Assurance evidence | [Assurance Crosswalk](docs/ASSURANCE_CROSSWALK.md) |
| Who owns which controls | [Responsibility Model](docs/RESPONSIBILITY_MODEL.md) |
| Vendor-neutral procurement | [Procurement Requirements](docs/PROCUREMENT_REQUIREMENTS.md) |
| Technical evidence index | [Technical Documentation Index](docs/TECHNICAL_DOCUMENTATION_INDEX.md) |
| Durable decisions | [Architecture Decision Records](docs/adr/README.md) |
| Machine-readable architecture | [`architecture/reference-architecture.json`](architecture/reference-architecture.json) |

---

# Validation ladder

```text
external engineering critique
        ↓
paired clinician synthetic evidence
        ↓
real workflow observation
        ↓
hospital / KIS / LIS / security discovery
        ↓
synthetic or deidentified integration sandbox
        ↓
independent clinical / privacy / security / regulatory review
        ↓
shadow workflow
        ↓
limited read-only pilot — only when gates permit
        ↓
second ward / vendor / hospital
```

**More synthetic feature breadth is no longer the highest-value next move.**

The remaining uncertainties now require contact with reality.

---

# Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.lock
uvicorn app.main:app --reload
```

Useful endpoints:

- clinician UI: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`
- normal gate board: `http://127.0.0.1:8000/api/readiness/gates`
- agent gate board: `http://127.0.0.1:8000/api/readiness/agents`
- data-mode lock: `http://127.0.0.1:8000/api/readiness/data-mode`

Recare capstone:

```bash
uvicorn app.recare_api:app --reload --port 8010
```

- health: `http://127.0.0.1:8010/health`
- capabilities: `http://127.0.0.1:8010/api/capabilities`
- eval suite: `http://127.0.0.1:8010/api/eval-suite`

---

# Safety status

**Synthetic/public prototype only. Not for clinical use.**

CareOS currently performs no production clinical writes, makes no autonomous diagnosis/treatment decisions, does not silently merge ambiguous patients, keeps source failure and uncertainty explicit, and refuses identifiable live-patient startup while core assurance gates are incomplete.

README visuals elsewhere in the repository are synthetic previews, not clinical screenshots. See [`docs/screenshots/README_SCREENSHOTS_NOTE.md`](docs/screenshots/README_SCREENSHOTS_NOTE.md).

> **Pre-hospital phase: complete enough to stop inventing and start learning from real users, integrations and implementation.**
