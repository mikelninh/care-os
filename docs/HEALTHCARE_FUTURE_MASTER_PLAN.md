# CareOS Healthcare Future Master Plan

Baseline: **18 August 2026**

> **Mission:** return time, clarity and agency to care while making the underlying information flow more trustworthy, interoperable, resilient and humane.

This document is intentionally broader than one product. It describes the future healthcare operating model CareOS should help make possible, the order in which to build toward it, the measurable outcomes, the hard safety boundaries and the evidence required before expanding authority.

It is a **north-star + execution contract**, not a claim that the future state already exists.

---

# 1. The future-state test

A healthcare system is moving in the right direction when all of the following become true at the same time:

## For clinicians

- open the patient once;
- relevant current context is already assembled;
- pending, stale, unavailable, contradictory and corrected information remain visibly distinct;
- important changes since the last review are obvious;
- the original source is one click/tap away;
- repetitive documentation is prepared, not repeatedly retyped;
- routine coordination happens digitally and structurally;
- AI can prepare and explain, but cannot silently invent authority;
- the system works on the devices and network conditions clinicians actually have;
- when CareOS fails, the legacy clinical workflow remains usable.

## For patients

- understand what happened, what changed, what is pending and what happens next;
- can access the information they are legally entitled to access;
- can see who accessed/shared data where the governing infrastructure supports that;
- can correct or flag suspected errors through a governed workflow;
- can delegate access where permitted;
- can carry a safe portable summary across institutions/countries;
- plain-language explanation and translation never overwrite source truth;
- the system reduces uncertainty rather than manufacturing reassurance.

## For hospital IT

- install a local/provider-controlled data plane;
- describe systems once using a non-secret capability manifest;
- reuse adapters and conformance tests across sites;
- discover standard capabilities automatically where safe;
- know every network destination, credential boundary and data flow;
- upgrades are checked before rollout;
- canary/shadow validation precedes dependency;
- rollback is rehearsed and boring;
- no routine PHI is required in a shared control plane;
- a vendor change does not require rebuilding every clinical application.

## For hospitals and practices

- exchange data through governed interoperable rails rather than fax/copy-paste where digital exchange is possible;
- send the minimum necessary information for the purpose;
- receiving systems preserve provenance, state and trust;
- coordination status is machine-readable rather than trapped in phone calls;
- referrals/transfers/discharge become longitudinal workflows rather than document hand-offs.

## For the health system

- standards define seams, not one national monolith;
- vendors can compete without trapping providers;
- citizens retain meaningful control and transparency;
- digital trust can extend across borders;
- innovations can plug into a stable clinical context contract;
- health-system learning uses governed data while clinical operations remain protected;
- every deployment makes the next deployment cheaper and safer.

---

# 2. Product north stars

CareOS must optimise **benefit and risk together**.

## Primary benefit metric

> **Time Returned to Care**

Measured as a paired before/after change in a defined workflow, not a survey impression.

Initial product hypotheses (targets, not current claims):

| Role/workflow | First useful target | Mature ambition | Must not worsen |
|---|---:|---:|---|
| physician review / documentation | 20–30 min/shift | 45–60 min/shift | missed pending work, unsupported facts, source verification |
| nursing handover / task reconciliation | 10–15 min/shift | 20–30 min/shift | omissions, duplicate tasks, alert burden |
| discharge / transfer coordination | 15–20 min/case | 30–60 min/case | inappropriate sharing, missing-field loops, placement correctness |
| case management / social service | 15–20 min/case | 30–45 min/case | status accuracy, handoff ownership |
| hospital IT routine supported integration change | days → hours | <1 workday | security review, conformance, rollback evidence |
| patient/family understanding | qualitative baseline | high teach-back success | false certainty, hidden pending state |

A speed gain is invalid if a safety-stop metric triggers.

## Core safety metrics

- wrong-patient events;
- unsupported consequential facts;
- pending-as-negative errors;
- stale-as-current errors;
- unavailable-as-absent errors;
- contradiction loss;
- draft/source-truth confusion;
- unauthorised agent/tool action;
- inappropriate data disclosure;
- incomplete audit event;
- failed rollback/recovery;
- verification decay.

## Experience metrics

- time to orient to a patient;
- clicks/taps/context switches;
- searches across systems;
- manual copy/paste;
- phone calls/faxes caused by information discovery rather than human judgment;
- task abandonment;
- correction burden;
- support tickets;
- perceived cognitive load;
- repeat use / voluntary adoption;
- patient comprehension.

---

# 3. Stakeholder operating model

The same trustworthy context should appear differently for different people.

## 3.1 Physician

### Before

```text
open KIS
→ search last note
→ open lab
→ open microbiology
→ check medication
→ find old letter
→ reconstruct timeline
→ call for missing context
→ write summary again
```

### Target

```text
open patient
→ changed since last review
→ pending / contradictory / stale
→ relevant source-linked current state
→ human plan
→ prepared note/handover/discharge draft
→ verify source where consequential
→ sign/decide
```

Agent jobs:

- changed-since-last-review synthesis;
- source-linked timeline;
- progress-note skeleton;
- discharge draft preparation;
- missing-field check;
- question answering over admitted source context;
- never independently diagnose/prescribe under the current CareOS boundary.

## 3.2 Nurse

Target surface:

- what changed this shift;
- what must happen next;
- overdue/pending tasks;
- care-relevant exceptions;
- isolation/infection-control state;
- medication/order change visibility;
- handover draft from governed source data;
- fast correction without fighting the system.

Agent jobs:

- structure handover from approved documentation;
- group changes;
- surface missing required fields;
- prepare tasks from approved plans;
- no hidden plan modification.

## 3.3 Emergency clinician

Target:

- minimal trustworthy orientation in seconds;
- allergies / major diagnoses / critical medication / recent encounters;
- provenance and recency visible;
- imported/cross-border summary clearly labelled;
- break-glass governed and audited where applicable;
- no slow dependency on a non-critical AI service.

## 3.4 Pharmacist / medication safety

Target:

- current medication state with source/version/time;
- medication changes and discontinuations;
- allergies/intolerances;
- renal/hepatic context when available and governed;
- reconciliation conflicts;
- discharge medication comparison;
- agent can prepare discrepancy review, not silently resolve it.

## 3.5 Radiology / diagnostics

Target:

- question/indication and relevant prior context;
- prior related studies surfaced without hunting;
- report lifecycle (preliminary/final/corrected) preserved;
- critical-result acknowledgement workflow explicit;
- image data stays on appropriate imaging infrastructure; CareOS links/contextualises rather than copies everything by default.

## 3.6 Laboratory / microbiology

Target:

- specimen/order/result relationships intact;
- preliminary/final/corrected/cancelled semantics preserved;
- pending work remains pending;
- late result automatically re-opens affected downstream summaries/drafts for review;
- no result loss through document flattening.

## 3.7 Discharge / case management / social service

Target:

- aftercare need visible early;
- required minimum data assembled once;
- missing fields explicit;
- approved digital routing;
- replies/status structured;
- no repeated copy-paste into parallel systems;
- patient/family sees a comprehensible status and next step where appropriate.

## 3.8 Outpatient physician / practice

Target:

- referral arrives structured plus source document where needed;
- recent hospital events and medication changes are understandable;
- requested follow-up is explicit;
- results can return through interoperable rails;
- no manual re-entry merely because institution changed.

## 3.9 Therapist / allied health professional

Target:

- purpose-limited, role-appropriate context;
- current restrictions/goals/orders where applicable;
- tasks/appointments/handovers;
- no default exposure to the entire record.

## 3.10 Patient / family / proxy

Target interface:

```text
Today
What happened
What changed
What is still pending
What happens next + owner
Medication changes
Appointments / follow-up
Documents
Who accessed/shared data (where infrastructure exposes it)
Questions to ask
Report a possible error
Share / delegate access
```

Agent jobs:

- explain jargon;
- translate presentation;
- locate source material;
- prepare questions;
- explain what “pending”, “preliminary”, “corrected”, “unavailable” mean;
- never claim more certainty than the record supports.

## 3.11 Hospital IT / integration engineer

Target workflow:

```text
careos init
→ describe/discover systems
→ adapter plan
→ identity strategy
→ conformance
→ generated network/data-flow pack
→ deploy sandbox
→ shadow/canary
→ upgrade-check
→ promote/rollback
```

## 3.12 DPO / CISO / clinical safety / governance

Target:

- generated, reviewable non-secret system/data-flow manifest;
- explicit responsibilities;
- purpose/data minimisation;
- access policy and audit semantics;
- agent capability manifest;
- model/provider boundaries;
- threat model;
- rollback/incident owners;
- evidence linked to each gate;
- no “trust us” AI black box.

## 3.13 Leadership / CFO / public payer

Target dashboard:

- time returned to care;
- reduction in duplicate work;
- integration lead time;
- adoption;
- safety metrics;
- avoided support/manual coordination burden;
- reliability/SLA;
- no ROI claim that excludes implementation/support/risk costs.

---

# 4. Devices and interaction surfaces

The future system is **contextual**, not “desktop vs mobile.”

## Managed workstation / Windows / Citrix

Primary surface for:

- physician review;
- documentation;
- complex source inspection;
- pharmacy/diagnostic review;
- administration.

Requirements:

- keyboard-first;
- dense but calm information hierarchy;
- no horizontal scrolling at normal managed resolutions;
- resilient under Citrix/VDI latency;
- no GPU assumption;
- no installation requirement on each workstation if browser deployment works;
- same-patient launch from KIS where possible.

## iPad / clinical tablet

Primary surface for:

- rounds;
- bedside review;
- nursing tasks/handover;
- patient explanation;
- image/document preview where appropriate.

Requirements:

- touch targets;
- one-hand/standing use;
- quick re-auth;
- role/context switching safely;
- no hidden hover interactions;
- camera/microphone features opt-in and governed;
- local cache minimised and protected.

## Phone

Use for:

- lightweight task/status/communication;
- patient/family access;
- on-call notification where justified;
- not the default interface for complex clinical decisions.

## Shared terminal

Requirements:

- aggressive session/context isolation;
- clear patient banner;
- quick logout/lock;
- no cross-user local residue;
- re-auth for consequential actions.

## Voice

Useful when hands/attention are constrained, but voice input is **untrusted source material until reviewed**.

- ambient/dictation draft;
- structured note preparation;
- commands require explicit confirmation for consequential operations;
- audio retention policy explicit;
- no accidental cross-patient capture.

---

# 5. Wi-Fi, degraded networks and offline behavior

Healthcare cannot assume perfect connectivity.

Define four operating modes:

## NORMAL

All required sources current and reachable.

## DEGRADED

One or more non-critical dependencies impaired.

- show last-known state only with freshness label;
- dependent absence claims disabled;
- optional agent/model features may disappear;
- core source inspection stays available where technically possible.

## OFFLINE / SOURCE UNAVAILABLE

- never fabricate empty/negative state;
- display exactly which source is unavailable;
- preserve only explicitly allowed local emergency/minimal cache;
- legacy system remains operational fallback;
- queue non-consequential drafts/actions only when idempotency and revalidation are designed;
- do not queue hidden clinical writes.

## RECOVERY

- re-auth/re-establish source state;
- revalidate patient context;
- reconcile versions/events missed during outage;
- surface conflicts created during outage;
- delayed actions require current-state validation before execution;
- audit the recovery transition.

Target availability philosophy:

> **Core clinical work must degrade gracefully. AI convenience may disappear before source truth, identity, audit or legacy care pathways do.**

---

# 6. The clinical context graph

Yes: a graph is valuable — but it must be a **derived, source-linked view**, not a magical model-created truth database.

## Why graph structure matters

Healthcare is relational and temporal:

```text
patient
  ├─ encounter
  │   ├─ diagnosis
  │   ├─ order
  │   │   └─ specimen
  │   │       └─ result
  │   ├─ medication administration
  │   └─ document
  ├─ medication
  ├─ allergy
  ├─ clinician/team
  └─ follow-up task
```

Useful graph questions:

- Which pending result belongs to this treatment episode?
- Which current statement was superseded by a correction?
- Which draft relied on a now-changed source fact?
- Which clinician/user/agent accessed or produced which artifact?
- What evidence supports this summary sentence?
- What downstream workflows should reopen after a result correction?

## Graph safety rules

- every consequential node/edge traces to authoritative source evidence or an explicit human/agent artifact;
- graph relations distinguish asserted vs derived vs proposed;
- patient boundaries are hard partitions unless a governed cross-record relation exists;
- no fuzzy cross-patient merge;
- lifecycle/version/time represented explicitly;
- deletion/restriction semantics propagated where required;
- graph is reconstructable from evidence + transformations;
- audit graph and clinical graph are related but access-controlled separately.

---

# 7. Agent architecture: make every user more capable, never less accountable

The most useful agents are **workflow agents**, not autonomous “AI doctors.”

## Agent classes

### Orientation agent

Answers: “What changed? What is pending? Where did this come from?”

### Documentation agent

Prepares source-linked notes, letters, handovers and forms.

### Coordination agent

Tracks referrals, discharge steps, missing information, replies and owners.

### Verification agent

Checks whether a draft is grounded, whether required fields/sources are missing, and whether lifecycle state was preserved.

### Patient explanation agent

Explains approved/source information in plain language and prepares questions.

### IT integration agent

Explains manifest/preflight failures, suggests documented fixes and generates non-secret configuration/review artifacts. It cannot grant itself network/secrets/production authority.

### Operations agent

Surfaces SLO/connector/upgrade regressions to humans; proposes rollback, does not autonomously override clinical governance.

## Universal agent contract

```text
agent identity + version
human/workflow delegator
patient/encounter/task scope
allowed tools/operations/data categories
network destinations
budgets/timeouts
source/evidence requirement
human confirmation rule
write/send separation
audit
revocation / kill switch
```

Principle:

> **Model may interpret and propose. Deterministic policy owns authority. Humans retain consequential clinical judgment.**

---

# 8. First day / first week in different hospitals

## Hospital A — modern FHIR/ISiK-capable tertiary hospital

### Before day 1

- manifest generated;
- CapabilityStatement discovery;
- identity/context-launch path agreed;
- conformance against deidentified/synthetic sandbox;
- network/security/data-flow pack approved;
- one workflow chosen;
- baseline measurements captured.

### Day 1

- read-only shadow mode for one ward;
- clinicians do normal work;
- CareOS records what it would surface/draft;
- no clinical dependency;
- implementation team observes friction.

### Days 2–5

- daily 15-minute implementation review;
- every mismatch becomes a fixture/regression test;
- 3–5 clinician champions compare current vs CareOS-assisted flow;
- source-verification behavior measured;
- UI adjusted only for recurring real friction.

### End of week 1

Decision:

```text
PASS → optional read-only copilot for bounded workflow
HOLD → fix/test
FAIL → remove/rollback
```

## Hospital B — mixed legacy KIS + HL7 integration engine + separate LIS

Week 1 goal is **not** “full CareOS.”

- build/use generic HL7 adapter only after conformance;
- start with one stable feed/domain;
- no UI automation unless standards/API route is impractical;
- preserve normal KIS workflow;
- prove source identity/lifecycle before clinician dependency.

## Hospital C — small hospital / constrained IT

Target:

- appliance/VM or simple managed deployment;
- one accountable implementation owner;
- minimal configuration;
- remote support without remote access to PHI by default;
- smaller initial workflow;
- no Kubernetes requirement merely because enterprise architecture likes Kubernetes.

## Practice / outpatient clinic

- browser-first;
- national/standard exchange rails where available;
- minimal local infrastructure;
- referral/follow-up first;
- patient summary and task closure instead of hospital-scale data aggregation.

---

# 9. The first irresistible use case

Do **not** begin by promising to fix all healthcare.

The ideal first clinical product is:

> **Five-second orientation + changed/pending/conflicting context + source-linked draft for one high-friction daily workflow.**

Why:

- happens every day;
- benefits clinicians immediately;
- read-first limits authority;
- measurable against current workflow;
- uses the foundational interoperability layer;
- creates trust before automation expands;
- generates exactly the data needed to improve the product.

For Infectiology, a candidate workflow is morning review / handover / discharge preparation around microbiology, anti-infective therapy, isolation, trends, pending work and documentation.

---

# 10. Before → after synthetic inspiration cases

These are illustrative hypotheses to test, not real outcome claims.

## Case A — morning physician review

### Before

```text
08:07 open KIS
08:09 yesterday's note
08:12 lab
08:15 microbiology
08:19 medication
08:23 old discharge letter
08:28 call ward/lab about pending result
08:34 reconstruct timeline
08:43 start progress note
```

### After target

```text
08:07 open patient from KIS context
08:07 changed / pending / conflict view
08:10 inspect two consequential sources
08:13 confirm plan
08:16 edit source-linked draft
08:20 done
```

Hypothesis: ~20+ minutes returned on this workflow with no verification decay.

## Case B — nursing handover

Before: free text + task list + medication change + verbal reconciliation.

After target: changes, unresolved work, pending results, isolation/context and human-confirmed handover in one view.

Hypothesis: 10–20 minutes saved per handover plus fewer clarification loops.

## Case C — discharge coordination

Before: search chart → copy → phone/fax → wait → call → rewrite status.

After target: minimum necessary context prepared → missing fields explicit → approved digital route → structured response/status → patient sees next step.

Hypothesis: 20–40 minutes/case in the slice we control; must be tested against real coordination workflows.

## Case D — corrected lab result after discharge draft

Before: corrected result may sit in another system and require a human to notice the old letter/draft is stale.

After target:

```text
source corrected
→ graph/version relation updates
→ affected derived context marked stale
→ draft reopens for review
→ clinician sees exactly why
```

Impact target: prevent stale derived information from silently surviving a source correction.

## Case E — patient after discharge

Before: dense letter, unclear pending result, uncertain medication change, calls ward/GP.

After target: “what happened / what changed / what is pending / who owns it / next steps” plus source documents and plain-language explanation.

Proof: teach-back, fewer information-only clarification calls, no false certainty.

---

# 11. How we prove actual impact

## Baseline first

For each chosen workflow capture:

- elapsed time;
- systems/windows opened;
- searches;
- clicks/taps where useful;
- copy/paste/manual re-entry;
- phone calls/messages/faxes;
- correction count;
- missing/pending item misses;
- source checks;
- cognitive effort;
- patient understanding where relevant.

## Paired evaluation

Same synthetic/deidentified tasks:

```text
current workflow
vs
CareOS-assisted workflow
```

Counterbalance order where feasible.

## Shadow evaluation

With governance, compare what CareOS would have surfaced/proposed against the normal workflow without creating dependency.

## Real limited rollout

One ward / one workflow / named owners / stop thresholds.

## Evidence ladder

```text
synthetic usability
→ deidentified integration
→ shadow live
→ read-only copilot
→ human-approved bounded action
→ second ward
→ second vendor
→ second hospital
→ multi-site evidence
```

No later-stage claim may be borrowed from an earlier stage.

---

# 12. Safety and worst-case design

Ask “how could this hurt someone?” before “how cool could this be?”

## Worst cases

- wrong patient context;
- old result presented as current;
- pending interpreted as negative;
- source outage interpreted as absence;
- model hallucination accepted as source fact;
- imported/translated data loses meaning;
- malicious document expands agent authority;
- hidden autonomous write;
- correction fails to invalidate downstream artifact;
- clinician stops verifying because UI feels authoritative;
- patient receives false reassurance or alarming misinterpretation;
- data sent to wrong institution/person;
- compromised credential/agent accesses excessive data;
- shared workstation leaks previous patient context;
- network outage leaves staff dependent on inaccessible system;
- vendor upgrade silently changes interface semantics;
- audit trail is incomplete or mutable;
- support/control plane becomes a PHI exfiltration path;
- mass outage/update impacts many hospitals simultaneously.

## Architectural responses

- deterministic patient/encounter binding;
- hard cross-patient rejection;
- provenance mandatory;
- source-state semantics mandatory;
- typed lifecycle/version graph;
- explicit confidence/review states;
- least privilege;
- read/write separated;
- no model-owned authority;
- confirmation bound to exact action;
- read-after-write verification;
- immutable/tamper-evident audit strategy;
- kill switch and credential revocation;
- provider-local data plane;
- deny-default egress;
- staged rollout + canary + rollback;
- legacy fallback;
- signed/pinned release artifacts;
- conformance before connection;
- upgrade compatibility testing;
- incident simulation;
- no single global service required for core bedside truth.

---

# 13. Long-term hospital relationship: critical software is a service, not a sale

If hospitals depend on it, the relationship must look like infrastructure operations.

## Service model target

### 24/7 operational coverage for critical production deployments

- severity model;
- on-call engineering;
- hospital incident channel;
- response/communication targets by severity;
- status communication;
- post-incident review;
- rollback/runbook ownership;
- vendor/interface escalation path.

Do not publish guaranteed SLA numbers until staffing/infrastructure can actually support them.

## Regular cadence

### Continuous

- non-PHI health telemetry where approved;
- connector/source SLOs;
- security alerts;
- release/advisory feed.

### Weekly during rollout

- adoption/friction/safety review;
- unresolved integration issues;
- regression fixtures from incidents.

### Monthly/quarterly after stabilisation

- Time Returned to Care;
- support burden;
- safety/verification metrics;
- product usage;
- interface/vendor changes;
- roadmap review;
- security/privacy updates;
- clinician/patient feedback.

### Before every meaningful upgrade

```text
compatibility check
→ conformance
→ change/risk summary
→ shadow/canary
→ promote or rollback
```

Long-term promise:

> **Every incident at one deployment should, where generalisable and legally shareable, become a regression test protecting the others.**

---

# 14. Patient access and agency

CareOS should complement national patient-access infrastructure rather than create an ungoverned duplicate record.

Design goals:

- patient-facing view built from authoritative/provider/national sources;
- access rights enforced by applicable law and infrastructure;
- role/purpose/consent restrictions remain visible to the system;
- access log surfaced where source infrastructure provides it;
- patient can download/share portable summary where permitted;
- proxy/delegation support where legally/technically available;
- sensitive/restricted data not exposed merely because CareOS can technically retrieve it;
- disputed/corrected information workflow;
- emergency access separated from routine access;
- child/dependent/incapacitated-patient cases treated as dedicated policy domains.

Patient product principle:

> **The patient should never need to reverse-engineer their own care from a stack of PDFs.**

---

# 15. Hospital ↔ practice ↔ other provider communication in the ideal future

```text
sender workflow
   ↓
minimum necessary structured context + source documents
   ↓
trusted identity + purpose + consent/restriction policy
   ↓
standard exchange rail / interoperable endpoint
   ↓
receiver validates format + issuer + patient + policy
   ↓
receiver context graph
   ↓
acknowledgement / task / status
   ↓
source updates flow back through governed channel
```

No “document sent” dead end.

A referral, transfer, consult or discharge is a **stateful workflow**:

```text
requested → received → accepted/declined → scheduled → performed → result available → follow-up closed
```

Documents remain useful evidence, but coordination should not depend on interpreting fax transmission as workflow state.

---

# 16. What is missing in today's global digital-health landscape — and what CareOS can add

This is a product inference, not a claim that no organisation has solved any individual piece.

## Existing building blocks already exist

- national EHR/patient-access systems;
- FHIR/HL7 interoperability standards;
- regional/national exchange infrastructure;
- EHDS direction in Europe;
- WHO global trust infrastructure direction;
- KIS/EHR/LIS/RIS/PACS vendors;
- workflow/AI companies such as Recare;
- national digital identity/trust systems.

## The recurring seams still need work

### 1. Trustworthy context composition

Transported data is not automatically usable context. State, provenance, time, version, contradiction and availability must survive composition.

### 2. Productised integration knowledge

Hospitals repeatedly pay to rediscover vendor/version/interface differences.

CareOS contribution: capability manifest + adapter catalog + conformance + compatibility registry + upgrade preflight.

### 3. Explicit degraded/offline semantics

Many apps treat failure as “no data.”

CareOS contribution: unavailable/stale/unknown are first-class states.

### 4. Agent authority architecture

AI systems need deterministic identity, permissions, tool contracts, audit and kill switches.

### 5. Cross-application clinical context contract

Apps should integrate with a stable trustworthy context layer instead of directly re-solving every source system.

### 6. Outcome contract

“AI accuracy” alone is not sufficient.

CareOS contribution: Time Returned to Care gated by safety + source verification.

### 7. Patient comprehension layer

Access to documents is not the same as understanding the care journey.

### 8. Portable content + trust + policy separation

FHIR validity, issuer trust and permission to use imported data are distinct.

---

# 17. Scope order — what we tackle first

## Phase 0 — foundation (now)

- clinical truth/provenance/lifecycle;
- patient identity boundaries;
- source-state semantics;
- derived clinical graph;
- audit model;
- agent capability boundary;
- adapter/install contract;
- resilience/offline policy;
- UI design system/accessibility;
- measurement protocol.

## Phase 1 — one irresistible workflow

Infectiology morning review/handover/discharge preparation.

Goal: measurable time-back without safety/verification loss.

## Phase 2 — one real hospital

- real workflow observation;
- hospital capability manifest;
- sandbox/deidentified integration;
- security/privacy review;
- shadow;
- read-only pilot.

## Phase 3 — repeatability

- second ward;
- second source/vendor configuration;
- second hospital;
- compatibility registry;
- prove configuration/conformance > bespoke code.

## Phase 4 — cross-provider continuity

- hospital ↔ practice/referral/follow-up;
- discharge coordination;
- patient longitudinal view;
- portable summary.

## Phase 5 — specialty packs

Choose from actual pull/impact, likely candidates:

- infectious diseases;
- emergency medicine;
- internal medicine;
- oncology;
- neurology;
- surgery/perioperative;
- pharmacy/medication safety;
- radiology/diagnostics;
- nursing/handover;
- discharge/case management.

Core stays stable. Specialty differences live in views/workflows/policies/evals.

## Phase 6 — Germany-scale interoperability

- reusable German adapters/profiles;
- ePA/TI/ISiK integration where appropriate;
- national conformance/compatibility evidence;
- procurement/assurance pattern;
- multi-site operations.

## Phase 7 — EU/global portability

- EHDS-aligned exchange components where applicable;
- IPS conformance;
- issuer/trust verification;
- country packs;
- low-bandwidth/offline portable summary;
- international pilots.

---

# 18. What “100%” means — and why it is not a useful single percentage

A healthcare system is never finished. Medicine, laws, vendors, threats, evidence and workflows change.

Use a **readiness vector**, not one vanity score:

```text
clinical usefulness
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
```

Current broad estimate (August 2026, architectural/pre-hospital view only):

- future-state architecture: **~70% articulated**;
- executable pre-hospital foundations: **~45–55% of the foundations we can build alone**;
- real-hospital product evidence: **<10%**;
- multi-hospital repeatability: **~0% evidenced**;
- Germany-scale operating system: **low single digits**;
- ideal global healthcare future: **not sensibly expressible as completion %**.

The important point:

> **We are far along in thinking and prototypes, but still near the beginning of reality.**

That is exactly why the next milestone is external contact, not another twenty speculative features.

---

# 19. Time horizon

We can make the architecture and pre-hospital proof coherent quickly; we cannot responsibly “figure out all healthcare” before working with the system.

Reasonable programme horizon:

```text
now–4 weeks      foundation + external critique + clinician synthetic evidence
1–3 months       first real integration discovery/sandbox if partner available
3–9 months       first bounded hospital pilot + one repeatable adapter path
9–18 months      second/third site, multi-specialty and cross-provider continuity
18–36 months     credible multi-hospital platform / national programme contribution
3–7 years        broad Germany infrastructure impact if institutions adopt and evidence supports scale
5–10+ years      international ecosystem contribution
```

These are programme planning ranges, not promises; hospital/regulatory/vendor timelines dominate once we leave the synthetic environment.

---

# 20. The difficult questions we keep permanently open

1. Which information should **not** be centralised?
2. Who is authoritative when sources conflict?
3. How do we prove patient identity across institutions safely?
4. How do we keep “helpful AI” from increasing automation bias?
5. What remains available during total network/model/control-plane failure?
6. Which functions become medical-device functionality as intended use expands?
7. Who owns harm when human, model, adapter and source all contribute?
8. How do patients challenge incorrect information?
9. How do we support people without smartphones, strong connectivity or digital literacy?
10. How do we handle children, guardianship, proxy access and sensitive domains?
11. How do we prevent a national interoperability layer becoming national surveillance infrastructure?
12. How do we make audits useful without creating another high-value privacy target?
13. How do we safely retire legacy workflows after years of parallel operation?
14. How do we stop vendor-specific “extensions” from recreating lock-in above FHIR?
15. How do we fund/maintain open adapters and conformance infrastructure for decades?
16. How do we measure whether time saved becomes patient-facing time rather than more throughput/admin?
17. How do we prevent alert fatigue and AI-generated work?
18. When should an agent abstain rather than help?
19. What is the minimum viable context in an emergency or offline setting?
20. How do we prove benefits across age, language, disability and socioeconomic groups rather than only expert digital users?
21. What happens if CareOS itself becomes a systemic dependency and then fails?
22. How do we design updates so one bad release cannot disrupt hundreds of hospitals?
23. How do we create credible independent oversight/conformance rather than self-certification?
24. How can a hospital leave CareOS without losing access to its own integration knowledge/data?
25. Are we actually improving outcomes, or merely making the same broken workflow faster?

Every roadmap review should revisit these.

---

# 21. Definition of success

The strongest future testimonials would not be about AI.

A clinician:

> “I open the patient and I know what changed, what is pending and where it came from. I spend my time deciding and caring, not reconstructing the chart.”

A nurse:

> “Handover is calmer. I know what is unfinished. I do not need another alert system.”

A patient:

> “I understand what happened and what happens next. I can see my information and ask better questions.”

Hospital IT:

> “The KIS changed version and we knew the compatibility problem before rollout. We did not rebuild every app.”

Hospital leadership:

> “We can show time returned to care and safety together.”

And the health system:

> “Information follows the patient through governed interoperable infrastructure instead of forcing people to become the integration layer.”

That is the end state we work backward from.
