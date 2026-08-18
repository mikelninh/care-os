# CareOS Critical Service Operating Model

Baseline: **18 August 2026**

> Future production target: hospitals should experience CareOS as dependable infrastructure with an explicit fallback path, not as a SaaS feature that sometimes disappears.

This document defines target operating standards. It is **not** a current production SLA or contractual promise.

---

# 1. Reliability philosophy

The first reliability question is not:

> "Can we make CareOS never fail?"

It is:

> **"When CareOS or one of its dependencies fails, can the hospital keep caring for patients safely, understand what degraded, and recover without ambiguity?"**

CareOS is deliberately **not** the authoritative KIS/system of record.

That creates a safer operating pattern:

```text
CareOS healthy   → faster coherent workflow
CareOS degraded  → visible partial context + restricted automation
CareOS down      → existing hospital source workflows remain available
```

---

# 2. Production service tiers

## Tier 0 — synthetic/deidentified evaluation

- business-hours support acceptable;
- no live clinical dependency;
- no PHI unless approved deidentified environment;
- no consequential write.

## Tier 1 — read-only shadow

- production-like monitoring;
- no clinician dependency;
- incident response during agreed pilot window;
- source and identity failures measured.

## Tier 2 — clinician read/draft copilot

- 24/7 critical support path for participating workflows;
- source fallback remains available;
- rollback tested;
- model outage does not remove core source-linked context.

## Tier 3 — bounded execution

Only after much stronger evidence.

- 24/7 Sev-0/Sev-1 operations;
- write/read-after-write verification;
- idempotency;
- human confirmation rules;
- target-system rollback/escalation;
- independently reviewed incident plans.

---

# 3. Target service objectives

Targets below are starting proposals for future contractual design, not current commitments.

## Core data-plane availability

```text
pilot target:           ≥99.9%
mature production:      ≥99.95%
critical mature paths:  evaluate ≥99.99% only where architecture/dependencies justify it
```

The metric must separate:

```text
CareOS process availability
source-system availability
identity-provider availability
network availability
model-provider availability
```

A composite "green" metric that hides source outages is unacceptable.

## Latency targets

For a provider-local environment under normal load:

```text
patient-context shell / cached metadata     p95 < 1 s
core source-linked context                  p95 < 2 s when local sources allow
source inspection                           p95 < 2 s excluding upstream viewer
agent source-grounded question              target p95 < 5 s
longer document/voice drafts                progressive feedback; no frozen UI
```

Never sacrifice correctness/source-state reporting to hit latency.

## Incident response target

Future staffed service model:

```text
SEV-0 patient-safety / broad outage     acknowledgement ≤ 5 min
SEV-1 major production degradation      acknowledgement ≤ 15 min
SEV-2 workflow impairment               acknowledgement ≤ 4 h
SEV-3 low-risk defect                   next business-day triage
```

Clinical safety owner and hospital incident owner must have direct escalation paths for Sev-0/1.

---

# 4. Failure modes and required behavior

## CareOS application unavailable

Required:

- KIS/source workflows remain accessible;
- no partial write left ambiguous;
- status page/IT health endpoint identifies outage;
- last-known local display, if enabled, is unmistakably stale/read-only;
- recovery does not require reconstructing authoritative truth from CareOS storage.

## One source unavailable

Required:

- other admitted facts may remain visible;
- unavailable source named;
- `complete=false`;
- `may_assert_absence=false`;
- dependent agent claims suppressed;
- no reassuring empty state.

## Identity unavailable

Required:

- no patient-context guessing;
- no fuzzy fallback matching;
- launch blocks or returns user to source workflow;
- cached identity mapping only under explicitly approved rules.

## Model provider unavailable

Required:

- source-linked context still works;
- deterministic features remain;
- draft/agent features show unavailable state;
- no silent swap to an unapproved model/provider.

## Audit destination unavailable

For consequential workflows:

- actions requiring durable audit fail closed or enter a specifically approved bounded buffer;
- no unlogged write/send path.

## KIS/vendor upgrade

- compare last-known-good capability manifest;
- conformance replay;
- canary/shadow;
- promote only after explicit evidence;
- rollback path tested.

---

# 5. Release strategy

## No fleet-wide surprise updates

Release rings:

```text
0. internal synthetic
1. integration sandbox
2. hospital shadow/canary
3. one workflow / one ward
4. hospital/site
5. hospital group / wider fleet
```

Promotion requires evidence from the previous ring.

## Version everything consequential

- container/build digest;
- adapter;
- hospital capability profile;
- terminology/mapping;
- policy;
- prompt;
- model/provider;
- agent definition/tool registry;
- workflow pack;
- schema.

## Never silently change

- model;
- clinical prompt behavior;
- write/send capability;
- mapping semantics;
- patient identity strategy;
- source prioritisation;
- alert threshold with clinical consequence.

---

# 6. Security patching target

Future production process:

- continuously monitor dependencies/images;
- emergency security lane for critical exploitable vulnerabilities;
- validate patch against conformance/safety suite;
- canary before fleet promotion unless active exploitation makes emergency process necessary;
- publish customer-facing security advisory where appropriate;
- maintain rollback artifact.

"Patch fast" never means "skip the clinical regression suite".

---

# 7. Disaster recovery

CareOS should minimise authoritative state so recovery is simpler.

## Clinical truth

Systems of record remain authoritative.

Provider-local context/cache is rebuildable from sources.

## Configuration

- signed/versioned deployment configuration;
- encrypted backups;
- tested restore.

## Audit

Audit is not disposable cache.

- durable provider-approved storage;
- tamper-evident controls;
- replication/backup appropriate to deployment;
- regular restore verification.

## Target exercises

At least annually in mature production:

- regional/cloud/cluster failure;
- IdP failure;
- source outage;
- compromised credential;
- bad release rollback;
- lost audit sink;
- model-provider outage;
- KIS upgrade incompatibility.

---

# 8. Hospital relationship cadence

## Implementation phase

```text
shared implementation channel
named hospital IT owner
named clinical champion
named CareOS/partner integration owner
weekly workflow review
weekly safety/metrics review
```

For first go-live days, increase cadence to a live war-room-style channel without making clinicians responsible for debugging infrastructure.

## Mature production

### Monthly operations review

- availability/degradation;
- source reliability;
- incidents;
- support tickets;
- adapter/version changes;
- upcoming hospital upgrades;
- security actions.

### Quarterly value/clinical review

- Time Returned to Care;
- adoption;
- correction/rejection;
- safety stops;
- verification behavior;
- workflow friction;
- next expansion decision.

### Annual resilience review

- disaster recovery;
- penetration/security review;
- access/role governance;
- business continuity;
- data-flow/subprocessor review;
- rollback exercise.

---

# 9. Support experience

A nurse or doctor should not need to know whether an issue is "FHIR", "Kubernetes" or "LLM".

User-facing support should capture automatically, where privacy permits:

```text
hospital/site
user role
patient-context pseudonymous correlation ID
CareOS version
adapter/source health
workflow/module
exact visible error state
trace ID
```

Never require a clinician to paste patient data into a support ticket.

## Help layers

1. inline self-explanation;
2. product-support agent with no clinical authority;
3. human support;
4. clinical/integration/security escalation as appropriate.

---

# 10. Status transparency

Hospital IT should always be able to answer:

```text
is CareOS up?
which sources are up?
is identity working?
which feature is degraded?
which users/workflows are affected?
what release is running?
what changed?
what is the rollback version?
```

Clinicians should see only clinically useful degradation information, not infrastructure noise.

Example:

> **Microbiology source unavailable since 10:42. Other patient information is current. Pending/negative microbiology conclusions are disabled until the source recovers.**

This is safer than a generic red "system error" banner.

---

# 11. Dependency budget

Critical workflow value should not require every optional dependency to be healthy.

Order of independence:

```text
core source-linked context
  should not require external model

patient/source identity
  should not depend on model

source-state/freshness
  should not depend on model

authorization
  should not depend on model

audit policy
  should not depend on model
```

The model is an enhancement layer, not the system's nervous system.

---

# 12. Long-term customer promise

The relationship should feel like:

> **"You can depend on the workflow, understand every important change, keep control of your data and systems, and leave without being trapped."**

That means:

- exportable configuration/evidence;
- open interfaces;
- no proprietary patient identity;
- no hidden source transformations;
- explicit compatibility records;
- documented migration/offboarding path;
- hospital-owned kill authority;
- stable old-version support windows defined contractually.

Critical infrastructure earns trust partly by making exit possible.
