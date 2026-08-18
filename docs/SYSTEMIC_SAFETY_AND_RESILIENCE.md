# CareOS Systemic Safety & Resilience

Baseline: **18 August 2026**

> If CareOS succeeds, CareOS itself becomes a risk surface. Safety therefore includes protecting hospitals **from CareOS**, not only protecting CareOS from attackers.

This document defines the design direction for keeping blast radius bounded as deployments grow.

---

# 1. Systemic-risk principle

A platform used by many hospitals must never make one of these easy:

- one bad release breaks every hospital;
- one compromised central control plane exposes routine clinical data;
- one model/provider outage blocks core clinical truth;
- one adapter regression silently changes clinical semantics everywhere;
- one operator can grant global write authority;
- one patient-identity bug propagates across sites;
- one configuration push bypasses local governance;
- one security incident forces all hospitals into the same failure mode.

Target:

> **Shared learning; bounded failure.**

---

# 2. Blast-radius architecture

```text
shared control plane
  signed releases / policy / schemas / adapter metadata
  NO routine longitudinal PHI required
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
 hospital A      hospital B   hospital C
 local data      local data   local data
 plane           plane        plane
 local kill      local kill   local kill
 local audit     local audit  local audit
 local secrets   local secrets local secrets
```

Rules:

1. provider data plane remains independently operable for bounded periods;
2. shared control-plane outage must not erase local source truth or legacy fallback;
3. hospitals retain local deployment/rollback authority;
4. credentials are provider/site scoped;
5. agent delegations are site + patient + task scoped;
6. releases are pinned, not silently floating;
7. adapter/package versions are explicit;
8. data-plane network egress is allowlisted;
9. no central super-admin can silently cross every provider boundary by default;
10. no automatic global promotion of a release solely because CI is green.

---

# 3. Release safety

Target release sequence:

```text
source change
→ unit/contract tests
→ synthetic adversarial suite
→ integration/conformance
→ signed/pinned artifact
→ internal canary
→ opt-in pilot site(s)
→ shadow/read-only observation
→ staged cohorts
→ general release
```

Promotion evidence should include:

- test suite version;
- adapter compatibility evidence;
- migrations/schema changes;
- security scan/SBOM/provenance;
- expected data-flow change;
- clinical semantics change assessment;
- rollback plan;
- target cohort;
- stop thresholds;
- named owner.

Never roll a semantic clinical-state change to every site simultaneously.

---

# 4. Kill hierarchy

Kill switches should be granular:

```text
model/provider kill
agent/version kill
tool/capability kill
adapter/source kill
workflow kill
hospital/site kill
release kill
```

A hospital should not need to disable read-only source context merely because one model worker is unsafe.

Likewise, disabling an adapter should not automatically erase other independent sources.

---

# 5. Audit is a safety system

Audit must answer:

```text
who / what actor
which organisation
which patient/encounter
which operation
which source/tool
what authorization decision
what version (app/agent/model/adapter/policy)
what evidence/context identifiers
what result/status
when
where/origin
whether break-glass
whether human confirmation
```

Audit goals:

- reconstruct consequential actions;
- detect anomalous access;
- support incident response;
- show who/what changed an artifact;
- distinguish human vs agent activity;
- support patient-access transparency where governing infrastructure permits;
- support safety evaluation.

Audit anti-goals:

- indiscriminate clinical-content duplication;
- centralising PHI merely for observability;
- making the audit service itself a silent single point of clinical failure.

Production target: tamper-evident/independently protected audit with retention/access appropriate to the deployment.

---

# 6. Mass-incident classes

## A. Bad application release

Response:

- stop cohort rollout;
- pin last known good;
- rollback;
- compare affected artifacts/state;
- determine whether any derived data needs invalidation/recalculation;
- publish advisory;
- regression test.

## B. Adapter semantic regression

Example: vendor changes status mapping and `preliminary` becomes `final`.

Response:

- disable adapter version;
- source marked unavailable/degraded rather than normal empty;
- identify affected fact/artifact lineage through graph;
- invalidate/reopen downstream derived artifacts;
- conformance fixture from incident.

## C. Patient identity incident

Response:

- immediate affected resolver/connector kill;
- cross-patient data never silently “fixed” by model;
- identify/audit affected sessions/artifacts;
- mandatory review before reopening;
- incident becomes permanent identity regression fixture.

## D. Model/provider incident

Response:

- model/worker kill only;
- source-linked clinician context remains;
- drafts disabled/clearly unavailable;
- no fallback to a less governed provider automatically.

## E. Central control-plane outage

Response:

- pinned local release keeps operating within approved local TTL/policy;
- no new central configuration needed for normal bounded operation;
- local source/identity/audit continues;
- local IT can kill/rollback independently.

## F. Cybersecurity compromise

Response:

- revoke scoped credentials/delegations;
- isolate site/component;
- preserve protected audit;
- fail closed on authority;
- do not destroy clinical access to legacy source systems merely to protect CareOS.

---

# 7. Offline / disaster principle

CareOS must never be the only path to core clinical truth during its early/medium adoption.

Long-term critical use requires:

- documented downtime procedure;
- local emergency/minimum information strategy where lawful/appropriate;
- ability to identify freshness of cached information;
- paper/legacy/emergency fallback where required by provider continuity planning;
- recovery reconciliation;
- periodic outage exercises.

“Offline mode” must not mean “show cached UI that looks current.”

---

# 8. Dependency hierarchy

Prefer failure in this order:

```text
optional generative features disappear first
→ convenience coordination features degrade
→ derived context becomes visibly stale/unavailable
→ source systems / legacy clinical workflow remain available
```

Never invert this hierarchy so an AI/provider/control-plane outage makes authoritative patient data harder to reach.

---

# 9. Human factors as safety engineering

Worst cases are not only backend bugs.

Design against:

- automation bias;
- alert fatigue;
- patient-context confusion;
- source-vs-draft confusion;
- confirmation fatigue;
- hidden stale state;
- over-dense screens;
- color-only status;
- tiny touch targets;
- accidental action on shared terminals;
- urgent users skipping source verification because it is too slow.

Safety UX targets:

- patient identity always obvious;
- uncertainty impossible to mistake for final state;
- consequential source inspection ≤1 interaction when feasible;
- correction fast;
- destructive/consequential actions review exact payload/target;
- agent activity visually distinct but not noisy;
- failures explain what still works.

---

# 10. Organisational safety

Technical controls fail when responsibility is vague.

Every production deployment needs named owners for:

- clinical outcome;
- patient safety;
- hospital integration;
- privacy/DPO;
- cybersecurity;
- operational support/on-call;
- audit/SIEM;
- release promotion;
- rollback;
- incident commander;
- vendor escalation.

No production launch with “shared responsibility” that means nobody owns the stop button.

---

# 11. Service-level design

CareOS may eventually justify critical-service SLAs, but do not promise numbers before capability exists.

A mature target service should define at least:

- availability SLO by capability, not only one app uptime number;
- source freshness SLO;
- identity/auth latency/availability;
- audit durability;
- data recovery RPO/RTO where state exists;
- incident acknowledgement/update targets;
- security vulnerability response;
- supported release window;
- adapter/vendor compatibility support window;
- emergency rollback target;
- planned maintenance communication.

A “99.99%” marketing number is meaningless if source data is stale or patient identity is unsafe.

---

# 12. Independence and exit

Critical infrastructure must support exit.

Hospitals should be able to export/retain:

- non-secret site manifest;
- mapping configuration they own;
- compatibility/conformance evidence;
- audit records according to governance;
- derived clinical artifacts according to agreed ownership/format;
- open context/API contracts.

The integration layer must not become a new lock-in mechanism while claiming to solve old lock-in.

---

# 13. Systemic-safety proof programme

Before broad scale:

1. synthetic kill-switch drill;
2. model outage drill;
3. source outage/partial-read drill;
4. identity resolver incident drill;
5. adapter version regression drill;
6. rollback drill;
7. control-plane disconnect drill;
8. audit tamper/replay test;
9. shared-terminal session isolation test;
10. multi-site staged-release simulation;
11. independent penetration test;
12. hospital disaster/downtime exercise.

Each failure produces a regression fixture.

---

# 14. One rule to remember

> **If CareOS disappears, people must still be able to care for patients. If CareOS lies, the system must make the lie hard to propagate. If CareOS is compromised, the blast radius must be bounded.**
