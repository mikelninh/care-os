# Hospital Implementation Playbook — Zero-Drama Rollout

Baseline: **18 August 2026**

> Goal: introduce a clinical context/AI workflow with the least possible disruption, prove value before increasing authority, and make rollback easier than escalation.

This playbook is product-agnostic. It can support CareOS research, a Recare deployment or another hospital workflow.

## The promise we can responsibly make

We cannot guarantee that no component will ever fail.

We can design the migration so failure is far less dangerous:

1. **no big-bang cutover**;
2. **legacy stays available** until the new capability earns dependency;
3. **clinical uncertainty fails closed** rather than becoming false absence;
4. **read does not imply write**;
5. **every stage is reversible**;
6. **vendor/system upgrades are preflighted before rollout**;
7. **one legacy capability retires at a time**.

North star:

> **Time Returned to Care — gated by safety and verification.**

---

# Phase 0 — Workflow archaeology

Before automation, observe the real work.

For representative cases, capture where feasible:

- elapsed task time;
- systems opened;
- searches/context switches;
- calls/messages;
- copy/paste and duplicate entry;
- corrections;
- pending work found late;
- handoffs;
- paper/fax/spreadsheet workarounds;
- cognitive load.

Outputs:

```text
workflow map
baseline metrics
pain-ranked opportunity
explicit non-goals
```

> **Automate the painful step, not the imagined workflow.**

---

# Phase 1 — Describe the hospital once

The discovery output should become a **machine-readable Hospital Capability Manifest**, not disappear into consulting notes.

Capture:

```text
hospital/site
KIS / LIS / RIS-PACS / document systems
vendor / product / version
FHIR / ISiK / HL7 / vendor APIs / feeds
authentication mode
patient + encounter identity
cross-source identity strategy
source IDs / versions / effective time / lifecycle support
read / write capability
SSO + patient-context launch
audit destination
network constraints
security / privacy / clinical / rollback owners
```

CareOS implementation: `app/hospital_install.py` + `deploy/hospital.example.json`.

The manifest is **non-secret**. Endpoints, tokens, certificates and passwords remain in hospital-controlled secret infrastructure and are referenced by name only.

## Preflight

Run deterministic preflight before engineers build custom integration:

```bash
python scripts/careos.py doctor hospital.json --env-file hospital.env
python scripts/careos.py preflight hospital.json
```

The output classifies:

```text
PASS  = known requirement satisfied
WARN  = usable for planning but needs conformance/review
BLOCK = missing safe runtime path, identity or accountable control
```

Do not hide a blocker inside an implementation estimate.

---

# Phase 2 — Discover what the source actually exposes

Where a permitted FHIR endpoint exists, inspect its `CapabilityStatement` rather than relying only on meetings/spreadsheets:

```bash
python scripts/careos.py discover-fhir hospital.json --env-file hospital.env
```

Discovery can report:

- advertised FHIR version/software;
- resource types;
- interactions;
- search parameters;
- resource versioning;
- differences between declared and advertised capabilities.

Discovery **suggests**. It does not silently rewrite the hospital manifest or decide governance facts.

For non-FHIR paths, equivalent safe discovery should eventually exist, but only after a real adapter implementation and conformance contract exist.

---

# Phase 3 — Select the least bespoke adapter

Preferred migration path:

```text
ISiK / FHIR
      ↓
FHIR R4
      ↓
HL7 v2
      ↓
stable vendor API
      ↓
document/source feed
      ↓
UI/computer-use bridge as explicit fallback
```

But **a standard named by the hospital does not mean the platform implements it**.

Current CareOS truth:

| Path | Status |
|---|---|
| FHIR R4 read | implemented research runtime |
| ISiK/FHIR read | FHIR runtime + validation path |
| HL7 v2 | contract-only |
| vendor API | contract-only |
| source feed | contract-only |
| UI bridge | contract-only |
| live write | blocked |

If the strongest available hospital interface is contract-only, integration stops cleanly and creates a bounded adapter task.

---

# Phase 4 — Conformance before connection

Connectivity is not interoperability.

Every site/adapter should replay the same behavioral checks:

### Identity

- patient identity survives the boundary;
- encounter identity survives where required;
- cross-source mapping is governed;
- patient A cannot become patient B.

### Provenance

- upstream resource/document IDs survive;
- versions survive where exposed;
- clinical effective time remains separate from ingestion/recorded time.

### Lifecycle

- preliminary;
- final;
- corrected;
- cancelled;
- pending;
- stale;
- unavailable.

### Transport

- paging completes or fails closed;
- partial reads are visible;
- outages are visible;
- retry/idempotency is explicit.

### Security

- authentication failure closes access;
- credentials do not appear in logs/config;
- network destinations are bounded;
- read does not become write.

A conformance failure becomes a regression fixture before broader rollout.

---

# Phase 5 — Read-only + shadow first

Default authority ladder:

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

Initial question:

> **Can we surface the right patient context with the right source/state semantics without becoming a new dependency?**

Shadow mode runs beside the normal workflow and compares what the new path would show/propose against what actually happened.

Exit criteria should include:

- correct patient/encounter binding;
- provenance for consequential facts;
- pending/unavailable/stale states preserved;
- source outages visible;
- acceptable latency;
- no unnecessary second patient search;
- audit functioning;
- rollback rehearsed.

---

# Phase 6 — One workflow, one ward

Avoid hospital-wide AI transformation launches.

Choose:

```text
one workflow
one ward/team
one clinical champion
one implementation owner
one engineering owner
one IT/integration owner
one measurable outcome
```

Pilot charter:

```text
problem + baseline
sources
excluded decisions
human approval boundary
success metrics
safety-stop metrics
rollback owner
review date
```

---

# Phase 7 — Copilot mode

The system may now:

- extract;
- organize;
- surface source-linked context;
- draft;
- propose administrative next actions.

Humans verify, correct and approve.

Capture:

- accepted unchanged;
- edited;
- rejected;
- source opened;
- pending item missed;
- contradiction reviewed;
- completion time;
- abandonment reason.

Corrections become evaluation/regression evidence, not invisible cleanup.

---

# Phase 8 — Controlled legacy bridge

A UI/computer-use bridge can be valuable when no practical typed write path exists, but it is a separate risk surface.

Require compatibility evidence for:

- KIS UI/version;
- expected screen state;
- session/concurrency behavior;
- field mapping;
- confirmation;
- retry/idempotency;
- safe halt on UI changes;
- read-after-write verification;
- audit.

Never describe computer-use as equivalent to a typed API.

---

# Phase 9 — Bounded execution

Only consider consequential write/send actions after read/draft value is proven and governance permits them.

Every action needs an explicit authority contract:

```text
workflow/agent identity + version
patient/encounter scope
allowed tool + operation
data categories
budgets
human confirmation
idempotency/replay
allowed egress
audit
kill/revocation
```

Rules:

- no self-escalation;
- no autonomous break-glass;
- write and external send are separate;
- failed/partial execution is visible;
- read-after-write verification where applicable.

Current CareOS release intentionally ships no live transactional adapter.

---

# Phase 10 — Measure before scale

Measure benefit and risk together.

### Benefit

- task time;
- searches/context switches;
- calls/messages;
- manual entries;
- effort;
- adoption/repeat use.

### Reliability / safety

- wrong-patient events;
- source outages;
- unsupported facts;
- stale/pending confusion;
- missed pending work;
- corrections;
- contradictions;
- system availability;
- support incidents.

### Verification

- source-opening rate;
- acceptance without source check;
- draft-vs-source confusion;
- correction after source review.

```text
PASS → expand carefully
HOLD → fix / gather evidence
FAIL → rollback or redesign
```

A speed win never cancels a safety-stop event.

---

# Phase 11 — Treat upgrades like migrations

Before a KIS/LIS/interface upgrade, compare last-known-good and proposed capability manifests:

```bash
python scripts/careos.py upgrade-check current.json proposed.json
```

CareOS upgrade preflight blocks changes such as:

- source removal;
- vendor/product replacement under the same identity;
- interface loss;
- patient-identity loss;
- provenance/effective-time/lifecycle loss;
- newly introduced write capability;
- a proposed configuration that no longer passes preflight.

A normal vendor/version change still requires shadow revalidation.

This is how a vendor upgrade becomes a compatibility test **before** it becomes a clinical surprise.

---

# Phase 12 — Prove repeatability

Do not call the platform scalable after one successful site.

The real infrastructure test is:

```text
Hospital A / Vendor A
        ↓
reusable adapter + configuration
        ↓
no core fork

Hospital B / different vendor/version
        ↓
reusable adapter + configuration
        ↓
no core fork
```

Track:

- human integration hours/site;
- time from manifest to first validated data;
- time to shadow mode;
- custom code/site;
- adapter/test reuse rate;
- configuration-only deployment rate;
- pre-production conformance failures;
- upgrade regressions caught before rollout;
- support burden.

The goal is **marginal hospital integration cost approaching configuration + conformance, not custom software engineering**.

---

# Implementation team

| Role | Responsibility |
|---|---|
| clinical sponsor | outcome, scope, escalation |
| clinician champion | workflow truth + feedback |
| implementation owner | rollout coordination |
| integration engineer | source interfaces/mapping |
| AI/product engineer | agent/model/workflow behavior |
| hospital IT | infrastructure/operations |
| security / DPO | controls/privacy/risk |
| product | scope/adoption/metrics |
| support | incident/friction feedback |

One person may cover multiple roles; the responsibilities still need named owners.

---

# Desired implementation experience

For hospital IT:

```text
one non-secret capability manifest
one preflight report
one adapter/conformance plan
one security/network data-flow package
one local deployment path
one upgrade check
one rollback route
```

For clinicians:

```text
no second patient search if avoidable
minimal new UI
source visible when needed
uncertainty visible
fast correction
human authority obvious
no hidden writes
```

---

## CareOS assets

- [Hospital Self-Install Platform](HOSPITAL_SELF_INSTALL_PLATFORM.md)
- [Connector SDK](CONNECTOR_SDK.md)
- [Current Status & Gaps](CURRENT_STATUS_AND_GAPS.md)
- [Reference Architecture V2](ARCHITECTURE_V2.md)
- [Trust & Data Flow](TRUST_AND_DATA_FLOW.md)
- [Hospital Assurance Pack](HOSPITAL_ASSURANCE_PACK.md)
- [Agent Security Model](AGENT_SECURITY_MODEL.md)
- [Recare Integration Accelerator](RECARE_INTEGRATION_ACCELERATOR.md)
- [Endgame](ENDGAME.md)

> **Reduce uncertainty in layers, earn authority from evidence, and never make the hospital absorb complexity merely because the software can.**
