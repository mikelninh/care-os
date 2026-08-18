# Hospital Implementation Playbook — Zero-Drama Rollout

Baseline: **18 August 2026**

> Goal: introduce a clinical AI/context workflow with the least possible disruption, prove value before increasing authority, and make rollback easier than escalation.

This playbook is intentionally product-agnostic. It can be used for CareOS research, a Recare deployment, or another hospital AI workflow.

## Core principle

A hospital implementation is not successful because software was installed.

It is successful when:

- clinicians spend less time hunting/re-entering information;
- the workflow is safer or no less safe;
- source verification does not degrade;
- support burden is acceptable;
- users choose to keep using it;
- the hospital can understand, govern and reverse the integration.

North-star metric:

> **Time Returned to Care — gated by safety and verification.**

---

# Phase 0 — Workflow archaeology

Before proposing automation, observe the current workflow.

Do not ask only "what would you like AI to do?"

Ask users to **show the real work**.

Capture a baseline for 5–10 representative cases where feasible:

- elapsed task time;
- KIS/LIS/RIS/PACS/ePA/other systems opened;
- searches;
- window/context switches;
- phone calls/messages;
- manual copy/paste;
- duplicate entry;
- corrections;
- missing/pending items discovered late;
- handoffs;
- workarounds / paper / fax / spreadsheets;
- frustration and cognitive load.

Outputs:

1. workflow map;
2. baseline metrics;
3. pain-ranked opportunity list;
4. explicit non-goals.

Rule:

> Automate the painful step, not the imagined workflow.

---

# Phase 1 — Hospital technical preflight

Create one reusable discovery sheet before engineers start integration work.

## Primary systems

- KIS/EHR vendor + version;
- LIS / microbiology;
- RIS/PACS;
- PVS where relevant;
- document archive;
- medication systems;
- identity / AD / SSO;
- ePA/TI paths;
- local integration engine.

## Interfaces

- HL7 v2 availability;
- FHIR endpoints and versions;
- ISiK profile/stage support;
- vendor APIs;
- file/document feeds;
- event/notification interfaces;
- write-back options;
- sandbox/test environment.

## Workplace reality

- Windows versions;
- browsers;
- Citrix/VDI/RDP;
- workstation restrictions;
- mobile/tablet availability;
- network segmentation;
- proxies/firewalls;
- offline/degraded workflows;
- shared terminals/session behavior.

## Governance / security

- data controller / processor roles;
- DPO/Datenschutz contact;
- CISO/IT security;
- clinical safety/medical leadership;
- works council where relevant;
- AVV/DPA;
- DSFA/DPIA applicability;
- hosting/processing locations;
- identity/role model;
- audit/SIEM requirements;
- retention/deletion;
- incident process;
- subprocessor/model-provider policy.

Classify the implementation before starting:

```text
GREEN  = standard path / known interface / low uncertainty
AMBER  = custom mapping, legacy constraint or governance dependency
RED    = missing authority, unsafe identity context, no reliable source, or unacceptable deployment dependency
```

Do not hide red items inside an implementation estimate.

---

# Phase 2 — Read-only first

Default rollout order:

```text
READ
  ↓
ORGANISE / SUMMARISE
  ↓
DRAFT
  ↓
HUMAN APPROVAL
  ↓
BOUNDED EXECUTION
```

Do not begin with autonomous write-back merely because an API exists.

Initial proof question:

> Can we reliably surface the right patient context with the right source/state semantics inside the clinician workflow?

Read-only exit criteria should include:

- correct patient/encounter binding;
- provenance available for consequential facts;
- pending/unavailable/stale states preserved;
- source outages visible;
- response latency acceptable;
- no second patient search introduced unnecessarily;
- audit functioning;
- rollback tested.

---

# Phase 3 — Shadow mode

Run the new logic without changing the clinician's consequential workflow.

Compare:

```text
what the system would have shown/proposed
vs
what happened in the normal workflow
```

Measure:

- correct/incorrect facts;
- missed items;
- pending-state errors;
- contradictions;
- unsupported claims;
- source failures;
- latency;
- correction burden;
- agent/tool denials;
- user-visible degraded state.

Use shadow failures to create regression tests before widening exposure.

---

# Phase 4 — One workflow, one ward

Avoid a hospital-wide "AI transformation" launch.

Choose:

- one workflow;
- one ward/team;
- one clinical champion;
- one implementation owner;
- one engineering owner;
- one IT/integration owner;
- one measurable outcome.

Example:

> Infectiology discharge-prep / morning review on Ward X.

Pilot charter:

```text
problem
baseline
scope
users
source systems
excluded decisions
human approval boundary
success metrics
safety-stop metrics
rollback owner
review date
```

---

# Phase 5 — Copilot mode

The system may now:

- extract;
- organise;
- surface context;
- draft;
- propose next administrative action.

The human:

- verifies;
- corrects;
- approves;
- remains the authority for consequential clinical output.

Record corrections as training/evaluation evidence, not as hidden cleanup work.

Important telemetry:

- accepted unchanged;
- edited;
- rejected;
- source opened;
- pending item missed;
- contradiction reviewed;
- time to complete;
- reason for abandonment.

---

# Phase 6 — Legacy-system bridge

Integration preference:

1. standards-based interface (FHIR/ISiK/HL7 where appropriate);
2. stable vendor API;
3. provider integration engine;
4. controlled document/file path;
5. UI automation / computer-use only when it is the pragmatic bridge.

Computer-use can be valuable in legacy KIS environments because it avoids long interface projects, but it must be treated as a different risk surface:

- UI/version fragility;
- session ownership;
- concurrent-user behavior;
- field targeting;
- confirmation;
- replay/idempotency;
- screen-state validation;
- audit;
- safe halt on unexpected UI.

Never describe UI automation as equivalent to a typed transactional API.

---

# Phase 7 — Bounded execution

Only consider write/send actions after read/draft value is proven and the deployment's governance permits them.

Every consequential capability should have an explicit manifest:

```text
agent/workflow identity + version
patient/encounter scope
allowed tool
allowed operation
allowed data categories
record/page/runtime budgets
human confirmation
idempotency / replay behavior
audit requirement
egress destinations
kill / revocation mechanism
```

Rules:

- no agent self-escalation;
- no autonomous break-glass;
- write and external send remain separate capabilities;
- retry behavior is explicit;
- human confirmation is bound to the actual proposed action, not a generic prior approval;
- failed/partial execution is visible.

---

# Phase 8 — Measure before scale

A rollout dashboard should include **benefit and risk together**.

## Benefit

- median task time;
- searches/window switches;
- calls/messages;
- manual entries;
- overtime/admin burden where reliably measurable;
- user effort;
- adoption;
- repeat use.

## Reliability / safety

- wrong-patient events;
- source outages;
- unsupported facts;
- stale/pending confusion;
- missed pending items;
- corrections;
- contradictions requiring review;
- write/tool denials;
- system availability;
- degraded-mode frequency;
- support tickets.

## Verification behavior

- source-opening rate;
- acceptance without source check;
- draft-vs-source confusion;
- correction after source review.

Decision:

```text
PASS -> expand carefully
HOLD -> fix / gather more evidence
FAIL -> rollback or redesign
```

A speed win does **not** override a safety-stop event.

---

# Phase 9 — Repeatability

Do not call the approach scalable after one successful ward.

Next proof:

1. second ward / specialty;
2. second KIS or vendor configuration;
3. second hospital;
4. no fork of the core clinical-state/evidence/agent contracts.

Track per deployment:

- connector work hours;
- mapping differences;
- policy differences;
- workflow configuration;
- custom code introduced;
- deployment lead time;
- test reuse rate;
- support burden.

The goal is to move hospital variation into **versioned adapters/packs/configuration**, not branches of the core product.

---

# Hospital implementation team

A practical minimum cross-functional group:

| Role | Responsibility |
|---|---|
| clinical sponsor | outcome, scope, escalation |
| clinician champion | workflow truth + user feedback |
| implementation owner | rollout coordination |
| integration engineer | source interfaces / mapping |
| AI/product engineer | agent/model/workflow behavior |
| hospital IT | infrastructure / operations |
| security / DPO | controls / privacy / risk |
| product | scope + adoption + metrics |
| support | incident / friction feedback |

One person may cover multiple roles in a small pilot, but the responsibilities must remain explicit.

---

# The implementation experience we want

For the hospital:

```text
one discovery package
one accountable implementation owner
one technical preflight
one privacy/security evidence pack
one synthetic conformance suite
one pilot dashboard
one rollback plan
```

For clinicians:

```text
no new patient search if avoidable
minimal new UI
source visible when needed
uncertainty visible
fast correction
human authority obvious
no hidden background writes
```

For hospital IT:

```text
known interfaces
known egress
known data flows
known model/providers
known failure modes
known logs
known update path
known rollback
```

---

# CareOS assets supporting this playbook

- [Pre-Hospital Handoff](PRE_HOSPITAL_HANDOFF.md)
- [Reference Architecture V2](ARCHITECTURE_V2.md)
- [Deployment Patterns](DEPLOYMENT_PATTERNS.md)
- [Trust & Data Flow](TRUST_AND_DATA_FLOW.md)
- [Hospital Assurance Pack](HOSPITAL_ASSURANCE_PACK.md)
- [Responsibility Model](RESPONSIBILITY_MODEL.md)
- [Safety Case](SAFETY_CASE.md)
- [Agent Security Model](AGENT_SECURITY_MODEL.md)
- [Recare Collaboration Map](RECARE_COLLABORATION_MAP.md)

> **Best implementation strategy: reduce uncertainty in layers, earn authority from evidence, and never make the hospital absorb complexity merely because the software can.**
