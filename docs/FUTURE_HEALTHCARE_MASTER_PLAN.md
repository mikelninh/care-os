# CareOS Future Healthcare Master Plan

Baseline: **18 August 2026**

> Mission: make healthcare feel coherent to the people giving and receiving care — without centralising authority, hiding uncertainty or forcing hospitals to replace every system they already depend on.

This is the end-to-end product/architecture north star. It is not a claim that CareOS can deliver all of it today.

---

# 1. The desired future in one sentence

> **Every authorised person sees the right patient context, at the right moment, in the right interface, with the source, freshness, uncertainty and responsibility still visible — and routine coordination/documentation happens with almost no manual friction.**

The patient remains a person, not a record.

The clinician remains the accountable professional, not a button-pusher for an AI.

The hospital keeps its systems of record.

The interoperability layer makes those systems behave like one coherent environment.

---

# 2. What healthcare should feel like

## For a physician

Open the patient in the KIS.

CareOS is already in the same patient context.

The first screen answers:

```text
What changed since I last looked?
What is pending?
What contradicts something else?
What could be important today?
What needs my decision?
Where did each item come from?
What work can be safely drafted/prepared for me?
```

No second login. No second patient search. No re-reading 35 documents to reconstruct a timeline.

## For nursing

At shift handover:

```text
what changed this shift
what must happen next shift
what is pending / overdue
new isolation or infection-control information
new medication / order changes
lines / drains / wounds / mobility / nutrition / risk context
which source confirmed each important change
```

Not another documentation surface: a role-specific projection of the same source-linked context.

## For patients

```text
what do we currently know?
what changed today?
which results are still pending?
what medicines am I currently documented as taking?
what is the plan / next appointment / discharge step?
who accessed my shared record?
what does this term mean in plain language?
how can I flag something that looks wrong?
```

Plain language is a presentation layer. It never silently replaces the original clinical wording.

## For hospital IT

```text
which source systems are connected?
which adapters / versions are running?
which capabilities are conformant?
which sources are stale / unavailable?
which patients/workflows are affected?
what changed in this release?
can I roll it back safely?
what data leaves the provider boundary?
```

## For hospital leadership

```text
Time Returned to Care
workflow adoption
safety-stop events
source reliability
support burden
integration effort per site
avoidable duplicate work
patient experience
```

No vanity AI metrics.

---

# 3. Universal foundation, role-specific products

```text
                    PATIENT / PERSON
                          │
              identity + treatment context
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
 provider systems                       ePA / external
 KIS · LIS · RIS/PACS                  sources / partners
 docs · devices · PVS                       │
        └─────────────────┬─────────────────┘
                          ↓
                   reusable adapters
                          ↓
               canonical clinical graph
    facts · sources · time · state · relations · tasks
                          ↓
              deterministic policy boundary
                          ↓
       ┌──────────────┬──────────────┬──────────────┐
       ↓              ↓              ↓              ↓
   clinician       nursing        patient        operations
      view            view           view            view
       │              │              │              │
       └──────────────┴───────┬──────┴──────────────┘
                              ↓
                       bounded agents
                              ↓
                         human authority
```

One truth substrate. Many projections.

---

# 4. Device strategy

## Clinical workstation / PC — primary

Why:

- KIS/PVS workflows already live there;
- larger context and documents need screen space;
- existing SSO/context launch is easier to preserve;
- hospitals often use managed Windows, VDI or Citrix;
- no new device should be required for core value.

Target experience:

```text
browser / embedded launch
no local admin rights required
keyboard-first navigation
old/managed Windows compatible
WCAG-accessible
fast with modest hardware
no GPU requirement
```

## Tablet — rounds / bedside companion

Use for:

- rounds;
- bedside explanation;
- quick source review;
- task confirmation;
- secure voice capture;
- patient-facing shared view.

Tablet must never become a second documentation island.

## Mobile — lightweight, not a mini-KIS

Use for:

- secure task inbox;
- carefully bounded notifications;
- voice/photo capture where governance permits;
- patient communication;
- authentication / approval where appropriate.

Avoid dense clinical decision interfaces on phones unless a workflow is explicitly designed and validated for them.

## Patient devices

Patient access should work on smartphone **and** web/desktop where national infrastructure permits, while integrating with official ePA access rather than replacing it.

---

# 5. Connectivity and offline strategy

CareOS should **not be clinically offline-first**.

Healthcare data becomes dangerous when old information looks current.

Desired hierarchy:

```text
ONLINE
fresh source-linked context
all allowed read/draft functions

DEGRADED
some sources unavailable
available facts remain visible
missing source clearly shown
may_assert_absence = false
high-risk automation reduced/disabled

OFFLINE
legacy KIS/local workflow remains fallback
optional encrypted approved last-known cache = read-only
freshness age unavoidable in UI
no external send
no autonomous agent tools
no transactional write
no negative/absence inference from missing data
```

Offline queued writes are a future workflow-specific capability, not a general platform feature.

---

# 6. The first ideal use case

## Infectiology: morning review → rounds → documentation → handover

Why this is strong:

- information comes from several sources;
- lifecycle matters: pending / preliminary / final / corrected;
- treatment evolves over time;
- missed information can matter clinically;
- source verification remains important;
- documentation burden is obvious;
- one context can help physician, nursing and discharge workflows.

### Target clinician screen

```text
PATIENT HEADER
identity · encounter · location · allergies · code status where appropriate

SINCE LAST REVIEW
3 new / changed items

NOW
current documented problems
current documented therapies
key current trends
infection-control context

PENDING
microbiology / tests / consults / tasks

CONTRADICTIONS / REVIEW
items that do not reconcile cleanly

PLAN / WORK
human-entered plan + agent-prepared drafts

SOURCES
one-click provenance
```

The default screen should not begin with a chatbot.

The agent is available **inside the workflow**, not as the workflow.

---

# 7. Time Returned to Care targets

These are **product targets, not current CareOS claims**.

Germany's 2025 DKI hospital survey reported that physicians and nurses spend almost three hours per day on documentation/evidence obligations; the survey estimated that reducing that burden by one hour per full-time worker would correspond arithmetically to roughly 22,000 physician and 49,000 nursing full-time equivalents becoming available for patient-near work.

Sources:
- https://www.dki.de/forschungsprojekt/dki-blitzumfrage-aktuelle-burokratiebelastung-in-den-krankenhausern-2025
- https://pubmed.ncbi.nlm.nih.gov/34937102/

## Product targets

| User | First useful pilot target | Mature ambition |
|---|---:|---:|
| physician | **≥20 min / shift** returned on targeted workflows | **45–60 min / shift** |
| nurse | **≥15 min / shift** | **30–45 min / shift** |
| social / discharge team | **≥20 min / eligible case** | **30–60 min / eligible case** |
| coding / admin | **≥20% targeted workflow reduction** | **40%+ targeted workflow reduction** where safe |
| hospital IT | **hours, not weeks**, for already-supported adapter/config changes | configuration + conformance for routine sites |
| patient | less repeated history, fewer coordination calls, faster understanding | continuity that feels institution-independent |

A time saving is invalidated for rollout when it causes:

```text
wrong patient
missed pending item
unsupported claim
verification decay
unauthorised action
clinically meaningful stale-data confusion
```

**Safety beats speed.**

---

# 8. Where the time goes — and how we attack it

Common high-friction categories supported by German hospital research include documentation, searching/reading fragmented records and calling/coordination.

One German university-hospital observation found 37.1% of observed physician time interacting with health records: 9.0% searching, 7.7% reading and 20.5% writing, plus 6.8% calling.

Source: https://pubmed.ncbi.nlm.nih.gov/34937102/

## CareOS attack surface

### Searching / reconstructing

Before:

```text
KIS → lab → documents → old discharge letter → ePA → call ward → handwritten note
```

After target:

```text
patient context auto-launched
→ changed/pending/relevant items already composed
→ source available one click away
```

### Reading

Before: read entire documents to discover what changed.

After: change-aware timeline + role-specific projection; original source remains inspectable.

### Writing

Before: retype history, findings and prior work into multiple documents.

After: agent prepares source-linked draft; clinician approves/edits; approved write route is explicit and verifiable.

### Calling / coordination

Before: phone/fax/email to discover whether information or follow-up exists.

After: structured task/status exchange through existing trusted rails and networks; humans call when human discussion is actually needed.

### Duplicate entry

Before: same patient/fact manually re-entered into multiple systems.

After: map once into the canonical context, then use approved adapters/Operator-style bridges where necessary.

---

# 9. Agents: superpowers, not hidden authority

The ideal agent behaves like a highly capable colleague with a visible badge, narrow job description and revocable permissions.

## Safe agent jobs

- pre-round chart preparation;
- "what changed since yesterday?";
- source-linked timeline construction;
- draft progress note / discharge letter / handover;
- extract structured candidates from documents;
- prepare referral/aftercare package;
- find missing required fields;
- translate presentation text while preserving source wording;
- explain jargon to patients;
- prepare patient questions for clinician review;
- route administrative tasks;
- watch for newly finalised results and surface them to the correct workflow;
- simulate conformance / rollout checks for IT.

## Agent jobs that require much stronger evidence / regulation

- diagnostic recommendations;
- treatment recommendations;
- medication changes;
- autonomous order entry;
- autonomous discharge decisions;
- autonomous external communication with clinical consequence.

## Rule

> **Model proposes. Deterministic policy decides what the model is even allowed to attempt. Human authority remains explicit.**

The agent must never choose its own patient, widen its own permissions, infer break-glass authority, hide source failure or silently convert a draft into source truth.

---

# 10. The clinical context graph

A graph is likely a critical conceptual layer because healthcare is relationships over time, not a bag of documents.

Example:

```text
Patient
 ├─ Encounter
 │   ├─ Diagnosis
 │   ├─ Medication
 │   ├─ Lab result ── derived from ── Specimen
 │   ├─ Task ── assigned to ── Team
 │   ├─ Document ── authored by ── Clinician
 │   └─ Decision ── supported by ── Evidence
 │
 ├─ Allergy ── contradicted by? ── Document statement
 └─ Care plan
```

Add operational/trust edges:

```text
fact → asserted by → source resource
fact → supersedes → earlier fact
fact → contradicts → other fact
agent draft → derived from → facts
human decision → reviewed → draft
access event → actor → patient context
portable item → issued by → organisation
```

Important: **graph is a logical contract first.** CareOS does not need to force every hospital into a graph database. It can project graph semantics over relational/FHIR/document stores.

---

# 11. Audit should be a first-class product

Every consequential access/action should be reconstructable:

```text
who / what acted?
for which organisation?
which patient / encounter?
under which treatment context?
which source/facts were visible?
which agent/model/tool version participated?
what was proposed?
what did the human approve/change/reject?
what was written/sent?
what happened afterward?
```

Audit has three audiences:

1. **clinician / patient** — understandable transparency;
2. **hospital operations/security** — incident reconstruction;
3. **engineering/quality** — reproducible regressions.

Audit must not itself become an uncontrolled PHI lake.

---

# 12. Worst cases — designed before delight

| Worst case | Architectural prevention |
|---|---|
| wrong patient | authoritative patient/encounter binding outside model; cross-source ID strategy; hard rejection |
| pending result shown as negative | lifecycle state is part of truth contract |
| source outage shown as "nothing found" | unavailable ≠ absent; partial context disables absence claims |
| stale cache looks current | freshness/last-success state unavoidable in UI |
| agent hallucinates | model output is untrusted draft; source evidence required |
| agent expands privileges | deterministic gateway + signed/narrow delegation |
| duplicate patient merge | no fuzzy auto-merge; governed MPI/resolver only |
| unit/terminology mapping error | original value/code preserved + mapping lineage + review |
| KIS upgrade silently breaks adapter | capability + conformance + upgrade preflight + canary |
| compromised credential | least privilege, short-lived identity, revocation, audit, network bounds |
| ransomware/provider outage | provider-local fallback, rebuild from authoritative sources, tested recovery |
| model provider unavailable | core context remains useful without model; deterministic fallback |
| clinician trusts automation too much | visible source, review affordances, verification metrics |
| alert fatigue | workflow-owned, thresholded, role-specific signals; no global "AI alerts" feed |
| hidden patient data / consent restriction | receiving view must preserve restriction/availability uncertainty; never infer completeness |
| translation changes meaning | source text preserved; translation presentation-only |
| cross-border issuer untrusted | content validity separated from issuer trust and local-use policy |

---

# 13. Patient access and power

CareOS should align with official patient-access infrastructure rather than create a shadow patient record.

Germany's ePA already gives insured people access/control mechanisms and access logs; provider access is tied to treatment context, and patients can manage institutional access through the ePA mechanisms.

Sources:
- https://www.gematik.de/anwendungen/epa-fuer-alle/faq
- https://www.gematik.de/anwendungen/epa-fuer-alle/krankenhaeuser
- https://www.gematik.de/newsroom/news-detail/das-sind-die-neuen-funktionen-der-epa

## CareOS patient view should add usability

```text
NOW
plain-language current summary

CHANGED
new results / changed plan / new document

PENDING
things still waiting

NEXT
appointments, follow-up, discharge steps

MEDICATION
source-linked current documented list + uncertainty

MY DATA
source documents where available through governed access

ACCESS
who accessed the shared record / when, where the official infrastructure exposes it

CORRECT / ASK
flag possible errors or ask a question without directly rewriting source truth
```

A patient-facing AI may explain or prepare questions. It must make uncertainty visible and must not impersonate the treating clinician.

---

# 14. Communication between hospitals, practices and care partners

Do not invent another universal inbox.

Germany already has national rails including ePA, TI and KIM; EHDS/MyHealth@EU is building cross-border exchange requirements for priority health-data categories.

Sources:
- https://fachportal.gematik.de/anwendungen/kommunikation-im-medizinwesen
- https://www.gematik.de/krankenhaeuser
- https://health.ec.europa.eu/ehealth-digital-health-and-care/european-health-data-space-regulation-ehds_en

Ideal composition:

```text
WITHIN HOSPITAL
provider-local canonical context + role views

HOSPITAL ↔ PRACTICE
national standard rails / ePA / KIM / structured FHIR/document exchange where applicable

HOSPITAL ↔ POST-ACUTE / REHA / NURSING
structured referral/status networks such as Recare + national rails

EU CROSS-BORDER
EHDS / MyHealth@EU priority datasets

GLOBAL
FHIR + International Patient Summary-shaped minimum context + explicit issuer trust + local policy
```

CareOS makes the content trustworthy/usable across these rails. It should not replace the rails.

---

# 15. Hospital relationship: product + critical service

A successful hospital relationship is not "install software and disappear".

## Pilot cadence

```text
daily / live channel during first days
weekly implementation + clinical review
weekly metrics/safety review
```

## Production cadence

```text
24/7 critical incident channel
monthly operational review
quarterly clinical/value review
scheduled compatibility review before KIS/LIS upgrades
annual disaster-recovery / security exercises
continuous regression + conformance updates
```

## Release rule

No silent changes to:

- model/provider;
- prompts that affect clinical output;
- adapter mapping;
- terminology mapping;
- workflow authority;
- write/send capability.

Every consequential change is versioned, tested, canaried and rollbackable.

See `docs/CRITICAL_SERVICE_OPERATING_MODEL.md`.

---

# 16. Three hospital archetypes

## A. Smaller / legacy-heavy hospital

Reality:

```text
managed Windows
small IT team
one main KIS
HL7/interface engine
paper/fax leftovers
limited API surface
```

CareOS path:

```text
browser-first
no device purchase
manifest + preflight
one supported adapter
one workflow
shadow first
UI bridge only if typed integration is genuinely unavailable
```

Today CareOS generic HL7/UI-bridge paths remain contract-only; this archetype is a priority real-world adapter challenge, not something to pretend is solved.

## B. Large university hospital

Reality:

```text
multiple KIS/subsystems
LIS/RIS/PACS
specialty systems
MPI/complex identity
FHIR/ISiK plus legacy feeds
strict research/security governance
```

CareOS path:

```text
multiple provider-local connectors
trusted MPI resolver
clinical context graph
one department first
central conformance/observability
role views
```

## C. Hospital group

Reality:

```text
many sites
repeated vendor combinations
central IT/security
local clinical variation
```

CareOS path:

```text
one shared control plane without routine PHI
site-local data planes
adapter/version compatibility registry
fleet-safe canary releases
shared synthetic conformance suites
local clinical policy packs
```

This is where adapter reuse becomes infrastructure economics.

---

# 17. First day → first week → first month

## Day 0 — no clinician yet

IT:

1. install synthetic/deidentified data plane;
2. create Hospital Capability Manifest;
3. run `doctor` + `preflight`;
4. discover FHIR capabilities where permitted;
5. resolve identity / source / network blockers;
6. run conformance;
7. verify rollback.

## Day 1 — synthetic workflow with team

15-minute orientation, not training school.

Clinicians use a synthetic version of their own workflow.

Capture confusion and missing context.

## Days 2–5 — shadow

Approved deidentified/source sandbox where available.

No new clinical dependency.

Measure:

```text
time
searches
source opens
corrections
pending items
system errors
workflow abandonment
```

## Week 2–4 — one live read-only workflow, only after gates

One ward/team.

Legacy remains available.

No autonomous writes.

## Month 2+

Only expand if:

```text
users repeatedly choose it
measurable time returned
no safety-stop signal
verification does not decay
support burden is acceptable
```

---

# 18. Synthetic before/after inspiration

These examples are **hypotheses to test, not measured CareOS outcomes**.

### Physician morning review

**Before:** 18 minutes: KIS + lab + document search + old letter + one phone clarification.

**After hypothesis:** 6 minutes: auto-launched patient context, changed/pending panel, 2 source checks, agent-prepared progress-note skeleton.

**Potential return:** 12 minutes per reviewed complex case.

### Nursing handover

**Before:** 22 minutes: read free-text notes + medication/order changes + handwritten/parallel task list.

**After hypothesis:** 9 minutes: role-specific changes, pending tasks, isolation changes, source-backed exceptions.

**Potential return:** 13 minutes per handover set.

### Discharge / aftercare coordination

**Before:** repeated calls/faxes, copy-paste and status chasing.

**After hypothesis:** structured aftercare need, digital routing/status, agent-prepared package, source-linked data reused once.

**Potential return:** tens of minutes per eligible case; must be measured against the real workflow. Recare publicly reports 30–60 minutes per case for its Discharge product, which is useful external proof that this workflow category can produce material savings — not evidence that CareOS itself has achieved it.

Source: https://recareai.com/loesungen/loesungen-fuer-krankenhaeuser

### Patient discharge understanding

**Before:** verbal explanation + dense letter + later call because plan is unclear.

**After hypothesis:** source-preserving discharge summary + plain-language view + pending items + next steps + question channel.

**Potential value:** better understanding and fewer avoidable coordination contacts; health-outcome claims require prospective evidence.

---

# 19. What is missing in today's healthcare stack

No country has solved all of these simultaneously.

CareOS hypothesis: the missing layer is the combination of:

1. **usable context**, not more raw documents;
2. **provenance as correctness**;
3. **clinical lifecycle/uncertainty as data**, not prose;
4. **cross-source patient identity that never guesses**;
5. **open adapter contracts + executable conformance**;
6. **relationship/temporal graph semantics**;
7. **bounded agent authority**;
8. **patient-readable transparency**;
9. **failure-aware/offline-aware UX**;
10. **upgrade compatibility before production**;
11. **Time Returned to Care as outcome metric**;
12. **hospital-owned data plane / anti-lock-in**;
13. **local → national → EU → global portability without forcing one global database**.

---

# 20. Master roadmap

## Phase 0 — principles / synthetic proof **DONE / ACTIVE**

- provenance;
- lifecycle;
- human authority;
- agent containment;
- synthetic clinician workflow;
- adversarial tests.

## Phase 1 — self-install foundation **ACTIVE**

- Hospital Capability Manifest;
- adapter maturity;
- FHIR discovery;
- local data plane;
- Docker/Helm;
- upgrade preflight;
- offline/degraded policy;
- clinical graph contract;
- service operating model.

## Phase 2 — external reality

- Pavlo/Recare critique;
- real clinician sessions;
- first real hospital manifest;
- deidentified KIS/LIS sandbox;
- first real adapter compatibility record.

## Phase 3 — first hospital shadow workflow

- real SSO/context launch;
- real patient/encounter identity;
- source freshness/outage;
- one team;
- Time Returned to Care baseline + after;
- no write authority.

## Phase 4 — first useful production workflow

- accountable clinical/security/privacy approval;
- 24/7 operating model;
- real audit/SIEM;
- rollback/recovery exercise;
- read/draft copilot;
- longitudinal user evidence.

## Phase 5 — second hospital / different vendor

This is the first real infrastructure proof.

- adapter reuse;
- compatibility registry;
- custom engineering hours/site;
- fleet upgrade testing.

## Phase 6 — specialty platform

Add specialties from shared core, not forks:

```text
Infectiology
Internal Medicine
Emergency
Oncology
Neurology
Surgery
ICU
Cardiology
Nephrology
Paediatrics
Psychiatry
Ob/Gyn
...
```

Each specialty pack defines:

- relevant projection;
- workflow metrics;
- terminology/rules;
- high-risk failure cases;
- agent tools;
- patient explanation needs.

## Phase 7 — care continuum

- practices/PVS;
- rehab;
- nursing;
- pharmacy;
- home care;
- emergency services;
- patient/caregiver access.

## Phase 8 — Germany reference fabric

- open adapter ecosystem;
- national conformance lab;
- agent capability standard;
- patient transparency ledger;
- public procurement requirements;
- ePA/TI/EHDS integration.

## Phase 9 — EU / global portability

- EHDS priority categories;
- IPS-shaped portable minimum summary;
- trust/issuer verification;
- country policy packs;
- cross-border translation with source preservation.

## Phase 10 — continuously improving healthcare operating environment

There is no true "100% complete". The final phase is an ecosystem where new systems, agents and workflows plug into stable safety/interoperability contracts and improve without forcing every hospital to rebuild its foundation.

---

# 21. How far are we?

A single percentage hides too much, but as a forcing function:

```text
vision / principles / reference architecture       ~70%
synthetic engineering foundation                    ~55%
self-install / integration product                  ~35%
clinician-facing product evidence                   ~25%
patient-facing product                              ~15%
real hospital integration evidence                   ~5%
production operations / assurance                   ~10%
multi-hospital repeatability                         ~2%
Germany-wide ecosystem                               ~2%
EU/global operational interoperability               ~1%
```

Weighted against the full endgame: **roughly 10–15%**.

Weighted against what can responsibly be done before access to real hospital systems/users: **roughly 70–80%**.

That is not discouraging. It means the next 20% cannot be created by more imagination alone — it requires real users, hospital systems and partners.

---

# 22. How long does the whole thing take?

The technical specification is not the long pole. Institutional proof is.

Reasonable ambition if strong hospital/industry partners join:

```text
weeks         → complete next foundation contracts + synthetic UX/proofs
1–3 months    → first real manifest / sandbox / clinician evidence
3–9 months    → first serious read-only/shadow hospital workflow
6–18 months   → first production-grade workflow + second-site repeatability evidence
1–3 years     → meaningful multi-hospital adapter/platform footprint
3–7+ years    → credible national/EU infrastructure influence
continuous    → global interoperability, specialty expansion, safety improvement
```

The goal is not to "finish healthcare software". The goal is to establish foundations that remain stable while everything above them improves.

---

# 23. The hard questions we will keep asking

- Did this actually return time to care?
- Did users verify less because the UI became too persuasive?
- What happens when one source lies, lags or disappears?
- What happens when two systems disagree about the patient?
- What happens when the model is compromised?
- Can the hospital keep working if CareOS disappears right now?
- Can we prove which source supported every consequential output?
- Can the patient understand what happened and who saw their data?
- Can Hospital B reuse what Hospital A already paid to discover?
- Can an application be replaced without rebuilding source integrations?
- Can a KIS upgrade be tested before clinicians discover the breakage?
- Can a human override the system safely?
- Can a bad override be audited without creating blame culture?
- Are we reducing calls/faxes, or merely creating another inbox?
- Are we solving the workflow or automating bureaucracy that should be deleted?
- Which feature should **not** exist because its failure mode is unacceptable?

These questions are part of the product.

---

# 24. Endgame test

The product is succeeding when:

**Clinician:**
> "I opened the patient and everything important was already there."

**Nurse:**
> "Handover is clearer, and I know what is still unresolved."

**Patient:**
> "I understand what is happening and I can see where the information came from."

**Hospital IT:**
> "We upgraded the KIS, tested compatibility before rollout and did not rebuild every integration."

**Hospital leadership:**
> "We can prove time returned, safety behavior and adoption — not just AI usage."

**Application vendor:**
> "We integrated once against a stable clinical context contract."

**Healthcare system:**
> "Information follows the patient through trusted standards instead of being recreated by phone, fax and copy-paste at every boundary."

That is the future CareOS should work backward from.
