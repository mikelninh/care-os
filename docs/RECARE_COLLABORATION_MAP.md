# Recare x CareOS — Collaboration Map

Baseline: **18 August 2026**

> This is a public-product comparison and collaboration hypothesis, not a claim about Recare's private architecture or internal gaps.

## 1. The key conclusion

CareOS should **not** be positioned as a competing product to Recare.

Publicly, Recare has already built much of the clinical product layer CareOS independently converged toward: patient overview, extraction, document generation, voice documentation, an AI agent, KIS write-back via Operator, discharge coordination and prediction.

The useful contribution from CareOS is therefore the **engineering research underneath and around the workflow**:

- clinical-state semantics;
- source provenance / evidence contracts;
- deterministic agent authorization;
- adversarial evaluation;
- verification-preserving outcome measurement;
- global portability / trust separation;
- low-friction hospital implementation methodology.

The collaboration question is not:

> "Will Recare replace its stack with CareOS?"

It is:

> **"Which CareOS invariants and evaluation patterns survive contact with Recare's real product, integrations and hospitals — and where can they make the existing platform stronger?"**

---

# 2. What Recare publicly offers today

Current public product baseline:

| Recare capability | Publicly described role | CareOS relationship |
|---|---|---|
| Patient Overview | structured patient profile combining Recare/KIS/document data; diagnoses, medication, labs, allergies, notes; role-based views | strong product overlap |
| Extract | structured extraction from KIS, PDFs, scans and free text | strong overlap with document/truth pipeline |
| Docs | review-ready clinical documents | overlap with grounded drafting |
| Voice | real-time documentation / form filling from conversations | complementary |
| Agent | combines documentation, extraction, transfer and patient-context interaction | strong overlap with agent workflow |
| Operator | computer-use transfer of Recare-created content into the existing KIS | complementary legacy bridge |
| Discharge | digital discharge / post-acute coordination network | Recare-specific production moat |
| Predict | early identification of post-acute needs | complementary |

Public references:

- https://recareai.com/krankenhaus
- https://recareai.com/krankenhaus/recare-patient-overview
- https://recareai.com/krankenhaus/recare-agent
- https://recareai.com/krankenhaus/recare-operator

Publicly, Patient Overview explicitly keeps the KIS as the central system of record, structures information above it and marks information from unstructured sources as unvalidated until clinical personnel confirm it. This is philosophically close to CareOS's own "systems of record stay authoritative" and model-output-is-not-truth rules.

---

# 3. Where CareOS research can add value

These are **areas to investigate**, not assertions that Recare lacks them internally.

## 3.1 Clinical lifecycle semantics

CareOS treats clinical state as part of correctness:

```text
final
preliminary
pending
corrected
cancelled
stale
unavailable
contradictory
unknown
```

Key questions for a real Recare architecture:

- How is lifecycle state normalized across KIS/LIS/document sources?
- How are preliminary -> final -> corrected transitions handled?
- How does a source outage propagate to generated context?
- Can an agent ever collapse pending/unavailable into an apparent negative?
- How are contradictions surfaced rather than silently resolved?

Potential contribution: reusable state contract + lifecycle regression fixtures.

## 3.2 Provenance and evidence contracts

CareOS treats provenance as correctness, not decorative metadata.

A consequential fact should be able to retain:

```text
value / original wording
source organisation/system
resource/document identifier
clinical effective time
recorded / ingestion time
version / freshness
terminology mapping lineage
evidence span where document-derived
review state
contradiction / supersession state
```

Potential contribution: define/extend a machine-readable evidence contract that can travel through Patient Overview -> Agent -> Docs -> human approval.

## 3.3 Zero-trust agent authority

Recare has a real Agent product. CareOS's specific research question is:

> **If the reasoning model is compromised, what can it still do?**

CareOS keeps authority outside the model through:

- signed/narrow delegation;
- patient/encounter/task binding;
- versioned tools;
- operation and data-category allowlists;
- execution budgets;
- deny-default egress;
- human-confirmation requirements;
- kill/revocation path;
- audit;
- trusted Tool Proxy.

Potential contribution: use the CareOS hostile-worker / capability-manifest pattern as a red-team and assurance layer around real agent workflows.

## 3.4 Agent observability and evals

The Recare capstone turns failures into replayable scenarios:

- wrong patient;
- prompt injection;
- source unavailable;
- stale result;
- unauthorised write;
- pending/conflict retention.

Potential contribution: production eval suites that combine model quality, tool correctness, authorization and user-visible failure behavior.

## 3.5 Outcome metric: Time Returned to Care

CareOS does not treat speed alone as success.

Core outcome set:

- task time;
- source checks;
- corrections;
- missed pending items;
- unsupported claims;
- verification decay;
- user effort;
- adoption / abandonment;
- degraded-mode behavior.

A safety-stop overrides a speed win.

Potential contribution: pair Recare's real product metrics with clinician workflow/safety metrics instead of evaluating model output alone.

## 3.6 Interoperability beyond transport

Recare publicly describes HL7/KIS integration and works with existing hospital systems. CareOS adds a research thesis that **transport interoperability is necessary but insufficient**.

Three layers:

1. **content interoperability** — what does the clinical item mean?
2. **trust interoperability** — who issued it and can the receiver verify that?
3. **policy interoperability** — may the receiving context use it for this purpose?

Potential contribution: preserve source state/provenance across ISiK/FHIR -> EHDS/IPS portability rather than treating successful API transfer as the end state.

---

# 4. What to do if joining Recare

## Days 1–15 — reality absorption

Do not arrive with a rewrite proposal.

Spend time with:

- interoperability/integration engineers;
- AI/ML engineers;
- implementation;
- product;
- support;
- clinicians;
- hospital IT / security where possible.

Questions:

```text
Which KIS/LIS integrations generate the most pain?
What breaks most often?
What is the highest-support workflow?
Which clinical-source states are hardest to normalize?
Where do clinicians correct or distrust AI output?
How are agent failures traced today?
What integration work cannot be standardized?
Which assumptions in CareOS are simply wrong?
```

Output: `CareOS idea -> Recare reality` map.

Every CareOS concept gets one disposition:

- already solved better -> retire the duplicate;
- useful invariant -> integrate into existing architecture;
- useful test/eval -> port;
- wrong assumption -> document and remove;
- genuinely unresolved problem -> candidate roadmap item.

## Days 15–30 — choose one real problem

Prefer one narrow production-relevant workflow, e.g.:

- Patient Overview clinical-state/provenance reliability;
- source-grounded discharge preparation;
- document-extraction validation / correction loop;
- agent tool-policy containment;
- integration-failure observability;
- clinician verification/adoption measurement.

Do **not** build a parallel platform.

## Month 2 — own one vertical slice

Example:

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

Own the outcome end-to-end rather than only the model prompt.

## Month 3 — follow the system into the hospital

Work with implementation on an actual rollout:

- observe the workflow;
- sit with users;
- understand KIS/Citrix/browser/network constraints;
- inspect failure/support patterns;
- modify product/engineering based on observed friction;
- measure before/after workflow outcome.

The desired professional loop is:

> **engineer -> hospital -> engineer**

---

# 5. Partnership architecture hypothesis

A useful collaboration shape could be:

```text
                   RECARE PRODUCT

 Integrations ─ Patient Overview ─ Agent ─ Docs/Voice/Operator
       │               │             │
       └───────────────┼─────────────┘
                       │
              ASSURANCE / EVAL LAYER
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

This is a hypothesis for discussion, not a recommendation to add a new standalone Recare product.

---

# 6. The pitch posture

Bad framing:

> "I built something Recare should adopt."

Better framing:

> **"I independently converged toward many of the same problems you are already solving in production. While doing that I pushed hard on provenance, clinical state, agent authority, adversarial evals and implementation. I do not want to build a parallel stack. I want to learn which of those ideas survive your real hospital integrations and help implement the ones that do."**

This demonstrates:

- independent problem-solving;
- respect for production reality;
- no prototype/founder ego;
- genuine interest in implementation;
- willingness to delete work when the real system is better;
- focus on measurable patient/clinician outcomes.

---

# 7. Related CareOS evidence

- [Pre-Hospital Handoff](PRE_HOSPITAL_HANDOFF.md)
- [Recare Capstone](RECARE_CAPSTONE.md)
- [Hospital Implementation Playbook](HOSPITAL_IMPLEMENTATION_PLAYBOOK.md)
- [Current Status and Gaps](CURRENT_STATUS_AND_GAPS.md)
- [Agent Security Model](AGENT_SECURITY_MODEL.md)
- [Germany / Global Interoperability Blueprint](GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md)
