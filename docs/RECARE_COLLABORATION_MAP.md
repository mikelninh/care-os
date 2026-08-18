# Recare × CareOS — Collaboration Map

Baseline: **18 August 2026**

> Comparison of Recare's public product information with CareOS research. This is **not** a claim about Recare's private architecture, controls, implementation burden or missing capabilities.

## Executive conclusion

CareOS should **not** be positioned as a competing product to Recare.

Recare already operates the real hospital product/integration layer across Patient Overview, extraction, documents, voice, agents, discharge, prediction and KIS transfer. CareOS is a narrower **synthetic R&D / assurance / interoperability artifact**.

The collaboration question is:

> **Which CareOS invariants, evals and integration patterns survive contact with Recare's real hospitals — and where can they make an existing production platform easier to scale?**

---

## 1. Public Recare baseline

| Recare capability | Publicly described role | CareOS relationship |
|---|---|---|
| **Patient Overview** | structured patient profile combining KIS/Recare/document information | strong product overlap |
| **Extract** | structured extraction from findings, PDFs, scans and free text | overlap with evidence/truth pipeline |
| **Docs** | reviewable clinical documents | overlap with grounded drafting |
| **Voice** | real-time documentation/form filling | complementary |
| **Agent** | documentation, extraction, transfer and patient-context interaction | strong workflow overlap |
| **Clinical decision support via Prof. Valmed** | regulated CDS integrated into patient-context workflows | broader intended use than CareOS capstone |
| **Operator** | computer-use transfer of Recare-created information into existing KIS UI | important legacy bridge |
| **Discharge / Predict** | production discharge network and post-acute workflows | Recare production moat |

Public references are kept in [Recare Integration Accelerator](RECARE_INTEGRATION_ACCELERATOR.md).

### Maturity boundary

**Recare:** production hospital platform, real integrations, security/operations and real implementation experience.

**CareOS:** synthetic/pre-hospital research, blocked live PHI/write-back, narrow capstone, reference contracts and evaluation methods.

Do not imply equivalence.

---

# 2. Where CareOS research may contribute

These are investigation areas — **not assertions that Recare lacks them internally**.

## 2.1 Clinical lifecycle semantics

CareOS makes states explicit:

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

Questions for production reality:

- How are these normalized across KIS/LIS/document sources?
- Can pending/unavailable ever collapse into apparent absence?
- How do preliminary → final → corrected transitions propagate through Patient Overview / Agent / Docs?
- How are unresolved conflicts presented?

Potential contribution: reusable lifecycle contract + regression fixtures.

## 2.2 Provenance contracts

Consequential information should be able to retain:

```text
original value / wording
source organisation/system/resource
clinical effective time
recorded / ingestion time
version + freshness
terminology mapping lineage
evidence span
review / contradiction / supersession state
```

Potential contribution: test provenance survival from integration → context → agent/document → human approval.

## 2.3 Agent authority + containment

CareOS assumes reasoning models and source documents can be hostile.

Authority stays outside the model through:

- patient/encounter/task-bound delegation;
- versioned tools;
- operation/data allowlists;
- budgets;
- deny-default egress;
- human-confirmation rules;
- revocation/kill path;
- trusted Tool Proxy;
- audit.

Potential contribution: hostile-worker and tool-capability regressions around real agent workflows.

## 2.4 Agent observability + evals

CareOS turns failures into replayable scenarios:

- wrong patient;
- prompt injection;
- source unavailable;
- stale result;
- unauthorised write;
- pending/conflict retention.

Potential contribution: one eval surface across model, tool, authorization and user-visible degraded behavior.

## 2.5 Time Returned to Care — safety gated

Measure:

- task time;
- source checks;
- corrections;
- missed pending work;
- unsupported claims;
- verification decay;
- effort;
- adoption/abandonment.

A safety-stop overrides a speed win.

## 2.6 Interoperability beyond transport

CareOS separates:

1. **content** — what does the clinical item mean?
2. **trust** — who issued it / can the receiver verify it?
3. **policy** — may this receiving context use it for this purpose?

Potential contribution: preserve lifecycle/provenance semantics across source integration and later EU/global portability.

---

# 3. New collaboration hypothesis: integration as a product

Recare already knows far more about real hospital integration than CareOS does.

The useful hypothesis is therefore not:

> "CareOS can teach Recare how to integrate hospitals."

It is:

> **"Can the integration knowledge already accumulated across hospitals become increasingly machine-readable, testable and reusable so marginal deployment effort trends toward configuration + conformance rather than bespoke engineering?"**

CareOS now prototypes:

```text
Hospital Capability Manifest
        ↓
automatic adapter selection + maturity check
        ↓
FHIR capability discovery
        ↓
conformance / identity / source-state gates
        ↓
hospital-local data plane
        ↓
Docker / Helm deployment scaffold
        ↓
upgrade compatibility preflight
        ↓
shadow / rollout evidence
```

See [Recare Integration Accelerator](RECARE_INTEGRATION_ACCELERATOR.md) and [Hospital Self-Install Platform](HOSPITAL_SELF_INSTALL_PLATFORM.md).

### Questions for Pavlo

Before proposing any implementation, ask:

- Do you already have an internal adapter SDK/capability registry?
- How much site integration is configuration vs custom engineering?
- How are KIS/vendor/version profiles tracked?
- Where do HL7 integrations actually break most: identity, semantics, mapping, transport or operations?
- How are upgrades regression-tested?
- How is Operator UI/version compatibility tested?
- Can hospital IT self-configure any part today?
- Which security/network documents are recreated per customer?
- What is the time from signed hospital to first useful integrated workflow?
- Which step consumes the most integration-team time?

If Recare already solves these better, retire the duplicate CareOS idea and learn from the real system.

---

# 4. If joining Recare

## Days 1–15 — absorb reality

Spend time with:

- interoperability/integration engineering;
- AI/ML engineering;
- implementation;
- product/support;
- clinicians;
- hospital IT/security where possible.

Create a simple matrix:

```text
CareOS idea
→ already solved better
→ useful invariant/test
→ wrong assumption
→ unresolved production problem
```

Do not preserve prototype ideas for ego.

## Days 15–30 — choose one production problem

Strong candidates:

- Patient Overview source-state/provenance reliability;
- integration failure observability;
- adapter/version conformance;
- upgrade preflight;
- agent tool-policy containment;
- verification/correction measurement;
- source-grounded discharge/documentation workflow.

## Month 2 — own one vertical slice

```text
hospital source
    ↓
integration adapter
    ↓
structured clinical context
    ↓
agent / documentation workflow
    ↓
clinician review
    ↓
correction + telemetry
    ↓
regression evidence
```

## Month 3 — follow it into a hospital

Desired loop:

> **engineer → hospital → engineer**

Observe real KIS/Citrix/network/support constraints, measure friction and turn what happens into platform improvements.

---

# 5. Partnership architecture hypothesis

```text
                         RECARE

 integrations ─ Patient Overview ─ Agent ─ Docs/Voice/Operator
      │                 │             │
      └─────────────────┼─────────────┘
                        │
              reusable assurance layer
                        │
        provenance · lifecycle · identity
        adapter/version conformance
        policy/tool traces · adversarial evals
        upgrade preflight · correction telemetry
                        │
                  hospital rollouts
                        │
              Time Returned to Care
```

This is a discussion hypothesis, **not** a recommendation to create another standalone Recare product.

---

# 6. Pitch posture

Bad:

> "I built something Recare should adopt."

Better:

> **"I independently converged toward many of the problems you already solve in production. I pushed hard on provenance, clinical state, agent authority, adversarial evaluation and now repeatable hospital integration. I don't want to build a parallel stack. I want to learn which ideas survive your real architecture and help implement the ones that do."**

---

## Related evidence

- [Recare Integration Accelerator](RECARE_INTEGRATION_ACCELERATOR.md)
- [Hospital Self-Install Platform](HOSPITAL_SELF_INSTALL_PLATFORM.md)
- [Pre-Hospital Handoff](PRE_HOSPITAL_HANDOFF.md)
- [Recare Capstone](RECARE_CAPSTONE.md)
- [Hospital Implementation Playbook](HOSPITAL_IMPLEMENTATION_PLAYBOOK.md)
- [Current Status & Gaps](CURRENT_STATUS_AND_GAPS.md)
- [Agent Security Model](AGENT_SECURITY_MODEL.md)
- [CareOS Endgame](ENDGAME.md)
