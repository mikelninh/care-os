<div align="center">

# CareOS

### **Return time to care — without making clinical information less trustworthy.**

A clinician-first research architecture for turning fragmented hospital data into **source-linked, reviewable clinical context** for humans and bounded AI agents.

[**▶ Explore CareOS**](https://mikelninh.github.io/careos/) · [**▶ Clinician demo**](https://mikelninh.github.io/careos/sjk/) · [**▶ Recare work sample**](https://mikelninh.github.io/recare/) · [**Contribute**](CONTRIBUTING.md)

[![tests](https://github.com/mikelninh/care-os/actions/workflows/test.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/test.yml)
[![recare-capstone](https://github.com/mikelninh/care-os/actions/workflows/recare-capstone.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/recare-capstone.yml)
[![agent-redteam](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml)
[![global-interoperability](https://github.com/mikelninh/care-os/actions/workflows/global-interoperability.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/global-interoperability.yml)
[![license](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Synthetic / pre-hospital research only · not for clinical use · no identifiable patient data in public demos · no production write-back**

</div>

---

## CareOS in 10 seconds

Hospitals already have KIS/EHR, LIS, RIS/PACS, documents, ePA and other systems of record.

**CareOS does not replace them.** It explores the missing context and assurance layer between fragmented sources and clinical work.

```text
KIS · LIS · FHIR · documents · ePA
                ↓
        source-linked context
 identity · provenance · time · state
 contradiction · freshness · pending work
                ↓
       deterministic policy boundary
          ↙                    ↘
     clinician UX          bounded agent
          ↘                    ↙
             human decision
```

The question is deliberately simple:

> **Can clinicians spend less time hunting, reconciling and re-entering information without losing provenance, uncertainty or human control?**

North star: **Time Returned to Care — safety gated.**

---

## Four invariants

| | CareOS rule |
|---|---|
| **01** | **Pending ≠ negative.** |
| **02** | **Unavailable ≠ absent.** |
| **03** | **Documented therapy ≠ AI recommendation.** |
| **04** | **Agent draft ≠ source truth.** |

These are treated as correctness constraints, not UI decoration.

---

## Start here

| You are… | Open this |
|---|---|
| **Recare / AI engineering** | [90-second Recare work sample](https://mikelninh.github.io/recare/) → [runnable capstone](docs/RECARE_CAPSTONE.md) |
| **Clinician** | [Synthetic Infectiology workflow](https://mikelninh.github.io/careos/sjk/) |
| **Testing usefulness** | [Paired synthetic clinician A/B study](https://mikelninh.github.io/careos/sjk/ab.html) |
| **Software engineer / designer / researcher** | [Contributing guide](CONTRIBUTING.md) → [community roadmap](docs/COMMUNITY_ROADMAP.md) |
| **Hospital implementation** | [Zero-Drama Hospital Rollout](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md) |
| **CIO / CISO / senior engineer** | [Reference Architecture V2](docs/ARCHITECTURE_V2.md) |
| **Checking readiness / claims** | [Current Status & Gap Register](docs/CURRENT_STATUS_AND_GAPS.md) |
| **Germany / public sector** | [National / EU Integration Map](docs/NATIONAL_INTEGRATION_MAP.md) |
| **EU / global interoperability** | [Germany → Global Health Interoperability Blueprint](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md) |
| **Reviewing the whole project** | [Pre-Hospital Handoff](docs/PRE_HOSPITAL_HANDOFF.md) |

---

## What is actually built

### 1 · A clinician workflow

The first synthetic workflow is Infectiology: microbiology lifecycle, documented anti-infective therapy, hygiene/isolation context, trends, contradictions, pending work and source-linked handover/documentation drafts.

<div align="center">
  <img src="docs/screenshots/sjk-clinician-current.svg" alt="CareOS synthetic Infectiology clinician interface" width="820">
</div>

The paired study measures **task time, wrong answers, missed pending work, source checking, corrections, effort and verification decay** — not whether users simply like the UI.

### 2 · Clinical truth with provenance

A consequential surfaced fact can retain:

```text
patient + encounter binding
source organisation / system / resource
original value / wording
clinical effective time
recorded / ingestion time
version + freshness
preliminary / final / corrected / cancelled / pending / stale / unavailable
terminology + unit mapping lineage
evidence span for document-derived facts
contradiction / supersession / review state
```

The model may propose structure. **It does not become the authority that creates trusted clinical truth.**

#### Frozen synthetic holdout

| Metric | Result |
|---|---:|
| Precision | **100%** |
| Provenance coverage | **100%** |
| Unsupported claims | **0** |
| Wrong-source claims | **0** |
| Recall | **26.32%** |
| Review case rate | **100%** |

This is deliberately **not a production pass**. The conservative path recalls too little and creates too much review burden, so **G1 remains blocked**.

[Benchmark details →](docs/BENCHMARK.md)

### 3 · A zero-trust agent boundary

CareOS assumes the reasoning model can be wrong or compromised.

```text
approved workflow
      ↓ narrow delegation
agent identity
      ↓
┌──────────────────────────────┐
│ deterministic Agent Gateway │
│ patient / encounter binding │
│ allowed tools + operations  │
│ data categories + budgets   │
│ deny-default egress         │
│ audit + revocation          │
└──────────────┬───────────────┘
               ↓ admitted call only
        trusted Tool Proxy
               ↓
        source-linked result
               ↓
       untrusted draft
               ↓
        human review
```

The reasoning worker cannot grant itself a different patient, tool, network destination, break-glass state or write permission.

[Agent Security Model →](docs/AGENT_SECURITY_MODEL.md)

### 4 · Replayable failure tests

The Recare capstone exercises the real CareOS gateway/tool/draft/eval path against synthetic scenarios:

| Scenario | Safe behaviour |
|---|---|
| Happy path | source-linked draft, review required |
| Wrong patient | reject foreign context before use |
| Prompt injection | document text cannot expand authority |
| Source unavailable | degrade visibly; suppress dependent claims |
| Stale result | preserve old vs current-pending distinction |
| Unauthorised write | deny capability escalation |

A hostile run that is correctly blocked counts as a **safety success**, not failed completion.

[Run the Recare capstone →](docs/RECARE_CAPSTONE.md)

---

## Evidence state, not self-scores

CareOS reports what has been demonstrated rather than awarding itself maturity numbers.

| Area | Current evidence state |
|---|---|
| Clinician workflow | **DEMONSTRATED SYNTHETICALLY** |
| Clinical truth / provenance | **DEMONSTRATED SYNTHETICALLY** |
| Agent containment | **DEMONSTRATED SYNTHETICALLY** |
| Adversarial evaluation | **DEMONSTRATED SYNTHETICALLY** |
| German interoperability | **PARTIAL — real vendor sandbox required** |
| EU/global portability | **RESEARCH PROOF** |
| Hospital rollout | **PROPOSAL READY** |
| Recare capstone | **RUNNABLE SYNTHETIC PROOF** |
| Real clinician evidence | **EXTERNAL EVIDENCE REQUIRED** |
| Real KIS/LIS integration | **EXTERNAL EVIDENCE REQUIRED** |
| Production PHI operations | **BLOCKED BY DESIGN** |
| Multi-hospital repeatability | **NOT YET EVIDENCED** |

[Full evidence and gap register →](docs/CURRENT_STATUS_AND_GAPS.md)

---

## Interoperability: connect, don't replace

```text
provider systems
     ↓
FHIR / ISiK / HL7 / vendor adapters
     ↓
trusted clinical context
     ↓
Germany: ePA / TI where appropriate
     ↓
EU: EHDS / European exchange
     ↓
Global: FHIR / International Patient Summary + trust
```

The portability work deliberately separates:

1. **Content** — what does the clinical item mean?
2. **Trust** — who issued it and can that issuer be verified?
3. **Policy** — may the receiving context use it for this purpose?

A pending result in Berlin must remain **pending** after translation or exchange. Translation may change presentation — never source truth.

[Germany → Global Interoperability Blueprint →](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md)

---

## Hospital rollout: zero drama

```text
observe real workflow
        ↓
technical + governance preflight
        ↓
read-only context
        ↓
shadow mode
        ↓
one workflow / one ward
        ↓
human-approved copilot
        ↓
bounded execution only when earned
        ↓
measure benefit + safety
        ↓
second ward / vendor / hospital
```

Installation is not the outcome. A rollout earns expansion only when it removes work **without worse verification, corrections, missed pending items or safety behaviour**.

[Hospital Implementation Playbook →](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md)

---

## Recare: collaborate, don't duplicate

Recare already operates the real product layer across hospital workflows. CareOS is **not** a proposal to replace it.

The useful question is:

> **Which CareOS invariants, evals and implementation patterns survive contact with Recare's real integrations and hospitals — and make the existing platform stronger?**

The CareOS prototype also has a deliberately narrower authority boundary than Recare's full production product scope. That is intentional: this repository is an R&D/evaluation artifact, not a claim of equivalent production maturity.

[Recare × CareOS Collaboration Map →](docs/RECARE_COLLABORATION_MAP.md)

---

## Build with us

> **We are all in this together.**

Healthcare is too important and too interconnected for one person, company or discipline to solve alone. CareOS welcomes careful contributions from **software engineers, clinicians, designers, security researchers, interoperability specialists, data scientists, product thinkers and people with lived experience of broken healthcare workflows**.

Start with one bounded problem:

- 🟢 accessibility, mobile UX, synthetic fixtures, documentation;
- 🔵 clinician workflow, source inspection, trace tooling;
- 🟣 FHIR / ISiK / IPS / terminology / cross-border interoperability;
- 🔴 agent security, prompt injection, patient isolation, audit integrity;
- 🟠 evals, recall-vs-review burden, clinician-study analysis;
- 🌍 country packs, portability and low-bandwidth global health.

> **Find one piece of friction or one way the system can fail → make it better → show the evidence.**

[**How to contribute →**](CONTRIBUTING.md) · [**Pick a problem →**](docs/COMMUNITY_ROADMAP.md) · [**Open issues →**](https://github.com/mikelninh/care-os/issues) · [**Apache-2.0 license →**](LICENSE)

---

## What happens next

```text
external engineering critique
        ↓
synthetic clinician sessions
        ↓
real workflow mapping
        ↓
deidentified KIS / LIS sandbox
        ↓
hospital IT + privacy + security review
        ↓
shadow workflow
        ↓
limited live read-only pilot — only when gates allow
        ↓
second hospital / different vendor
```

More speculative features are now lower value than external evidence.

---

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.lock
uvicorn app.main:app --reload
```

Recare capstone:

```bash
uvicorn app.recare_api:app --reload --port 8010
```

Then inspect `GET /api/eval-suite` or `POST /api/run`.

---

## Deep review index

| Need | Evidence |
|---|---|
| Whole pre-hospital bundle | [Pre-Hospital Handoff](docs/PRE_HOSPITAL_HANDOFF.md) |
| Current gaps / readiness | [Current Status & Gaps](docs/CURRENT_STATUS_AND_GAPS.md) |
| Recare collaboration | [Recare Collaboration Map](docs/RECARE_COLLABORATION_MAP.md) |
| Recare executable proof | [Recare Capstone](docs/RECARE_CAPSTONE.md) |
| Hospital rollout | [Implementation Playbook](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md) |
| Logical architecture | [Architecture V2](docs/ARCHITECTURE_V2.md) |
| National / EU integration | [Integration Map](docs/NATIONAL_INTEGRATION_MAP.md) |
| Germany → global | [Global Blueprint](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md) |
| Agent threat model | [Agent Security Model](docs/AGENT_SECURITY_MODEL.md) |
| Safety / assurance | [Safety Case](docs/SAFETY_CASE.md) · [Assurance Crosswalk](docs/ASSURANCE_CROSSWALK.md) |
| Full evidence index | [Technical Documentation Index](docs/TECHNICAL_DOCUMENTATION_INDEX.md) |

---

<div align="center">

### **Keep systems of record. Standardize trustworthy context above them.**

*Models may interpret and propose. Evidence, authority and safety boundaries remain outside the model.*

</div>
