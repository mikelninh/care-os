<div align="center">

# CareOS

### **Return time to care — without making clinical information less trustworthy.**

A clinician-first **interoperability, context and assurance layer** that sits beside existing healthcare systems, composes source-linked clinical context and makes that context safely usable by people and bounded AI applications.

[**▶ 90-sec Recare work sample**](https://mikelninh.github.io/recare/) · [**▶ One patient end to end**](https://mikelninh.github.io/careos/journey.html) · [**▶ Master plan**](https://mikelninh.github.io/careos/master.html) · [**▶ Synthetic study**](https://mikelninh.github.io/careos/study.html)

[![tests](https://github.com/mikelninh/care-os/actions/workflows/test.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/test.yml)
[![hospital-self-install](https://github.com/mikelninh/care-os/actions/workflows/hospital-self-install.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/hospital-self-install.yml)
[![future-foundation](https://github.com/mikelninh/care-os/actions/workflows/healthcare-future-foundation.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/healthcare-future-foundation.yml)
[![agent-redteam](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml)

**Synthetic / pre-hospital research only · not for clinical use · no identifiable patient data in public demos · no production write-back**

</div>

---

## If you only have five minutes

1. **Run the Recare work sample** — [Clinical Time-Back Challenge →](https://mikelninh.github.io/recare/)
2. **See one complete patient journey** — [source → draft → outage → correction → recovery → patient → follow-up →](https://mikelninh.github.io/careos/journey.html)
3. **Check what is actually implemented** — [Foundation status →](docs/FOUNDATION_IMPLEMENTATION_STATUS.md)
4. **Check what is still unproven** — [Current gaps →](docs/CURRENT_STATUS_AND_GAPS.md)
5. **For Recare specifically** — [Recare × CareOS collaboration map →](docs/RECARE_COLLABORATION_MAP.md)

The intended reaction is not “nice AI demo.” It is:

> **This person understands that healthcare AI only becomes useful when integration, clinical state, provenance, authority, failure behavior and human workflow all survive contact with reality.**

---

## CareOS in 10 seconds

Healthcare workers still act as human middleware between KIS/EHR, LIS, RIS/PACS, documents, ePA, calls, messages and legacy workflows.

CareOS explores a stable layer above those systems rather than replacing them:

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

> **Infrastructure:** Can hospital #100 inherit integration and safety knowledge learned from hospitals #1–99 instead of starting another bespoke IT project?

North star: **Time Returned to Care — safety gated.**

---

## Four invariants

| | Rule |
|---|---|
| **01** | **Pending ≠ negative.** |
| **02** | **Unavailable ≠ absent.** |
| **03** | **Documented therapy ≠ AI recommendation.** |
| **04** | **Agent draft ≠ source truth.** |

These are correctness constraints, not interface copy.

---

# One golden journey connects the whole foundation

`app/end_to_end_journey.py` is a permanent synthetic regression story:

```text
source-linked preliminary result
        ↓
patient-local clinical graph
        ↓
unsigned source-dependent draft
        ↓
source/network interruption
        ↓
corrected/final result arrives
        ↓
RECOVERY — reconcile before resuming
        ↓
new fact supersedes old fact
        ↓
dependent draft becomes REVIEW REQUIRED
        ↓
safety audit event
        ↓
NORMAL only after reconciliation
        ↓
patient sees pending / next-step context
        ↓
minimum-purpose follow-up request
        ↓
requested → received → accepted → scheduled
→ performed → result available → follow-up complete
```

[**View the human-readable golden journey →**](https://mikelninh.github.io/careos/journey.html)

The regression deliberately protects two claim boundaries:

- **Time Returned to Care is a target to measure, not a fabricated outcome.**
- **24/7 production SLA is not offered until staffing and target-environment evidence exist.**

---

# What is implemented now

## Clinical truth + lifecycle

Consequential facts can retain:

```text
patient / encounter
source organisation / system / resource
original value / wording
effective + recorded time
version + freshness
preliminary / final / corrected / cancelled
pending / stale / unavailable / contradictory
terminology mapping lineage
review / supersession state
```

The model may propose structure. It does **not** become the authority that creates trusted clinical truth.

Known blocker: the frozen 500-case synthetic holdout preserved precision/provenance but reached only **26.32% recall with 100% review-case burden**, so production G1 remains blocked.

## Patient-local graph + stale-artifact invalidation

- hard patient partition;
- source / supersession / contradiction / derived relationships;
- evidence + transformer/version lineage;
- changed source facts reopen dependent unsigned AI/derived artifacts;
- signed human artifacts are flagged, never silently rewritten.

## Bounded agent architecture

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

Hostile scenarios include wrong patient, prompt injection, unavailable source, stale result and unauthorised write escalation.

## Resilience + recovery

Explicit modes:

```text
NORMAL · DEGRADED · OFFLINE · RECOVERY
```

Connectivity returning is not sufficient for normal operation: missed versions/events reconcile first, and corrected source facts can invalidate downstream drafts before the system returns to `NORMAL`.

## Patient / family foundation

The patient view uses the same source philosophy but answers different questions:

```text
What happened?
What changed?
What is still pending?
Who owns the next step?
What happens next?
What medication changed?
Where is the source?
How can I flag a possible error?
```

Plain language is presentation metadata, not source mutation. Proxy access is an explicit revocable grant, not a shared password.

[Try the synthetic patient view →](https://mikelninh.github.io/careos/patient.html)

## Cross-provider care coordination

A referral/transfer is modeled as workflow state rather than “document sent”:

```text
draft → requested → received → accepted/declined
→ scheduled → performed → result available → follow-up complete
```

Agents may prepare. Initial sending requires governed human/workflow authority. Real KIM/FHIR/network transport remains external work.

---

# Hospital installation should be simple; approval should not be fake

Current command surface:

```text
careos init
careos doctor
careos preflight
careos review-pack
careos discover-fhir
careos up
careos upgrade-check
careos down
```

Example:

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
python scripts/careos.py review-pack hospital.json --out-dir /tmp/careos-review
python scripts/careos.py discover-fhir hospital.json --env-file deploy/hospital.env.example
python scripts/careos.py up hospital.json --env-file deploy/hospital.env.example
```

The installer blocks rather than inventing missing patient identity, ownership, adapter runtime or live-data authority.

### Adapter truth today

| Path | Current CareOS state |
|---|---|
| **FHIR R4 read** | **implemented research runtime** |
| **ISiK / FHIR read** | **FHIR runtime + ISiK validation path** |
| **HL7 v2 ADT/ORU parsing** | **implemented synthetic/deidentified library connector** |
| **HL7 v2 self-install transport / real interface engine** | **not runnable / real evidence required** |
| Vendor API | **contract only** |
| Document/source feed | **contract only** |
| UI / computer-use bridge | **contract only** |
| Live transactional/write | **blocked by release policy** |

The machine-readable deployment catalog remains [`architecture/adapter-catalog.json`](architecture/adapter-catalog.json). It intentionally does **not** advertise a green HL7 self-install path until transport/interface-engine and real compatibility evidence exist.

---

# Hospital-scale reuse foundation

The infrastructure hypothesis is now executable as contracts:

### Trusted MPI / source-ID resolution

An enterprise patient may map deterministically to different source IDs. Missing, ambiguous, unavailable or stale resolution fails closed before connector reads. No LLM performs patient matching.

The runtime contract exists; `careos doctor/up` still block trusted-MPI self-install until an approved real hospital resolver adapter is configured.

### Generated hospital review pack

`careos review-pack` produces non-secret JSON / Markdown / Mermaid describing systems, adapters, auth modes, data flow, owner lanes, read/write boundaries and unresolved blockers.

It supports DPO/CISO/IT review. It is **not** DSFA/DPIA/security approval.

### Evidence-gated canary + rollback

```text
PROPOSED → PREFLIGHT → CONFORMANCE → CANARY
                                   ↙      ↘
                              ROLLBACK   PROMOTE
```

Identity errors, incomplete reads, unsupported claims, safety stops, operator stop or unexpected write authority block promotion.

### Compatibility registry

Vendor/product/version evidence can be classified as:

```text
synthetic-only · real-sandbox · real-shadow · production-observed
```

Compatibility knowledge can reduce repeated investigation. It can never automatically approve rollout.

[Hospital-scale foundation →](docs/HOSPITAL_SCALE_FOUNDATION.md)

---

# Measure usefulness instead of admiring the demo

The Time Returned to Care study captures:

- elapsed time;
- systems/searches/context switches;
- copy/paste;
- clarification contacts;
- wrong answers;
- missed pending items;
- source opens;
- corrections;
- acceptance without source verification;
- cognitive effort;
- explicit safety stops.

The paired protocol now counterbalances **condition order and matched synthetic case variant**. A role result is not marked publishable before ≥5 complete safe pairs, both order directions are represented and no safety/verification gate fails.

[Run the synthetic study →](https://mikelninh.github.io/careos/study.html) · [Protocol →](docs/TIME_RETURNED_TO_CARE_STUDY.md)

---

# Evidence state — not a self-score

| Area | Current evidence state |
|---|---|
| Clinician workflow | **DEMONSTRATED SYNTHETICALLY** |
| Clinical truth / provenance | **DEMONSTRATED SYNTHETICALLY — G1 BLOCKED** |
| Graph / stale-artifact invalidation | **IMPLEMENTED + TESTED** |
| Agent containment / adversarial evals | **DEMONSTRATED SYNTHETICALLY** |
| Resilience / recovery | **IMPLEMENTED + TESTED SYNTHETICALLY** |
| Patient/family experience | **IMPLEMENTED SYNTHETICALLY — usability pending** |
| Cross-provider lifecycle | **IMPLEMENTED CONTRACT — real transport pending** |
| Hospital manifest / preflight / local FHIR data plane | **IMPLEMENTED — NON-LIVE** |
| Trusted MPI resolver contract | **IMPLEMENTED — real resolver integration pending** |
| Review-pack / rollout / compatibility registry | **IMPLEMENTED + SYNTHETICALLY TESTED** |
| HL7 v2 ADT/ORU library connector | **IMPLEMENTED SYNTHETICALLY — transport/vendor evidence pending** |
| Time Returned to Care machinery | **IMPLEMENTED — participant evidence pending** |
| Real KIS/LIS integration | **EXTERNAL EVIDENCE REQUIRED** |
| Production PHI operations | **BLOCKED BY DESIGN** |
| Multi-hospital repeatability | **NOT YET EVIDENCED** |
| Regulatory / independent assurance | **EXTERNAL REVIEW REQUIRED** |

[Canonical implementation status →](docs/FOUNDATION_IMPLEMENTATION_STATUS.md) · [Gap register →](docs/CURRENT_STATUS_AND_GAPS.md) · [Production gates →](docs/GATES.md)

---

# Recare: collaboration, not duplication

Recare already operates the real hospital product/integration layer. CareOS is not a proposal to replace it.

The useful question is:

> **Which CareOS invariants, evals and integration patterns survive Recare's production reality — and where could they make an existing hospital platform easier to scale or safer to change?**

Areas to validate with the team:

- clinical lifecycle semantics across heterogeneous sources;
- provenance survival through context → agent/document → human review;
- agent tool/authority containment;
- failure replay/evaluation;
- integration knowledge as machine-readable compatibility/conformance evidence;
- upgrade regression testing;
- Time Returned to Care without verification decay.

We do **not** assume Recare lacks these internally.

[Recare × CareOS Collaboration Map →](docs/RECARE_COLLABORATION_MAP.md)

---

# Endgame

The endgame is **not one world EHR**.

It is an open clinical interoperability fabric where hospitals can keep/change systems of record while applications integrate against stable trustworthy seams:

```text
FHIR / IPS / provenance / trust
        ↓
regional + national profiles
        ↓
open adapters + conformance
        ↓
provider-local data planes
        ↓
stable source-linked context contract
        ↓
clinician / patient / agent / app ecosystem
```

Success eventually means a hospital can change a KIS vendor without rebuilding every application integration, and a new compatible application does not need 80 hospital-specific pipelines.

[Read the endgame →](docs/ENDGAME.md) · [Healthcare Future Master Plan →](docs/HEALTHCARE_FUTURE_MASTER_PLAN.md)

---

# What happens next

```text
real synthetic participant sessions
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
```

Broad speculative feature expansion is now lower value than external evidence.

---

## Deep review

| Need | Start here |
|---|---|
| Whole future state | [Healthcare Future Master Plan](docs/HEALTHCARE_FUTURE_MASTER_PLAN.md) |
| Current implementation | [Foundation Implementation Status](docs/FOUNDATION_IMPLEMENTATION_STATUS.md) |
| Current gaps | [Status & Gap Register](docs/CURRENT_STATUS_AND_GAPS.md) |
| Infrastructure endgame | [CareOS Endgame](docs/ENDGAME.md) |
| Hospital install / scale | [Self-Install Platform](docs/HOSPITAL_SELF_INSTALL_PLATFORM.md) |
| Hospital scale contracts | [Hospital-Scale Foundation](docs/HOSPITAL_SCALE_FOUNDATION.md) |
| Hospital rollout | [Implementation Playbook](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md) |
| Architecture | [Architecture V2](docs/ARCHITECTURE_V2.md) |
| Agent security | [Agent Security Model](docs/AGENT_SECURITY_MODEL.md) |
| Patient / family | [Patient & Family Experience](docs/PATIENT_FAMILY_EXPERIENCE.md) |
| Critical operations | [Critical Service Operating Model](docs/CRITICAL_SERVICE_OPERATING_MODEL.md) |
| Germany → world | [Global Interoperability Blueprint](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md) |
| Recare collaboration | [Recare Collaboration Map](docs/RECARE_COLLABORATION_MAP.md) |
| Technical index | [Technical Documentation Index](docs/TECHNICAL_DOCUMENTATION_INDEX.md) |

---

<div align="center">

### **Keep systems of record. Standardize trustworthy context above them.**

*Models may interpret and propose. Evidence, authority and safety boundaries remain outside the model.*

</div>