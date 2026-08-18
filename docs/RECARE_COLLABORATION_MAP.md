# Recare × CareOS — Collaboration Map

Baseline: **18 August 2026**

> This is a comparison of public product information with CareOS research. It is **not** a claim about Recare's private architecture, internal controls or missing capabilities.

## Executive conclusion

CareOS should **not** be positioned as a competing product to Recare.

Recare already operates the real product layer across hospital workflows: Patient Overview, extraction, document generation, voice documentation, agent workflows, discharge coordination, prediction and KIS transfer. Publicly, Recare says 1,000+ hospitals trust Recare Discharge; Patient Overview and Agent integrate with existing KIS via HL7; Recare states ISO 27001 certification and BSI C5 Type 2 compliance.

CareOS is a much narrower **synthetic R&D / evaluation artifact**.

The collaboration question is therefore:

> **Which CareOS invariants, evals and implementation patterns survive contact with Recare's real product, integrations and hospitals — and where can they make the existing platform stronger?**

---

## 1. Public Recare product baseline

| Recare capability | Publicly described role | CareOS relationship |
|---|---|---|
| **Patient Overview** | structured role-based patient profile combining KIS/Recare/document information | strong product overlap |
| **Extract** | structured extraction from findings, PDFs, scans and free text | strong overlap with evidence/truth pipeline |
| **Docs** | creates reviewable clinical documents | overlap with grounded drafting |
| **Voice** | real-time documentation and form/document filling | complementary |
| **Agent** | combines documentation, extraction, transfer and patient-context interaction | strong workflow overlap |
| **Clinical decision support via Prof. Valmed** | medical questions can be routed to MDR-certified Prof. Valmed in patient context | **broader intended use than CareOS prototype** |
| **Operator** | computer-use transfer of Recare-created data into KIS without a traditional interface project | complementary legacy bridge |
| **Discharge** | digital post-acute/discharge coordination network | Recare production moat |
| **Predict** | earlier identification of post-acute needs | complementary |

Public sources:

- https://recareai.com/krankenhaus
- https://recareai.com/krankenhaus/recare-patient-overview
- https://recareai.com/krankenhaus/recare-agent
- https://recareai.com/krankenhaus/recare-operator

### Important maturity boundary

Do not imply equivalence.

**Recare:** production hospital platform, real integrations, real clinical workflows, certified security claims, operating organisation and broad product scope.

**CareOS:** synthetic/pre-hospital research, deliberately blocked live PHI and write-back, narrow non-recommendation capstone, reference architecture and evaluation methods.

CareOS's rule `documented therapy ≠ AI recommendation` is a boundary for **this prototype**, not a claim that Recare should never support regulated clinical decision support. Recare publicly describes clinical decision support through Prof. Valmed. The useful question is how authority, provenance, routing, approval and evaluation should remain inspectable across different risk classes.

---

## 2. Where CareOS research may contribute

These are **investigation areas**, not assertions that Recare lacks them internally.

### 2.1 Clinical lifecycle semantics

CareOS treats state as part of correctness:

```text
preliminary
final
corrected
cancelled
pending
stale
unavailable
contradictory
unknown
```

Questions worth asking in a real Recare system:

- How is lifecycle state normalized across KIS/LIS/document sources?
- How are preliminary → final → corrected transitions represented?
- How does source unavailability propagate to downstream summaries/agents?
- Can pending/unavailable ever collapse into apparent absence?
- How are unresolved conflicts shown rather than silently resolved?

Potential contribution: reusable state contract + lifecycle regression fixtures.

### 2.2 Provenance / evidence contracts

A consequential fact should be able to retain:

```text
value + original wording
source organisation/system
resource/document identifier
clinical effective time
recorded/ingestion time
version + freshness
terminology mapping lineage
evidence span for document-derived content
review state
contradiction/supersession state
```

Potential contribution: test whether provenance survives the full path from integration → Patient Overview → Agent/Docs → human approval.

### 2.3 Agent authority and containment

Recare publicly says Agent actions are shown for user approval before execution. CareOS asks a narrower systems question:

> **If a reasoning model or source document becomes hostile, what can it still cause the platform to do?**

CareOS keeps authority outside the model through:

- narrow delegation;
- patient/encounter/task binding;
- versioned tools;
- operation/data allowlists;
- budgets;
- deny-default egress;
- human-confirmation requirements;
- revocation/kill path;
- audit;
- trusted Tool Proxy.

Potential contribution: hostile-worker/capability-manifest patterns as a red-team and regression layer around real agent workflows.

### 2.4 Agent observability and evals

The Recare capstone turns failures into replayable scenarios:

- wrong patient;
- prompt injection;
- source unavailable;
- stale result;
- unauthorised write;
- pending/conflict retention.

Potential contribution: combine model quality, tool correctness, authorization and user-visible degraded behaviour into one eval surface.

### 2.5 Time Returned to Care — safety gated

CareOS's outcome set is:

- task time;
- source checks;
- corrections;
- missed pending items;
- unsupported claims;
- verification decay;
- effort;
- adoption/abandonment;
- degraded-mode behaviour.

A safety-stop overrides a speed win.

Potential contribution: pair Recare's production outcome metrics with verification and correction behaviour, not model-output metrics alone.

### 2.6 Interoperability beyond transport

Recare publicly describes HL7/KIS integration, while Operator uses computer-use as a legacy bridge where interface work is undesirable.

CareOS separates three interoperability questions:

1. **content** — what does the clinical item mean?
2. **trust** — who issued it and can the receiver verify that?
3. **policy** — may this receiving context use it for this purpose?

Potential contribution: preserve lifecycle state and provenance across FHIR/ISiK → EHDS/IPS portability rather than treating successful transport as sufficient.

---

## 3. What to do if joining Recare

### Days 1–15 — absorb production reality

Spend time with:

- interoperability/integration engineering;
- AI/ML engineering;
- implementation;
- product/support;
- clinicians;
- hospital IT/security where possible.

Ask:

```text
Which integrations create the most operational pain?
What breaks most often?
Which clinical-source states are hardest to normalize?
Where do clinicians correct or distrust AI output?
How are agent failures replayed today?
Where does computer-use beat interface work — and where does it not?
Which assumptions in CareOS are simply wrong?
```

Output: `CareOS idea → Recare reality`.

Every CareOS concept gets one disposition:

- already solved better → retire duplicate;
- useful invariant → integrate into existing architecture;
- useful test/eval → port;
- wrong assumption → document and remove;
- unresolved production problem → candidate roadmap item.

### Days 15–30 — choose one real problem

Prefer one narrow production-relevant workflow:

- Patient Overview state/provenance reliability;
- source-grounded discharge preparation;
- extraction validation/correction loop;
- agent tool-policy containment;
- integration-failure observability;
- verification/adoption measurement.

Do **not** build a parallel platform.

### Month 2 — own one vertical slice

```text
hospital source
    ↓
Recare integration
    ↓
structured patient context
    ↓
Agent / document workflow
    ↓
clinician review
    ↓
correction + telemetry
    ↓
eval / regression
```

Own the outcome end to end rather than only the model prompt.

### Month 3 — follow the system into the hospital

Work with implementation on an actual rollout: observe, deploy narrowly, inspect KIS/Citrix/network/support constraints, measure friction and turn what happens back into engineering decisions.

Desired loop:

> **engineer → hospital → engineer**

---

## 4. Partnership architecture hypothesis

```text
                   RECARE PRODUCT

 Integrations ─ Patient Overview ─ Agent ─ Docs/Voice/Operator
       │               │             │
       └───────────────┼─────────────┘
                       │
              ASSURANCE / EVAL PATTERNS
                       │
             provenance + state
             contradiction/freshness
             capability manifests
             policy/tool traces
             adversarial evals
             correction telemetry
                       │
                 HOSPITAL PILOTS
                       │
               Time Returned to Care
```

This is a discussion hypothesis, **not** a recommendation to create another standalone Recare product.

---

## 5. Pitch posture

Bad:

> "I built something Recare should adopt."

Better:

> **"I independently converged toward many of the problems you already solve in production. While doing that I pushed hard on provenance, clinical state, agent authority, adversarial evals and implementation. I do not want to build a parallel stack. I want to learn which of those ideas survive your real hospital integrations and help implement the ones that do."**

That demonstrates independent problem-solving without prototype ego.

---

## Related CareOS evidence

- [Pre-Hospital Handoff](PRE_HOSPITAL_HANDOFF.md)
- [Recare Capstone](RECARE_CAPSTONE.md)
- [Hospital Implementation Playbook](HOSPITAL_IMPLEMENTATION_PLAYBOOK.md)
- [Current Status and Gaps](CURRENT_STATUS_AND_GAPS.md)
- [Agent Security Model](AGENT_SECURITY_MODEL.md)
- [Germany / Global Interoperability Blueprint](GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md)
