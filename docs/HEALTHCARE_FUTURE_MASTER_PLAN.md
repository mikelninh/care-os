# CareOS Healthcare Future Master Plan

Baseline: **18 August 2026**

> **Mission:** return time, clarity and agency to care while making the underlying information flow more trustworthy, interoperable, resilient and humane.

This is the **north-star + execution contract**. It describes what future healthcare should feel like and the evidence ladder for getting there. It is not a claim that the future state exists today.

Current implementation truth lives in:

- `docs/FOUNDATION_IMPLEMENTATION_STATUS.md`;
- `docs/CURRENT_STATUS_AND_GAPS.md`;
- `docs/GATES.md`.

The endgame/governance model lives in `docs/ENDGAME.md`.

---

# 1. The future-state test

A healthcare system is moving in the right direction when all of these become true **together**.

## Clinicians

- open the patient once;
- current relevant context is assembled before they hunt for it;
- pending, stale, unavailable, contradictory and corrected information remain distinct;
- important changes since last review are obvious;
- original evidence is quickly inspectable;
- repetitive documentation is prepared rather than retyped;
- routine coordination becomes structured/stateful;
- AI may prepare/explain but cannot silently invent authority;
- the system works on real Windows/Citrix/tablet/network conditions;
- legacy care remains usable when CareOS/AI fails.

## Patients/families

- understand what happened, what changed, what is pending and what happens next;
- source wording remains available behind explanations/translations;
- can access/share/delegate where governing infrastructure permits it;
- can flag possible errors through a governed workflow;
- can carry a portable summary without losing trust/provenance/state;
- do not receive false reassurance from missing/incomplete data.

## Hospital IT

- describe non-secret capabilities once;
- reuse adapters/conformance/compatibility evidence across sites;
- know data flows, egress and credential boundaries;
- upgrades are checked before dependency;
- canary/rollback is normal operating practice;
- routine PHI does not need a central shared control plane;
- changing one source vendor does not force every app integration to be rebuilt.

## Providers / health system

- referrals/transfers/discharge become stateful workflows rather than “document sent”;
- only purpose-relevant context travels;
- provenance/lifecycle/trust survive transport;
- vendors compete without trapping providers;
- citizens retain transparency/agency;
- every deployment makes the next deployment cheaper and safer.

---

# 2. North-star outcome: Time Returned to Care

> **Measure workflow benefit and safety together.**

Initial targets are hypotheses, not current outcomes:

| Role/workflow | First useful target | Must not worsen |
|---|---:|---|
| physician review/documentation | 20–30 min / affected shift workflow | missed pending work, unsupported facts, source verification |
| nursing handover/coordination | 10–15 min / affected shift workflow | omissions, duplicate tasks, alert burden |
| discharge/case management | 15–20 min / eligible case | inappropriate sharing, missing-field loops, status correctness |
| hospital IT routine supported change | days → hours | security review, conformance, rollback evidence |
| patient/family | high teach-back success | false certainty, hidden pending state |

A speed improvement is invalid if a safety stop occurs.

Core safety metrics:

- wrong patient;
- unsupported consequential fact;
- pending→negative;
- stale→current;
- unavailable→absent;
- contradiction loss;
- draft/source-truth confusion;
- unauthorised tool/action;
- inappropriate disclosure;
- incomplete audit;
- failed rollback/recovery;
- verification decay.

Experience metrics:

- time to orientation;
- systems/windows opened;
- searches/context switches;
- copy/paste/manual re-entry;
- information-only calls/faxes/messages;
- correction burden;
- cognitive effort;
- voluntary reuse/adoption;
- patient comprehension.

---

# 3. One trustworthy foundation, different role views

The same source-linked context should not become one universal screen.

## Physician

```text
open patient
→ changed / pending / contradictory / stale
→ source-linked current context
→ human plan
→ prepared note/handover/discharge draft
→ inspect consequential sources
→ decide/sign
```

## Nursing

- changes this shift;
- do-next / overdue / pending work;
- care-relevant exceptions;
- isolation/infection-control state;
- medication/order changes;
- governed handover preparation;
- no new alert firehose.

## Emergency

- minimal trustworthy orientation in seconds;
- allergies/critical meds/major diagnoses/recent encounters;
- recency/provenance obvious;
- governed break-glass where applicable;
- no dependency on an optional AI service for core context.

## Pharmacy / medication safety

- current medication state + source/version/time;
- changes/discontinuations;
- allergy/intolerance;
- reconciliation conflicts;
- agent prepares discrepancies; humans resolve them.

## Diagnostics / laboratory

- order/specimen/result relationships preserved;
- preliminary/final/corrected/cancelled state preserved;
- critical-result acknowledgement explicit;
- late/corrected results reopen affected derived work.

## Discharge / case management

- aftercare need visible early;
- minimum necessary context assembled once;
- missing information explicit;
- approved routing;
- structured reply/status;
- patient/family sees the next step.

## Practice / outpatient

- structured referral + source docs where needed;
- recent hospital events/med changes understandable;
- follow-up responsibility explicit;
- results return through interoperable rails;
- no retyping solely because the institution changed.

## Patient / family / proxy

```text
Today
What happened
What changed
What is still pending
What happens next + owner
Medication changes
Appointments/follow-up
Documents/sources
Questions to ask
Report possible error
Share/delegate where permitted
```

## Hospital IT / integration

```text
careos init
→ describe/discover systems
→ adapter plan
→ identity strategy
→ conformance
→ review pack
→ deploy sandbox
→ shadow/canary
→ upgrade-check
→ promote/rollback
```

## DPO / CISO / clinical safety / leadership

Need reviewable contracts, owner lanes, model/provider boundaries, audit, risk/rollback evidence and honest value/safety measurement—not a black-box “AI score.”

---

# 4. Devices and interaction

Healthcare is contextual, not “desktop versus mobile.”

## Managed Windows / Citrix / VDI

- keyboard-first;
- dense but calm hierarchy;
- no GPU assumption;
- resilient to latency;
- browser deployment where feasible;
- same-patient launch from KIS when possible.

## Tablet

- rounds/bedside/nursing/patient explanation;
- touch-friendly;
- safe re-auth/context switching;
- no hidden hover dependencies.

## Phone

- lightweight status/tasks/patient access;
- not the default surface for complex clinical judgment.

## Shared terminal

- aggressive user/patient context isolation;
- visible patient banner;
- fast logout/lock;
- no previous-user residue;
- re-auth for consequential actions.

## Voice

Voice/dictation is untrusted input until reviewed. Consequential commands require exact confirmation and retention policy must be explicit.

---

# 5. Failure is part of the product

CareOS models:

```text
NORMAL
DEGRADED
OFFLINE
RECOVERY
```

## Rules

- source failure never becomes “no finding”;
- stale cache is visibly stale;
- model outage removes AI convenience before source truth;
- identity failure blocks scoped/consequential work;
- only explicit idempotent non-consequential work may queue;
- hidden clinical writes never queue;
- legacy workflow remains fallback;
- network restored → RECOVERY, not automatically NORMAL;
- reconcile missed versions/events first;
- changed/corrected source facts may invalidate downstream drafts before normal operation returns.

> **AI convenience may disappear before source truth, identity, audit or legacy care pathways do.**

---

# 6. Patient-local clinical context graph

Healthcare is relational/temporal:

```text
patient
├─ encounter
│  ├─ diagnosis
│  ├─ order → specimen → result
│  ├─ medication
│  └─ document
├─ care team
├─ tasks
└─ follow-up
```

Graph rules:

- derived/source/proposed relationships are distinct;
- every consequential relation traces to evidence/explicit artifact;
- patient partitions are hard;
- no fuzzy cross-patient merge;
- lifecycle/version/time explicit;
- graph is reconstructable from evidence + transformations;
- source correction can find/reopen dependent artifacts;
- signed human records are never silently rewritten.

The graph is a derived evidence view, not an AI-created truth database.

---

# 7. Agent architecture

Useful agents are workflow agents, not autonomous “AI doctors.”

Potential classes:

- orientation;
- documentation;
- coordination;
- verification;
- patient explanation;
- IT integration support;
- operations support.

Universal authority contract:

```text
agent identity/version
human/workflow delegator
patient/encounter/task scope
allowed tools/operations/data
network destinations
budgets/timeouts
source/evidence requirement
human confirmation rule
write/send separation
audit
revocation/kill switch
```

> **Model may interpret and propose. Deterministic policy owns authority. Humans retain consequential clinical judgment.**

---

# 8. The first irresistible workflow

Do not start by promising to fix all healthcare.

First clinical hypothesis:

> **Fast orientation around changed/pending/conflicting source-linked context + a reviewable draft for one high-friction daily workflow.**

Why:

- frequent;
- immediately useful;
- read-first limits authority;
- measurable;
- exercises the interoperability foundation;
- creates trust before automation expands;
- generates real product evidence.

Current reference workflow: Infectiology morning review/handover/discharge preparation around microbiology, documented anti-infective therapy, isolation, trends, pending work and documentation.

---

# 9. How a hospital should start

## Before day 1

- workflow archaeology;
- baseline measurements;
- capability manifest;
- identity/context-launch facts;
- synthetic/deidentified conformance;
- security/privacy/data-flow review;
- one workflow;
- explicit owners/stop thresholds.

## Day 1

Read-only shadow. Nothing clinical depends on CareOS.

## Days 2–5

- implementation + engineering + clinicians review recurring friction;
- every meaningful mismatch becomes a fixture/regression;
- compare source verification and safety behavior;
- UI changes respond to repeated real friction, not aesthetic guesses.

## Then

```text
PASS → bounded read-only copilot
HOLD → fix/test
FAIL → remove/rollback
```

Dependency must be earned.

---

# 10. Real synthetic user evidence

Use paired matched synthetic cases:

```text
fragmented baseline
vs
CareOS-assisted workflow
```

Counterbalance order and case variant.

Measure:

- task seconds;
- systems opened;
- context switches;
- source opens;
- errors;
- missed pending items;
- corrections;
- verification behavior;
- cognitive effort;
- structured friction;
- safety stops.

Do not highlight a role/workflow directional result before ≥5 complete safe pairs with both order directions represented.

This is usability/workflow evidence—not clinical efficacy.

---

# 11. Cross-provider continuity

A referral/transfer/discharge should be a stateful care process:

```text
requested
→ received
→ accepted/declined
→ scheduled
→ performed
→ result available
→ follow-up complete
```

Transport should preserve:

- patient binding;
- sender/issuer;
- purpose/restrictions;
- source/provenance;
- lifecycle/trust;
- acknowledgement/status.

“PDF sent” is evidence of transmission, not completion of care.

---

# 12. Patient agency

CareOS complements governing patient-access infrastructure rather than creating an ungoverned duplicate record.

Goals:

- source-linked patient presentation;
- plain language/translation separate from source truth;
- pending/corrected/unavailable visible;
- governed proxy/delegation;
- access/share visibility where infrastructure permits it;
- error/dispute workflow;
- emergency access separate from routine;
- dedicated policy for children/guardianship/sensitive domains;
- no critical smartphone-only path.

> **Patients should not need to reverse-engineer their own care from a stack of PDFs.**

---

# 13. Critical-service operating discipline

If hospitals depend on a capability, it becomes a service obligation.

Design includes:

- criticality tiers;
- severity/escalation;
- model/agent/tool/adapter/workflow/site/release kill scopes;
- hospital-local rollback;
- staged releases/canary;
- outage game days;
- post-incident → regression rule;
- monthly/quarterly value+safety review.

Do not publish contractual SLA numbers before staffing and target-environment evidence exist.

Current state: **24/7 contractual SLA not offered.**

---

# 14. Scope order

## Phase 0 — pre-hospital foundation

Clinical truth, patient identity, lifecycle/state, graph, agent authority, resilience, install/adapter/rollout contracts, patient foundation and measurement machinery.

**Engineering foundation is now coherent enough for external testing.**

## Phase 1 — real synthetic users

Physician morning review first. Then nursing and discharge/case management if the first workflow teaches us something useful.

## Phase 2 — one real hospital/reality boundary

- real workflow observation;
- capability manifest with IT;
- approved deidentified/vendor sandbox;
- privacy/security review;
- shadow;
- read-only pilot only if evidence earns it.

## Phase 3 — repeatability

- second source/vendor configuration;
- second hospital;
- measure custom code/hours/site;
- prove configuration+conformance+compatibility reuse.

## Phase 4 — cross-provider continuity

Real hospital↔practice/referral/follow-up transport + patient continuity.

## Phase 5 — specialty expansion

Only from real pull/impact. Core contracts stay stable; specialty differences live in views/workflows/policies/evals.

## Phase 6 — Germany-scale contribution

Real reusable profiles/adapters, ePA/TI/ISiK/KIM integration where relevant, multi-site operations and independent assurance.

## Phase 7 — EU/global portability

FHIR/IPS + regional/country trust/policy/terminology + real cross-border evidence.

---

# 15. Readiness is a vector, not a percentage

Do not use one completion percentage or architecture score.

Review independently:

```text
clinical usefulness
clinical-truth quality
clinical safety evidence
interoperability coverage
identity/access assurance
security/privacy assurance
resilience/operations
patient agency
workflow adoption
multi-hospital repeatability
national portability
global portability
open governance/reversibility
```

Today the asymmetry matters more than a score:

- **pre-hospital architecture/contracts:** strong enough to critique/test;
- **real participant evidence:** not yet established;
- **real hospital/vendor evidence:** not yet established;
- **production PHI/operations/regulatory assurance:** intentionally blocked;
- **multi-hospital repeatability:** not evidenced;
- **national/global infrastructure:** research/endgame, not production evidence.

> **We are far along in making the hypothesis falsifiable and still near the beginning of proving it in reality.**

---

# 16. Permanent hard questions

Every serious roadmap review should revisit these:

1. Which information should not be centralised?
2. Who is authoritative when sources conflict?
3. How is patient identity proven safely across institutions?
4. How do we stop helpful AI increasing automation bias?
5. What works during total network/model/control-plane failure?
6. Which functions become medical-device functionality as intended use changes?
7. Who owns harm when source, adapter, model and human all contribute?
8. How do patients challenge incorrect information?
9. How do we support low digital literacy, disability and poor connectivity?
10. How do children/guardians/proxies/sensitive domains differ?
11. How do we avoid national interoperability becoming surveillance infrastructure?
12. How do we audit safely without creating another high-value privacy target?
13. When/how can legacy workflows be retired?
14. How do vendor extensions avoid recreating lock-in above FHIR?
15. Who funds open adapters/conformance for decades?
16. Does saved time become patient-facing/judgment time or only more throughput?
17. How do we prevent alert fatigue and AI-generated work?
18. When should an agent abstain?
19. What is minimum viable emergency/offline context?
20. Are benefits equitable across language/age/disability/socioeconomic groups?
21. What if the interoperability layer itself becomes a systemic dependency?
22. How do updates avoid multi-hospital blast radius?
23. Who independently governs/conforms/certifies the open contract?
24. Can a hospital leave the implementation without losing integration knowledge?
25. Are we improving care—or merely making a broken workflow faster?

The endgame must stay answerable to these questions.

---

# 17. Definition of success

The best testimonials are not about AI.

A clinician:

> “I know what changed, what is pending and where it came from. I spend my time deciding and caring rather than reconstructing the chart.”

A nurse:

> “Handover is calmer. I know what remains unfinished. It is not another alert system.”

A patient:

> “I understand what happened and what happens next.”

Hospital IT:

> “We detected the compatibility problem before rollout, and changing one source did not mean rebuilding every app.”

The ecosystem:

> “Information follows the patient through governed interoperable infrastructure instead of forcing people to become the integration layer.”

That is the future we work backward from.