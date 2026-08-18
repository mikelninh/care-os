# CareOS Critical Service Operating Model

Baseline: **18 August 2026**

> Future production target: hospitals should experience CareOS as dependable infrastructure with an explicit fallback path, not as a SaaS feature that sometimes disappears.

This document defines target operating standards. It is **not** a current production SLA or contractual promise.

---

# 1. Reliability philosophy

The first reliability question is not:

> "Can we make CareOS never fail?"

It is:

> **"When CareOS or one dependency fails, can the hospital keep caring for patients safely, understand what degraded, and recover without ambiguity?"**

CareOS is deliberately **not** the authoritative KIS/system of record.

```text
CareOS healthy   → faster coherent workflow
CareOS degraded  → visible partial context + restricted automation
CareOS down      → existing hospital source workflows remain available
```

---

# 2. Service hierarchy

## C0 — provider source truth

KIS/EHR/LIS/RIS/PACS and other provider-owned authoritative sources.

CareOS must never make C0 depend on a shared CareOS PHI/control plane. If CareOS fails, the provider's authoritative/legacy workflow remains the fallback.

## C1 — CareOS clinical context

Source-linked composition, lifecycle/freshness/provenance and review state.

A C1 outage is serious because users may depend on this layer for workflow efficiency. The provider must still retain a fallback to C0.

## C2 — bounded agent/model assistance

Drafting, explanation, orchestration and other model-assisted workflows.

C2 is deliberately more disposable. A model/provider failure must not remove C0/C1 access.

## C3 — administrative analytics

Aggregate reporting and other non-critical management capabilities.

`app/service_operating_model.py` makes the hierarchy machine-readable and rejects designs where core bedside truth/context depends on routine PHI in a shared control plane.

---

# 3. Incident severity

## SEV0 — systemic safety/security

Examples:

- wrong-patient isolation risk;
- unauthorized action capability;
- corrupted lifecycle/provenance semantics;
- compromised release affecting multiple providers.

Response rule: **contain first**. Narrow kill scopes should allow model/agent/tool/adapter/workflow/site/release to be disabled independently where possible.

## SEV1 — critical clinical workflow unavailable

CareOS clinical context is unavailable or unsafe for use. The hospital is told to use the authoritative/legacy path.

## SEV2 — degraded optional capability

Example: model/agent assistance unavailable while source-linked context remains available.

## SEV3 — non-critical degradation

Administrative/non-clinical feature issue.

`classify_incident()` provides the first deterministic classification baseline; production incident command remains an organisational responsibility.

---

# 4. Local hospital authority

Every production deployment should preserve provider-local authority to:

- disable a workflow;
- disable an adapter;
- disable agents/model use;
- return to the legacy workflow;
- hold/reject an upgrade;
- inspect local health/audit evidence;
- escalate a provider/vendor dependency.

A central CareOS service must not be the only kill switch.

---

# 5. Upgrade contract

```text
pinned release candidate
→ manifest compatibility check
→ adapter/conformance suite
→ security checks
→ shadow/canary
→ observe safety + reliability + workflow metrics
→ explicit promote OR rollback
```

A vendor/interface version change is a reason to revalidate, not a reason to assume compatibility.

---

# 6. SLO / SLA philosophy

Do **not** publish one vanity uptime number and do not invent contractual percentages before the operating organisation exists.

Future commitments should be capability-specific and evidence-backed, for example:

- provider-source connector availability;
- freshness age for each clinical source/domain;
- identity/auth availability;
- audit durability/ingestion;
- context API latency/availability;
- bounded agent service availability;
- incident acknowledgement/restoration windows by severity.

Targets must come from real target-environment measurement, staffing, failure exercises, dependency behaviour and hospital requirements.

`ServiceCommitment(CONTRACTED)` is deliberately invalid unless the service has:

- a concrete target;
- staffed on-call coverage;
- target-environment exercise evidence;
- evidence references.

## Current commitment

**24/7 SLA: NOT OFFERED.**

That changes only after the team, observability, exercises, responsibilities and contracts can actually carry the dependency.

---

# 7. Failure behaviour

## CareOS unavailable

Required:

- KIS/source workflows remain accessible;
- no partial write left ambiguous;
- hospital IT can identify the outage;
- last-known local display, if enabled, is unmistakably stale/read-only;
- recovery rebuilds from authoritative sources rather than treating CareOS cache as truth.

## One clinical source unavailable

Required:

- other source-linked context may remain visible;
- unavailable source is named;
- completeness becomes false/partial;
- absence assertions are disabled;
- dependent agent claims are suppressed;
- no reassuring empty state.

## Identity unavailable

Required:

- no patient-context guessing;
- no fuzzy fallback matching;
- agent/consequential operations disabled;
- legacy/source path remains the fallback.

## Model unavailable

Required:

- source-linked context still works;
- deterministic features remain;
- agent/draft assistance shows unavailable state;
- no silent swap to an unapproved provider/model.

## Audit unavailable

Consequential/agent operations requiring durable audit fail closed. No unlogged clinical write/send path.

## KIS/vendor upgrade

- compare last-known-good capability manifest;
- replay conformance;
- run shadow/canary;
- promote only after evidence;
- retain rollback.

`app/resilience_drills.py` provides the first executable synthetic failure/recovery contract.

---

# 8. Release strategy

No fleet-wide surprise updates.

```text
0 internal synthetic
1 integration sandbox
2 hospital shadow/canary
3 one workflow / one ward
4 hospital/site
5 hospital group / wider fleet
```

Promotion requires evidence from the previous ring.

Version every consequential input:

- build/container;
- adapter;
- hospital capability profile;
- terminology/mapping;
- policy;
- prompt/model/provider;
- agent/tool registry;
- workflow pack;
- schema.

Never silently change model, clinical prompt behaviour, action authority, mapping semantics, patient identity strategy or source prioritisation.

---

# 9. Hospital relationship cadence

## Pilot

Weekly implementation/value/safety review:

- incidents/friction;
- Time Returned to Care;
- safety stops;
- source/adapter health;
- user questions;
- workflow changes;
- regression items.

For the first go-live days, increase support presence without turning clinicians into infrastructure debuggers.

## Stable production target

Monthly operations review:

- availability/degradation;
- source reliability;
- incidents/near misses;
- support burden;
- adapter/version changes;
- upcoming hospital upgrades;
- security actions.

Quarterly value + safety review:

- Time Returned to Care;
- adoption/abandonment;
- corrections/rejections;
- safety stops;
- verification behaviour;
- clinician/nursing/patient feedback;
- roadmap/expansion decisions.

Annual resilience review where appropriate:

- disaster recovery;
- penetration/security review;
- access/role governance;
- business continuity;
- data-flow/subprocessor review;
- rollback exercise.

---

# 10. Support experience

A nurse or doctor should not need to know whether the problem is "FHIR", "Kubernetes" or "LLM".

Where privacy permits, support tooling should automatically capture non-clinical diagnostics such as:

```text
hospital/site
user role
pseudonymous correlation ID
CareOS version
adapter/source health
workflow/module
visible error state
trace ID
```

Never require a clinician to paste patient data into a support ticket.

Help layers:

1. inline self-explanation;
2. product-support agent with **no clinical authority**;
3. human support;
4. integration/security/clinical-safety escalation as appropriate.

---

# 11. Status transparency

Hospital IT should always be able to answer:

```text
is CareOS up?
which sources are up?
is identity working?
which capability is degraded?
which users/workflows are affected?
what release is running?
what changed?
what is the rollback version?
```

Clinicians should see clinically useful degradation information, not infrastructure noise.

Example:

> **Microbiology source unavailable. Other admitted patient information remains available. Pending/negative microbiology conclusions are disabled until the source is verified again.**

---

# 12. Post-incident learning

Every generalisable incident or near miss should produce at least one of:

- regression fixture;
- conformance test;
- policy rule;
- adapter compatibility record;
- degraded-state UX improvement;
- runbook change.

If hospital #20 repeats a known failure from hospital #3, the infrastructure flywheel is not working.

---

# 13. Disaster / downtime game days

Before critical dependency, exercises should cover:

- network loss;
- KIS/FHIR/LIS loss;
- stale source;
- IdP loss;
- audit loss;
- model-provider loss;
- control-plane loss;
- bad release;
- compromised agent/tool;
- recovery with missed corrected results;
- rollback under load.

Synthetic drills are useful engineering evidence. A real hospital disaster/downtime exercise remains an external gate.

---

# 14. Long-term customer promise

The relationship should feel like:

> **"You can depend on the workflow, understand every important change, keep control of your data and systems, and leave without being trapped."**

That requires:

- exportable configuration/evidence;
- open interfaces;
- no proprietary patient identity;
- no hidden source transformations;
- explicit compatibility records;
- documented migration/offboarding;
- hospital-owned kill authority;
- contractually defined support windows once production commitments exist.

Critical infrastructure earns trust partly by making exit possible.
