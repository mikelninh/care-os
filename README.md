<div align="center">

# CareOS

### **Return time to care — without making clinical information less trustworthy.**

CareOS is a clinician-first **interoperability, context and assurance layer** that sits beside existing hospital systems, composes source-linked clinical context and makes that context safely usable by people and bounded AI applications.

[**▶ Clinical review demo**](https://mikelninh.github.io/careos/clinical.html) · [**▶ One patient end to end**](https://mikelninh.github.io/careos/journey.html) · [**▶ Synthetic study**](https://mikelninh.github.io/careos/study.html) · [**▶ Release assurance**](docs/RELEASE_ASSURANCE.md) · [**▶ Real-world proof plan**](proof/README.md)

[![tests](https://github.com/mikelninh/care-os/actions/workflows/test.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/test.yml)
[![agent-redteam](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml)

**Pre-hospital research · synthetic/deidentified evaluation only · not for clinical use · no production write-back**

</div>

---

## CareOS in 30 seconds

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

> **Clinical:** Can clinicians spend less time hunting, reconciling, copying and coordinating information without losing provenance, uncertainty or human control?

> **Infrastructure:** Can hospital #100 reuse integration and safety knowledge learned from hospitals #1–99 instead of starting another bespoke IT project?

North star: **Time Returned to Care — safety gated.**

## Try these first

1. **Interactive clinical review** — [source review → human status review → documentation → ready-for-transfer](https://mikelninh.github.io/careos/clinical.html)
2. **One complete synthetic patient journey** — [source → draft → outage → correction → recovery → patient → follow-up](https://mikelninh.github.io/careos/journey.html)
3. **Time Returned to Care study** — [synthetic paired-study surface](https://mikelninh.github.io/careos/study.html)
4. **What is actually implemented** — [`FOUNDATION_IMPLEMENTATION_STATUS.md`](docs/FOUNDATION_IMPLEMENTATION_STATUS.md)
5. **What is automatically tested vs externally unproven** — [`RELEASE_ASSURANCE.md`](docs/RELEASE_ASSURANCE.md)
6. **What is still unproven** — [`CURRENT_STATUS_AND_GAPS.md`](docs/CURRENT_STATUS_AND_GAPS.md)
7. **How we now create real evidence** — [`proof/README.md`](proof/README.md)

The intended reaction is not “nice AI demo.” It is:

> **Does this architecture and workflow survive real clinicians, real hospital systems and skeptical external review?**

---

# What exists today

| Area | Evidence state today |
|---|---|
| Source-linked clinical lifecycle/provenance | **tested synthetically** |
| Patient-local graph + stale-artifact invalidation | **implemented + tested** |
| Bounded agent/tool authority | **tested synthetically + adversarial scenarios** |
| NORMAL / DEGRADED / OFFLINE / RECOVERY behavior | **implemented + tested synthetically** |
| Patient/family source-linked experience | **implemented synthetically** |
| Human clinical review UX | **interactive synthetic demo + DOM smoke + desktop/mobile visual QA** |
| FHIR R4 read path | **implemented research runtime** |
| ISiK/FHIR-oriented validation path | **implemented research path** |
| HL7 v2 ADT/ORU parsing | **synthetic/deidentified library connector** |
| Hospital manifest / preflight / review pack | **implemented + tested, non-live** |
| Docker/Helm deployment scaffold | **implemented, non-live** |
| Time Returned to Care study machinery | **implemented — participant evidence pending** |
| Real KIS/LIS integration | **external evidence required** |
| Production PHI operations | **blocked by design** |
| Multi-hospital repeatability | **not yet evidenced** |
| Clinical/regulatory assurance | **external review required** |

## Four correctness invariants

| | Rule |
|---|---|
| **01** | **Pending ≠ negative.** |
| **02** | **Unavailable ≠ absent.** |
| **03** | **Documented therapy ≠ AI recommendation.** |
| **04** | **Agent draft ≠ source truth.** |

The model may propose structure. It does **not** become the authority that creates trusted clinical truth.

## Release assurance in one sentence

CareOS has strong **synthetic engineering E2E + adversarial + integration-path coverage**, but it does **not** have clinical-production E2E proof. A green repository cannot substitute for real clinicians, approved hospital environments, privacy/security review or regulatory evidence.

See [`RELEASE_ASSURANCE.md`](docs/RELEASE_ASSURANCE.md) for the exact automated layers and non-claims.

---

# The blocker we do not hide

The frozen 500-case synthetic clinical-truth holdout currently preserves precision/provenance but achieves only **26.32% recall with 100% review-case burden**.

Therefore **production G1 remains blocked**.

That is not a footnote. It means CareOS should not be presented as clinically validated, production-ready or ready to make patient-care decisions.

The correct next move is not to hide the result or tune against the frozen holdout. It is to improve the frontier on fresh development data, observe real user behavior, and test against real source variation.

See [`CLAIM_EVIDENCE_MATRIX.md`](docs/CLAIM_EVIDENCE_MATRIX.md) and [`GATES.md`](docs/GATES.md).

---

# Real-World Proof Sprint 1

CareOS has reached the point where **external evidence is more valuable than another broad feature**.

The current proof ladder is:

```text
runnable synthetic tests
        ↓
real clinicians on synthetic cases
        ↓
independent clinical / privacy / security / IT critique
        ↓
real non-secret hospital capability manifest
        ↓
approved vendor / deidentified sandbox
        ↓
governed shadow workflow
        ↓
bounded read-only pilot
        ↓
second hospital / second vendor
        ↓
prove repeatability
```

Sprint 1 only graduates when we have:

- **≥5 complete safe paired clinician sessions** for one workflow family;
- observed baseline vs CareOS timing, errors, source checks and cognitive effort;
- zero hidden safety-stop events in any positive result;
- at least **3 independent reviewer perspectives**;
- one real non-secret hospital capability manifest completed with hospital staff;
- every external finding recorded as **supported / falsified / blocked / unknown**;
- at least one assumption corrected or falsified.

If nothing changes after external review, the test was probably too friendly.

Start here:

- [`proof/README.md`](proof/README.md)
- [`proof/CLINICIAN_STUDY_PREREG.md`](proof/CLINICIAN_STUDY_PREREG.md)
- [`proof/HOSPITAL_DISCOVERY_WORKSHOP.md`](proof/HOSPITAL_DISCOVERY_WORKSHOP.md)
- [`proof/INDEPENDENT_REVIEW_PACKET.md`](proof/INDEPENDENT_REVIEW_PACKET.md)
- [`proof/EVIDENCE_LEDGER.yaml`](proof/EVIDENCE_LEDGER.yaml)

---

# First workflow to prove

**Physician morning review + documentation preparation.**

The question is not:

> “Do you like CareOS?”

It is:

> **Can a clinician reconstruct changed, pending and critical context and prepare the bounded documentation task faster or with less friction without more errors or verification collapse?**

The paired protocol captures:

- elapsed task time;
- systems/searches/context switches;
- wrong answers;
- missed pending items;
- source opens;
- corrections;
- acceptance without source verification;
- cognitive effort;
- explicit safety stops.

A speed gain is **not** a win if safety or verification gets worse.

Protocol: [`TIME_RETURNED_TO_CARE_STUDY.md`](docs/TIME_RETURNED_TO_CARE_STUDY.md) · facilitator test: [`CLINICIAN_TEST.md`](CLINICIAN_TEST.md)

---

# One golden journey protects the architecture

`app/end_to_end_journey.py` is a permanent synthetic regression story:

```text
preliminary source result
        ↓
source-linked patient context
        ↓
unsigned derived draft
        ↓
source/network interruption
        ↓
corrected/final result arrives
        ↓
RECOVERY — reconcile before resuming
        ↓
old derived work becomes REVIEW REQUIRED
        ↓
human review + audit
        ↓
NORMAL only after reconciliation
        ↓
patient sees pending / next-step context
        ↓
follow-up request lifecycle
```

[View the human-readable journey →](https://mikelninh.github.io/careos/journey.html)

---

# Agent safety model

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

The model cannot grant itself new patient, tool, operation or effect authority.

See [`AGENT_SECURITY_MODEL.md`](docs/AGENT_SECURITY_MODEL.md).

---

# Hospital integration: runnable scaffold, not fake compatibility

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

The installer blocks rather than inventing missing patient identity, ownership, adapter runtime or live-data authority.

Current adapter truth:

| Path | Current state |
|---|---|
| FHIR R4 read | implemented research runtime |
| ISiK / FHIR read | runtime + validation path |
| HL7 v2 ADT/ORU parsing | synthetic/deidentified library connector |
| HL7 v2 real interface-engine transport | **real evidence required** |
| Vendor API | contract only |
| Document/source feed | contract only |
| Live transactional/write | **blocked by release policy** |

No named KIS/LIS compatibility claim is made until a real approved sandbox or hospital environment provides that evidence.

---

# Where OpenAction fits

CareOS is the **clinical product and source-linked workflow layer**.

[OpenAction](https://github.com/mikelninh/openaction) is the **adoption/evidence coordination layer** around the real pilot:

```text
claim
  ↓
required evidence
  ↓
owner
  ↓
independent verifier
  ↓
verified / rejected / blocked
  ↓
next milestone unlocked
```

For a CareOS hospital pilot, OpenAction can coordinate Clinical, Privacy, Security, Integration, Procurement, Finance, Operations and Sponsor while keeping one shared case state.

That creates a second falsifiable question:

> **Can we reduce avoidable waiting and duplicate review work without reducing accountability?**

---

# What we do not claim

CareOS is **not currently**:

- clinically validated;
- approved for identifiable patient-data production use;
- proven to save clinician time;
- proven interoperable with a named production KIS/LIS;
- a production-ready generic HL7 v2 interface-engine integration;
- proven repeatable across hospitals;
- regulatory approved/certified;
- a 24/7 clinical service.

Stronger-looking copy is not stronger evidence.

---

# How to help

The highest-value contribution now is **skeptical external evidence**, not more speculative features.

### If you are a clinician
Run one paired synthetic workflow and tell us where the workflow or trust model fails.

### If you work in hospital IT / integration
Try to map CareOS against a real non-secret system landscape and identify assumptions that do not survive your KIS/LIS/MPI reality.

### If you work in privacy / security / clinical safety / regulatory
Use the [`Independent Review Packet`](proof/INDEPENDENT_REVIEW_PACKET.md) and try to block the next step for a good reason.

### If you work in UX / service design
Test whether a clinician can understand changed/pending/source state without explanation and whether verification feels easier rather than heavier.

Every meaningful external finding should end up in the evidence ledger or as a regression test.

---

# Deep review

| Need | Start here |
|---|---|
| Release assurance / automated vs external proof | [`RELEASE_ASSURANCE.md`](docs/RELEASE_ASSURANCE.md) |
| Real-world proof campaign | [`proof/README.md`](proof/README.md) |
| Claim → evidence matrix | [`CLAIM_EVIDENCE_MATRIX.md`](docs/CLAIM_EVIDENCE_MATRIX.md) |
| Current gaps | [`CURRENT_STATUS_AND_GAPS.md`](docs/CURRENT_STATUS_AND_GAPS.md) |
| Implementation status | [`FOUNDATION_IMPLEMENTATION_STATUS.md`](docs/FOUNDATION_IMPLEMENTATION_STATUS.md) |
| Production gates | [`GATES.md`](docs/GATES.md) |
| Architecture | [`ARCHITECTURE_V2.md`](docs/ARCHITECTURE_V2.md) |
| Hospital rollout | [`HOSPITAL_IMPLEMENTATION_PLAYBOOK.md`](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md) |
| Hospital scale | [`HOSPITAL_SCALE_FOUNDATION.md`](docs/HOSPITAL_SCALE_FOUNDATION.md) |
| Agent security | [`AGENT_SECURITY_MODEL.md`](docs/AGENT_SECURITY_MODEL.md) |
| Patient / family | [`PATIENT_FAMILY_EXPERIENCE.md`](docs/PATIENT_FAMILY_EXPERIENCE.md) |
| Endgame | [`ENDGAME.md`](docs/ENDGAME.md) |

---

<div align="center">

### **Keep systems of record. Standardize trustworthy context above them.**

*Models may interpret and propose. Evidence, authority and safety boundaries remain outside the model.*

</div>