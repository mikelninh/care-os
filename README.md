<div align="center">

# CareOS

### **Return time to care — without making clinical information less trustworthy.**

A clinician-first interoperability and assurance layer that sits **beside existing hospital systems**, turns fragmented sources into source-linked clinical context, and exposes that context safely to humans and bounded AI applications.

[**▶ Explore CareOS**](https://mikelninh.github.io/careos/) · [**▶ Clinician demo**](https://mikelninh.github.io/careos/sjk/) · [**▶ Recare work sample**](https://mikelninh.github.io/recare/) · [**Endgame**](docs/ENDGAME.md) · [**Contribute**](CONTRIBUTING.md)

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

**CareOS does not replace them.** The target is to make each hospital progressively upgradeable without a big-bang migration:

```text
legacy KIS · LIS · RIS/PACS · documents · ePA
                        ↓
                 reusable adapters
           ISiK/FHIR · FHIR · HL7 · APIs
                        ↓
            canonical clinical context
 identity · provenance · time · lifecycle · freshness
                        ↓
             deterministic policy boundary
                 ↙               ↘
          clinician UX        bounded apps/agents
                 ↘               ↙
                    human authority
```

The product question:

> **Can clinicians spend less time hunting, reconciling and re-entering information without losing provenance, uncertainty or human control?**

The infrastructure question:

> **Can hospital #100 inherit the integration knowledge of hospitals #1–99 instead of starting another custom IT project?**

North star: **Time Returned to Care — safety gated.**

---

# The endgame: integration becomes infrastructure

```text
legacy system
      ↓
standard / reusable adapter
      ↓
canonical interoperability layer
      ↓
every compatible clinical application
```

Different vendors should reuse the same standards-based adapter whenever their interfaces actually conform:

```text
Dedalus / FHIR ─┐
SAP / FHIR ─────┼─► standard-fhir-r4 ─► CareOS context contract
Vendor C / FHIR ┘
```

Site/vendor differences belong in **versioned capability profiles, mappings and conformance evidence**, not forks of the clinical core.

Long-term goal:

> **A normal hospital IT team can get from download to validated shadow-mode readiness in hours, not months — while clinical, privacy and security gates remain stricter than the install UX.**

[**Read the full endgame →**](docs/ENDGAME.md) · [**Hospital self-install architecture →**](docs/HOSPITAL_SELF_INSTALL_PLATFORM.md)

---

## Self-install scaffold already in the repo

CareOS now has a first executable path toward "describe the hospital once, reuse everything possible":

### 1. Non-secret Hospital Capability Manifest

`deploy/hospital.example.json`

Describes:

```text
vendor/product/version
KIS/LIS/etc. role
available interfaces
auth mode
patient/encounter identity
resource IDs/versions
effective time/lifecycle support
read/write capability
SSO/context launch
audit + accountable owners
```

Endpoints and credentials are **references to hospital secret-store environment variables**, not values committed to configuration.

### 2. Deterministic preflight + adapter planner

```bash
python scripts/hospital_preflight.py deploy/hospital.example.json
```

The planner in `app/hospital_install.py` prefers:

```text
ISiK/FHIR
→ FHIR R4
→ HL7 v2
→ stable vendor API
→ document feed
→ controlled UI/computer-use bridge only as fallback
```

Missing patient identity or a missing safe read path becomes a **blocker**, not a silently generated custom integration.

### 3. Hardened local deployment scaffold

```bash
docker compose -f deploy/docker-compose.hospital.yml run --rm preflight
docker compose -f deploy/docker-compose.hospital.yml up -d careos
```

Enterprise deployment scaffold: `deploy/helm/careos/`.

These paths are currently for synthetic/deidentified evaluation. CareOS code still refuses live-data modes while the evidence gates remain incomplete.

---

## Four invariants

| | CareOS rule |
|---|---|
| **01** | **Pending ≠ negative.** |
| **02** | **Unavailable ≠ absent.** |
| **03** | **Documented therapy ≠ AI recommendation.** |
| **04** | **Agent draft ≠ source truth.** |

These are correctness constraints, not UI decoration.

---

## Start here

| You are… | Open this |
|---|---|
| **Recare / AI engineering** | [90-second Recare work sample](https://mikelninh.github.io/recare/) → [Recare integration accelerator](docs/RECARE_INTEGRATION_ACCELERATOR.md) |
| **Clinician** | [Synthetic Infectiology workflow](https://mikelninh.github.io/careos/sjk/) |
| **Hospital IT / integration** | [Self-install platform](docs/HOSPITAL_SELF_INSTALL_PLATFORM.md) → [Connector SDK](docs/CONNECTOR_SDK.md) |
| **Hospital implementation** | [Zero-Drama Hospital Rollout](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md) |
| **CIO / CISO / senior engineer** | [Reference Architecture V2](docs/ARCHITECTURE_V2.md) |
| **Testing usefulness** | [Paired synthetic clinician A/B study](https://mikelninh.github.io/careos/sjk/ab.html) |
| **Software engineer / designer / researcher** | [Contributing guide](CONTRIBUTING.md) → [community roadmap](docs/COMMUNITY_ROADMAP.md) |
| **Germany / public sector** | [National / EU Integration Map](docs/NATIONAL_INTEGRATION_MAP.md) |
| **EU / global interoperability** | [Germany → Global Health Interoperability Blueprint](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md) |
| **Checking readiness / claims** | [Current Status & Gap Register](docs/CURRENT_STATUS_AND_GAPS.md) |
| **Big vision** | [CareOS Endgame](docs/ENDGAME.md) |

---

# What is actually built

## 1 · Clinician workflow

The first synthetic workflow is Infectiology: microbiology lifecycle, documented anti-infective therapy, hygiene/isolation context, trends, contradictions, pending work and source-linked handover/documentation drafts.

<div align="center">
  <img src="docs/screenshots/sjk-clinician-current.svg" alt="CareOS synthetic Infectiology clinician interface" width="820">
</div>

The paired study measures **task time, wrong answers, missed pending work, source checking, corrections, effort and verification decay** — not whether users simply like the UI.

## 2 · Clinical truth with provenance

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

### Frozen synthetic holdout

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

## 3 · Zero-trust agent boundary

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

## 4 · Reusable adapter/install contract

`app/hospital_install.py` turns a site capability manifest into a deterministic adapter plan and readiness report.

The key property is **reuse across hospitals**: adapter selection is driven by tested interfaces, not hospital names.

`docs/CONNECTOR_SDK.md` defines the runtime and conformance contract.

## 5 · Replayable failure tests

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

| Area | Current evidence state |
|---|---|
| Clinician workflow | **DEMONSTRATED SYNTHETICALLY** |
| Clinical truth / provenance | **DEMONSTRATED SYNTHETICALLY** |
| Agent containment | **DEMONSTRATED SYNTHETICALLY** |
| Hospital preflight / adapter planning | **IMPLEMENTED + SYNTHETICALLY TESTED** |
| Docker/Helm self-install scaffold | **IMPLEMENTED — NON-LIVE** |
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

# Interoperability: connect, don't replace

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

The portability work separates:

1. **Content** — what does the clinical item mean?
2. **Trust** — who issued it and can that issuer be verified?
3. **Policy** — may the receiving context use it for this purpose?

A pending result in Berlin must remain **pending** after translation or exchange. Translation may change presentation — never source truth.

[Germany → Global Interoperability Blueprint →](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md)

---

# Hospital rollout: zero drama

```text
legacy stays available
        ↓
technical + governance preflight
        ↓
read-only connection
        ↓
shadow mode
        ↓
one workflow / one ward
        ↓
human-approved copilot
        ↓
bounded execution only when earned
        ↓
retire one redundant legacy capability
        ↓
repeat
```

We cannot guarantee that software never fails. We **can** design against dangerous migration failure:

- no big-bang cutover;
- operational failure falls back to the legacy workflow;
- clinical uncertainty fails closed rather than becoming false absence;
- every stage is reversible;
- read does not imply write;
- legacy capabilities retire one at a time only after evidence.

[Hospital Implementation Playbook →](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md)

---

# Recare: collaborate, don't duplicate

Recare already operates the real product and integration layer across hospital workflows. CareOS is **not** a proposal to replace it.

The useful question is:

> **Can the integration knowledge Recare has accumulated across real hospitals become increasingly productized — typed capability manifests, reusable adapter/version profiles, automated conformance, upgrade preflight and fleet-safe regression tests?**

That is a collaboration hypothesis, not a claim that Recare lacks these capabilities internally.

[Recare × CareOS Collaboration Map →](docs/RECARE_COLLABORATION_MAP.md) · [Recare Integration Accelerator →](docs/RECARE_INTEGRATION_ACCELERATOR.md)

---

# Build with us

> **We are all in this together.**

Healthcare is too important and too interconnected for one person, company or discipline to solve alone. CareOS welcomes careful contributions from **software engineers, clinicians, designers, security researchers, interoperability specialists, data scientists, product thinkers and people with lived experience of broken healthcare workflows**.

Especially useful now:

- 🏥 hospital manifest / installer UX;
- 🔌 FHIR / ISiK / HL7 adapter and conformance fixtures;
- 🧪 vendor/version compatibility tests;
- 🔴 agent security and patient isolation;
- 🎨 clinician/source-verification UX;
- 🌍 IPS / cross-border portability;
- 📊 integration effort + rollout evidence tooling.

> **Find one piece of friction or one way the system can fail → make it better → show the evidence.**

[**How to contribute →**](CONTRIBUTING.md) · [**Pick a problem →**](docs/COMMUNITY_ROADMAP.md) · [**Open issues →**](https://github.com/mikelninh/care-os/issues) · [**Apache-2.0 license →**](LICENSE)

---

## What happens next

```text
self-install / adapter hypothesis
        ↓
external engineering critique
        ↓
synthetic clinician sessions
        ↓
real hospital capability manifest
        ↓
deidentified KIS / LIS sandbox
        ↓
measure custom work vs adapter reuse
        ↓
shadow workflow
        ↓
second hospital / different vendor
        ↓
prove configuration + conformance beats bespoke integration
```

More speculative application features are lower value than proving this deployment model against reality.

---

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.lock
uvicorn app.main:app --reload
```

Hospital preflight:

```bash
python scripts/hospital_preflight.py deploy/hospital.example.json
```

Recare capstone:

```bash
uvicorn app.recare_api:app --reload --port 8010
```

---

## Deep review index

| Need | Evidence |
|---|---|
| Big vision / endgame | [CareOS Endgame](docs/ENDGAME.md) |
| Hospital self-install / scale | [Self-Install Platform](docs/HOSPITAL_SELF_INSTALL_PLATFORM.md) |
| Connector / adapter contract | [Connector SDK](docs/CONNECTOR_SDK.md) |
| Recare integration-scale hypothesis | [Recare Integration Accelerator](docs/RECARE_INTEGRATION_ACCELERATOR.md) |
| Whole pre-hospital bundle | [Pre-Hospital Handoff](docs/PRE_HOSPITAL_HANDOFF.md) |
| Current gaps / readiness | [Current Status & Gaps](docs/CURRENT_STATUS_AND_GAPS.md) |
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
