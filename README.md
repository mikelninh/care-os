<div align="center">

# CareOS

### **Return time to care — without making clinical information less trustworthy.**

A clinician-first **interoperability, context and assurance layer** that sits beside existing healthcare systems, turns fragmented sources into source-linked clinical context, and makes that context safely usable by people and bounded AI applications.

[**▶ Master plan**](https://mikelninh.github.io/careos/master.html) · [**▶ Clinician demo**](https://mikelninh.github.io/careos/sjk/) · [**▶ Patient view**](https://mikelninh.github.io/careos/patient.html) · [**▶ Measure time back**](https://mikelninh.github.io/careos/study.html) · [**▶ Recare work sample**](https://mikelninh.github.io/recare/)

[![tests](https://github.com/mikelninh/care-os/actions/workflows/test.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/test.yml)
[![hospital-self-install](https://github.com/mikelninh/care-os/actions/workflows/hospital-self-install.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/hospital-self-install.yml)
[![future-foundation](https://github.com/mikelninh/care-os/actions/workflows/healthcare-future-foundation.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/healthcare-future-foundation.yml)
[![agent-redteam](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml)
[![license](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Synthetic / pre-hospital research only · not for clinical use · no identifiable patient data in public demos · no production write-back**

</div>

---

## CareOS in 10 seconds

Healthcare workers still spend too much of their day acting as human middleware between KIS/EHR, LIS, RIS/PACS, documents, ePA, calls, messages and legacy workflows.

**CareOS does not ask hospitals to replace those systems.** It explores a stable, provider-local layer above them:

```text
KIS / EHR · LIS · RIS/PACS · documents · ePA
                       ↓
                reusable adapters
                       ↓
          source-linked clinical context
 identity · provenance · time · lifecycle · freshness
                       ↓
       patient-local graph + deterministic policy
               ↙                   ↘
        role-specific UX         bounded agents/apps
               ↘                   ↙
                    human authority
```

Two questions drive the project:

> **Clinical:** Can people spend less time hunting, reconciling, copying and coordinating information without losing provenance, uncertainty or human control?

> **Infrastructure:** Can hospital #100 inherit the integration and safety knowledge learned from hospitals #1–99 instead of starting another bespoke IT project?

North star: **Time Returned to Care — safety gated.**

---

## Start with the person you care about

| You are… | Start here |
|---|---|
| **Clinician** | [Synthetic Infectiology workflow →](https://mikelninh.github.io/careos/sjk/) |
| **Patient / family** | [Synthetic patient experience →](https://mikelninh.github.io/careos/patient.html) |
| **Clinician / researcher testing usefulness** | [Time Returned to Care study →](https://mikelninh.github.io/careos/study.html) |
| **Hospital IT / integration** | [Self-install platform →](docs/HOSPITAL_SELF_INSTALL_PLATFORM.md) |
| **CIO / CISO / senior engineer** | [Architecture V2 →](docs/ARCHITECTURE_V2.md) |
| **Recare / AI engineering** | [90-second work sample →](https://mikelninh.github.io/recare/) · [collaboration map →](docs/RECARE_COLLABORATION_MAP.md) |
| **Germany / policy / interoperability** | [Germany → global blueprint →](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md) |
| **Contributor** | [Contributing →](CONTRIBUTING.md) · [community roadmap →](docs/COMMUNITY_ROADMAP.md) |
| **Want the whole picture** | [Healthcare Future Master Plan →](docs/HEALTHCARE_FUTURE_MASTER_PLAN.md) |

---

# What the ideal day feels like

Open the patient once.

```text
CHANGED
what became new or different

PENDING
what is not final yet

REVIEW
contradictions, uncertainty, stale/unavailable sources

NOW
source-linked context relevant to this role

WORK
what needs human action + prepared reviewable drafts
```

An important fact should lead back to its original evidence in one interaction.

The desired reaction after a good rollout is not:

> “The AI is impressive.”

It is:

> **“Why was I ever opening five systems to answer this?”**

[Explore stakeholder before/after journeys →](https://mikelninh.github.io/careos/future.html)

---

# Four invariants

| | Rule |
|---|---|
| **01** | **Pending ≠ negative.** |
| **02** | **Unavailable ≠ absent.** |
| **03** | **Documented therapy ≠ AI recommendation.** |
| **04** | **Agent draft ≠ source truth.** |

These are correctness constraints, not interface copy.

---

# One golden journey now connects the foundation

`app/end_to_end_journey.py` is a synthetic end-to-end regression story:

```text
source-linked preliminary result
        ↓
patient-local clinical graph
        ↓
unsigned source-dependent clinician draft
        ↓
network/source interruption
        ↓
corrected/final result arrives
        ↓
RECOVERY — do not silently resume
        ↓
new fact supersedes old fact
        ↓
dependent AI draft becomes REVIEW REQUIRED
        ↓
safety audit event
        ↓
reconciliation complete → NORMAL
        ↓
patient sees pending / next-step context
        ↓
minimum-purpose follow-up request
        ↓
requested → received → accepted → scheduled
→ performed → result available → follow-up complete
```

The journey deliberately keeps two claims honest:

- **Time Returned to Care is a target to test, not a fabricated outcome.**
- **24/7 production SLA remains NOT OFFERED until the operating organisation and evidence exist.**

Run the integrated synthetic API:

```bash
uvicorn app.future_api:app --reload --port 8020
```

Then inspect:

```text
GET  /health
GET  /api/journey/golden
GET  /api/patient/synthetic
GET  /api/resilience/standard-recovery-drill
GET  /api/coordination/synthetic-lifecycle
GET  /api/time-back/targets
POST /api/time-back/report
GET  /api/service/catalog
```

---

# Hospital IT: installation should be easier than safety approval

Long-term target:

```text
careos init
careos doctor
careos preflight
careos discover-fhir
careos up
```

Today that command surface exists for **synthetic/deidentified evaluation**.

```bash
git clone https://github.com/mikelninh/care-os.git
cd care-os
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.lock

python scripts/careos.py init \
  --hospital-id DE-DEMO-001 \
  --site-name "Example Hospital"

python scripts/careos.py doctor hospital.json --env-file deploy/hospital.env.example
python scripts/careos.py preflight hospital.json
python scripts/careos.py discover-fhir hospital.json --env-file deploy/hospital.env.example
python scripts/careos.py up hospital.json --env-file deploy/hospital.env.example
```

The installer can be pleasant. **The safety gates may not be bypassed for convenience.**

If patient identity, cross-source mapping, accountable ownership or a runnable adapter is missing, preflight blocks.

### Adapter truth today

| Path | Current CareOS state |
|---|---|
| **FHIR R4 read** | **IMPLEMENTED research runtime** |
| **ISiK / FHIR read** | **FHIR runtime + ISiK validation path** |
| HL7 v2 | **CONTRACT ONLY** |
| Vendor API | **CONTRACT ONLY** |
| Document/source feed | **CONTRACT ONLY** |
| UI / computer-use bridge | **CONTRACT ONLY** |
| Live transactional/write | **BLOCKED BY RELEASE POLICY** |

The machine-readable source of truth is [`architecture/adapter-catalog.json`](architecture/adapter-catalog.json).

---

# Scaling model: integration becomes infrastructure

```text
hospital source
      ↓
reusable adapter
      ↓
canonical context contract
      ↓
compatible clinician / patient / agent applications
```

Every deployment should improve the next:

```text
capability manifest
→ adapter selection
→ conformance
→ shadow evidence
→ compatibility knowledge
→ regression test
→ next hospital inherits it
```

Vendor/site differences should trend toward **configuration, mappings and versioned compatibility evidence**, not `hospital-a.py`, `hospital-b.py`, `hospital-c.py`.

The endgame is **not one world EHR**. It is an open clinical interoperability fabric where systems can change without rebuilding every application integration from zero.

[Read the endgame →](docs/ENDGAME.md)

---

# Migration: no big-bang go-live

```text
legacy remains authoritative
        ↓
read-only connection
        ↓
shadow mode
        ↓
one workflow / one ward
        ↓
human-approved copilot
        ↓
bounded actions only when earned
        ↓
retire one redundant legacy capability
        ↓
repeat
```

We cannot guarantee that software never fails. We can design stronger migration guarantees:

- no big-bang cutover;
- legacy/source workflow remains fallback until the new capability earns dependency;
- unavailable/stale/pending data never becomes false absence;
- read never implies write;
- patient identity is not guessed by a model;
- every rollout stage has explicit stop/rollback ownership;
- vendor/version changes require compatibility + shadow revalidation;
- new write authority cannot appear as an ordinary software upgrade.

[Zero-Drama Hospital Rollout →](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md)

---

# Resilience: AI disappears before clinical truth

CareOS models four explicit operating states:

```text
NORMAL
DEGRADED
OFFLINE
RECOVERY
```

Examples:

- model provider down → source-linked context still works;
- LIS unavailable → other admitted facts may remain visible, but microbiology absence conclusions are disabled;
- identity unavailable → agent/consequential operations fail closed;
- network restored → CareOS enters **RECOVERY** until missed versions/events reconcile;
- corrected result during outage → dependent unsigned draft reopens for review before normal operation resumes.

`app/resilience_drills.py` and `app/recovery_reconciliation.py` make this executable.

---

# Clinical context graph

Healthcare is relational:

```text
patient
├── encounter
│   ├── diagnosis
│   ├── order → specimen → result
│   ├── medication
│   └── document
├── task
├── care team
└── follow-up
```

CareOS treats the graph as a **patient-local, source-linked derived view**, not a magical AI truth database.

Derived relationships require evidence plus transformer/version lineage. Cross-patient graph content is rejected.

A key safety use:

> **When a source fact changes, find every downstream artifact that depended on it and reopen what is no longer current.**

Human-signed records are never silently rewritten.

---

# Cross-provider communication: state, not “sent”

A referral or transfer should not disappear after a PDF/fax/email leaves one organisation.

CareOS now models a transport-agnostic lifecycle:

```text
draft
→ requested
→ received
→ accepted / declined
→ scheduled
→ performed
→ result available
→ follow-up complete
```

The request references only context declared relevant to the stated purpose. An agent may prepare the package; **draft → requested requires governed human/workflow confirmation**.

The current implementation is a synthetic contract, not a live KIM/FHIR/network integration.

---

# Patients: access should become understanding

The patient/family surface asks different questions from the clinician surface:

```text
What happened?
What changed?
What are we still waiting for?
Who owns the next step?
What happens next?
What medication changed?
Where is the original source?
How can I ask or flag a possible error?
```

Rules:

- plain language is presentation, never source mutation;
- original wording remains accessible;
- pending/preliminary/unavailable stay visibly uncertain;
- proxy/family access uses explicit revocable delegation, not shared passwords;
- a patient helper may explain/translate/find/prepare questions, but does not create a new clinical truth.

Success is measured through **teach-back and understanding**, not page views.

[Try the synthetic patient view →](https://mikelninh.github.io/careos/patient.html)

---

# Agents: useful because authority stays outside the model

```text
untrusted model proposal
        ↓
deterministic Agent Gateway
patient · encounter · task · tools · operations · budgets
        ↓
trusted Tool Proxy
        ↓
source-linked result
        ↓
untrusted draft
        ↓
human review
```

Potential bounded roles include orientation, documentation, coordination, verification, patient explanation, IT integration support and operations support.

The reasoning worker cannot grant itself a different patient, tool, network destination, break-glass state or write permission.

[Agent Security Model →](docs/AGENT_SECURITY_MODEL.md)

---

# Measure usefulness instead of admiring the demo

Product targets to test:

| Role / workflow | First target |
|---|---:|
| Physician review/documentation | **20–30 min / affected shift workflow** |
| Nursing handover/coordination | **10–15 min / affected shift workflow** |
| Discharge/case management | **15–20 min / eligible case** |
| Routine supported IT change | **days → hours** |
| Patient experience | **understanding / teach-back** |

The paired study captures:

- elapsed time;
- systems/searches/context switches;
- copy/paste;
- clarification calls/messages;
- wrong answers;
- missed pending items;
- source opens;
- corrections;
- acceptance without source verification;
- cognitive effort;
- explicit safety stops.

A directional aggregate is not highlighted before **≥5 complete safe pairs** for that role/workflow. Safety stops or verification collapse override any time saving.

[Run the local synthetic study →](https://mikelninh.github.io/careos/study.html) · [Protocol →](docs/TIME_RETURNED_TO_CARE_STUDY.md)

---

# Critical-service operating discipline

If hospitals eventually depend on CareOS, it must operate like infrastructure.

The design now includes:

- service criticality tiers;
- systemic incident severity;
- narrow model/agent/tool/adapter/workflow/site/release kill scopes;
- hospital-local fallback and rollback authority;
- release rings / canary / revalidation;
- synthetic outage game days;
- monthly/quarterly value + safety review template;
- post-incident → regression/conformance rule.

But the repository deliberately refuses to pretend an operations team already exists:

> **24/7 contractual SLA: NOT OFFERED.**

The machine contract rejects a `CONTRACTED` service commitment without staffed on-call coverage, target-environment exercise evidence and evidence references.

[Critical Service Operating Model →](docs/CRITICAL_SERVICE_OPERATING_MODEL.md) · [Game Day →](docs/OPERATIONS_GAME_DAY.md) · [Hospital Review Template →](docs/HOSPITAL_VALUE_SAFETY_REVIEW_TEMPLATE.md)

---

# Evidence state — no self-scores

| Area | Current evidence state |
|---|---|
| Clinician workflow | **DEMONSTRATED SYNTHETICALLY** |
| Clinical truth / provenance | **DEMONSTRATED SYNTHETICALLY** |
| Patient-local graph / stale-artifact invalidation | **IMPLEMENTED + TESTED** |
| Resilience / recovery contracts | **IMPLEMENTED + TESTED SYNTHETICALLY** |
| Patient/family experience | **IMPLEMENTED SYNTHETICALLY — usability evidence pending** |
| Cross-provider lifecycle | **IMPLEMENTED CONTRACT — real transport pending** |
| Agent containment / adversarial evals | **DEMONSTRATED SYNTHETICALLY** |
| Hospital manifest / preflight | **IMPLEMENTED + SYNTHETICALLY TESTED** |
| Hospital-local FHIR-family data plane | **IMPLEMENTED — NON-LIVE** |
| Docker / Helm install scaffold | **IMPLEMENTED — NON-LIVE** |
| Time Returned to Care study machinery | **IMPLEMENTED — PARTICIPANT EVIDENCE PENDING** |
| Real KIS/LIS integration | **EXTERNAL EVIDENCE REQUIRED** |
| Production PHI operations | **BLOCKED BY DESIGN** |
| Production 24/7 service | **NOT YET EVIDENCED / NOT OFFERED** |
| Multi-hospital repeatability | **NOT YET EVIDENCED** |

One important known clinical-truth blocker remains visible: the frozen synthetic holdout reached high precision/provenance but only **26.32% recall with 100% review-case burden**, so G1 remains blocked for production.

[Canonical foundation status →](docs/FOUNDATION_IMPLEMENTATION_STATUS.md) · [Full current gaps →](docs/CURRENT_STATUS_AND_GAPS.md)

---

# Recare: collaborate, don't duplicate

Recare already operates the real hospital product/integration layer. CareOS is not a proposal to replace it.

The collaboration question is:

> **Which of these invariants, install/conformance patterns, graph/recovery ideas and evaluation methods survive Recare's production reality — and which assumptions should we delete?**

A particularly interesting hypothesis is whether accumulated integration knowledge can become increasingly productized through capability manifests, reusable adapter/version profiles, conformance, upgrade preflight and fleet-safe regression tests.

That is an investigation hypothesis, **not** a claim about Recare's private architecture or missing capabilities.

[Recare × CareOS Collaboration Map →](docs/RECARE_COLLABORATION_MAP.md)

---

# Build with us

> **We are all in this together.**

CareOS is Apache-2.0 and welcomes careful contributions from engineers, clinicians, nurses, designers, security researchers, interoperability specialists, patients and researchers.

Useful lanes include:

- 🔌 real adapter + conformance work;
- 🏥 installer / hospital IT UX;
- 🪪 cross-source identity / MPI;
- 🧪 vendor/version compatibility;
- 🔴 patient isolation / agent security;
- 📴 resilience / recovery drills;
- 🎨 clinician/patient accessibility + source-verification UX;
- 📊 workflow evidence;
- 🌍 IPS / cross-border portability.

> **One failure → one fix → one regression test.**

[Contributing →](CONTRIBUTING.md) · [Community roadmap →](docs/COMMUNITY_ROADMAP.md) · [Open issues →](https://github.com/mikelninh/care-os/issues)

---

# What happens next

```text
synthetic participant sessions
        ↓
Recare / production-engineering critique
        ↓
real hospital workflow archaeology
        ↓
first real capability manifest
        ↓
approved deidentified KIS/LIS/vendor sandbox
        ↓
shadow workflow
        ↓
read-only pilot
        ↓
second vendor / second hospital
        ↓
prove repeatability
        ↓
cross-provider real transport
        ↓
Germany → EU → international reuse
```

The remaining high-value gaps require **people and systems outside this repository**. Broad speculative feature expansion is now lower value than learning from them.

---

## Deep review

| Need | Evidence |
|---|---|
| Whole future state | [Healthcare Future Master Plan](docs/HEALTHCARE_FUTURE_MASTER_PLAN.md) |
| Current implementation | [Foundation Implementation Status](docs/FOUNDATION_IMPLEMENTATION_STATUS.md) |
| Big infrastructure endgame | [CareOS Endgame](docs/ENDGAME.md) |
| Hospital install / scale | [Self-Install Platform](docs/HOSPITAL_SELF_INSTALL_PLATFORM.md) |
| Hospital rollout | [Implementation Playbook](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md) |
| Logical architecture | [Architecture V2](docs/ARCHITECTURE_V2.md) |
| Current truth / gaps | [Status & Gap Register](docs/CURRENT_STATUS_AND_GAPS.md) |
| Patient / family | [Patient & Family Experience](docs/PATIENT_FAMILY_EXPERIENCE.md) |
| Critical operations | [Critical Service Operating Model](docs/CRITICAL_SERVICE_OPERATING_MODEL.md) |
| Germany → world | [Global Interoperability Blueprint](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md) |
| Agent security | [Agent Security Model](docs/AGENT_SECURITY_MODEL.md) |
| Full evidence index | [Technical Documentation Index](docs/TECHNICAL_DOCUMENTATION_INDEX.md) |

---

<div align="center">

### **Keep systems of record. Standardize trustworthy context above them.**

*Models may interpret and propose. Evidence, authority and safety boundaries remain outside the model.*

</div>
