# CareOS Stakeholder Journeys

Baseline: **18 August 2026**

> One clinical truth substrate, many interfaces. Nobody should be forced to become a CareOS expert just to do their actual job.

All scenarios below are product targets / synthetic journey hypotheses until tested with real users.

---

# 1. Physician

## Before

A complex inpatient morning review may require:

```text
open KIS
find yesterday's note
open lab system
find microbiology
scan medication list
open imaging report
find old discharge letter
check ePA / scanned documents
call ward or colleague about unresolved context
reconstruct timeline mentally
write the same context again
```

## First day

- CareOS launches from the existing patient context.
- 10–15 minute orientation using synthetic cases.
- Physician learns only four concepts:
  1. changed;
  2. pending;
  3. review/contradiction;
  4. source.
- No chatbot tutorial required.

## Everyday

Default screen:

```text
CHANGED SINCE LAST REVIEW
NOW
PENDING
REVIEW / CONTRADICTIONS
WORK / DRAFTS
SOURCES
```

Agent helps with:

- pre-round synthesis;
- timeline;
- draft note;
- discharge summary skeleton;
- missing required-field check;
- "show me the source";
- "what changed since yesterday?".

## After one week target

The physician should be able to say:

> "I stopped opening five places just to understand the patient."

Target proof:

- ≥20 min/shift returned on targeted workflows;
- fewer system switches/searches;
- zero wrong-patient events;
- zero missed-pending safety stops attributable to CareOS;
- source-open rate does not collapse.

---

# 2. Nurse

## Before

```text
free-text notes
handover sheet
medication/order screen
paper task list
verbal clarification
multiple places for isolation / mobility / line / wound / nutrition context
```

## First day

The nurse sees a role-specific synthetic handover screen.

No AI terminology.

The UI asks practical questions:

```text
what changed?
what must happen?
what is late/pending?
what needs clarification?
```

## Everyday

- shift-change delta instead of full-chart reread;
- tasks grouped by patient/urgency/time;
- new/changed care-relevant facts highlighted;
- source available behind the fact;
- unclear/contradictory item can be escalated without rewriting it.

Agent helps with:

- handover draft;
- task extraction from approved plans/documents;
- structured voice draft;
- identifying missing documentation fields;
- explaining source change, not choosing treatment.

## After one week target

> "Handover tells me what changed, not just everything that has ever happened."

Target proof:

- ≥15 min/shift returned;
- fewer missed handover items;
- no increase in alert burden;
- fewer duplicate notes/task lists.

---

# 3. Social service / discharge management

## Before

```text
search chart for aftercare need
call ward/doctor
copy patient context into referral
phone/fax multiple facilities
track replies manually
repeat missing information
update hospital documentation separately
```

## First day

- CareOS/Recare-style workflow receives structured aftercare context from the same patient substrate.
- User sees only data needed for placement/transition.
- Missing fields are explicit.

## Everyday

- aftercare need visible earlier;
- referral package prepared once;
- status/replies structured;
- no re-keying unchanged patient facts;
- source changes invalidate/review the appropriate parts of the referral.

Agent helps with:

- missing-field collection;
- referral package draft;
- facility/status summarisation;
- patient/family explanation draft;
- follow-up task creation.

## After one week target

> "I spend my time solving difficult placements, not chasing the same information."

Target proof:

- ≥20 minutes returned per eligible case;
- fewer outbound clarification calls;
- fewer duplicate entries;
- earlier aftercare initiation;
- no inappropriate data sharing outside permitted scope.

---

# 4. Pharmacist / medication safety role

## Everyday target

```text
current documented medication
source + prescription/dispensation context
changes over time
allergy/intolerance context
renal/hepatic context where permitted/relevant
unreconciled discrepancies
pending medication reconciliation tasks
```

Agent may:

- compare lists;
- surface discrepancies;
- prepare reconciliation worksheet;
- fetch supporting source information.

Agent must not autonomously alter medication.

Proof:

- reconciliation time;
- discrepancy detection;
- source-verification behavior;
- correction burden.

---

# 5. Laboratory / microbiology

CareOS should not replace LIS workflows.

Value:

- preserve preliminary/final/corrected/cancelled status;
- make newly finalised results visible to downstream workflows;
- link organism/specimen/result relationships;
- show which workflow/users consumed earlier preliminary information;
- make source outage visible.

Agent may:

- route newly finalised results to approved task queues;
- prepare change summaries;
- never convert pending to negative.

---

# 6. Radiology

CareOS should not become a PACS viewer.

Value:

- report availability/state;
- key report relationships to encounter/problem/task;
- source link into existing image/report systems;
- changed/addended report visibility.

Agent may summarise a report for workflow/patient presentation only with the original report one click away.

---

# 7. Coding / medical controlling

## Before

- search documentation for required evidence;
- clarify missing documentation;
- manually trace diagnosis/procedure support;
- repeated requests to clinicians.

## Everyday target

- evidence-linked coding workbench;
- missing evidence explicitly separated from absent evidence;
- versioned source documents;
- draft suggestions never silently committed.

Agent may:

- prepare evidence bundle;
- identify missing documentation;
- draft clarification request.

Target proof:

- workflow time reduction;
- fewer clinician interruptions;
- auditability of evidence.

---

# 8. Hospital IT / integration engineer

## First day

```bash
careos init
careos doctor
careos preflight
careos discover-fhir
```

The system tells them:

- what it knows;
- what it does not know;
- what adapter exists;
- what adapter is contract-only;
- what identity assumptions are unsafe;
- what network/owner requirements are missing.

## First week

- sandbox connection;
- conformance suite;
- source-state tests;
- synthetic outage tests;
- rollback rehearsal;
- generated review pack.

## Everyday

Operations screen:

```text
source health
adapter versions
compatibility status
latency
failed mappings
identity failures
stale-source counts
deployment version
policy/model version
rollback state
```

No PHI-heavy central fleet dashboard by default.

## After one month target

> "This behaves like a product we operate, not a consultant's integration project."

Proof:

- integration engineer hours/site;
- configuration-only change rate;
- upgrade regressions caught before rollout;
- adapter reuse rate;
- support burden.

---

# 9. CISO / security team

They should never need to reverse-engineer the architecture from a sales deck.

They receive:

```text
data-flow map
network destinations
identity/auth path
secret handling
roles / treatment context
agent authority model
logging/audit locations
subprocessors/providers
retention/cache policy
software versions + SBOM
vulnerability / patch process
rollback / incident process
```

Every integration change produces a diff.

No model or developer has production break-glass by implication.

---

# 10. Data Protection Officer / privacy

Needs:

- purposes/data categories;
- provider/control-plane separation;
- data minimisation;
- retention;
- recipients/processors;
- cross-border/provider path;
- patient access/correction flow;
- audit;
- treatment-context/consent/restriction handling;
- DSFA/DPIA support evidence.

CareOS generates the technical facts. It does not automate legal approval.

---

# 11. Clinical leadership / chief physician

First questions:

```text
What exact workflow changes?
What can go wrong?
How will I know it is helping?
What does the AI decide?
What stays with the clinician?
Can we stop immediately?
What happens during downtime?
```

Dashboard should show:

- Time Returned to Care;
- adoption;
- correction rate;
- missed-pending/safety stops;
- source verification;
- uptime/degraded time;
- incident/rollback history.

No "AI messages generated" KPI as primary evidence.

---

# 12. CFO / hospital management

Needs economic evidence that connects to operations:

```text
hours returned
implementation/support hours
licence/platform cost
avoidable duplicated work
length-of-stay/process metrics where causality can be evaluated
staff satisfaction/retention signals
integration marginal cost
```

CareOS should not promise savings from hypothetical FTE elimination. The first economic frame is **capacity returned to care**.

---

# 13. Patient

## Before

- repeats history;
- waits for professionals to find information;
- receives dense documents;
- may not know what is pending;
- calls because next step is unclear;
- cannot easily see how one institution relates to another.

## First use

Patient does not need to become a hospital-IT user.

The patient view begins with:

```text
WHAT WE KNOW
WHAT CHANGED
WHAT IS STILL PENDING
WHAT HAPPENS NEXT
MY MEDICINES
MY DOCUMENTS / SOURCES
WHO ACCESSED MY SHARED RECORD
ASK / FLAG A POSSIBLE ERROR
```

## Agent

Patient agent can:

- explain medical vocabulary;
- translate presentation;
- prepare questions for the care team;
- explain next steps;
- help find a document/result.

It must clearly distinguish:

```text
source record
plain-language explanation
clinician plan
AI-generated explanation
```

## Target feeling

> "I know what is happening to me."

---

# 14. Family / authorised caregiver

Only through explicit delegated access / applicable official mechanisms.

Needs:

- current plan;
- appointments/follow-up;
- discharge needs;
- medication/support instructions;
- questions to ask;
- notification preferences.

Caregiver access must never become a shortcut around patient choice or legal authority.

---

# 15. General practice / outpatient specialist

Long-term CareOS projection:

- incoming hospital discharge context structured;
- new/changed medications;
- pending hospital results/follow-up;
- source-linked summary;
- ePA/KIM/standard exchange used rather than another proprietary inbox;
- referral questions and results tied together longitudinally.

The same core contracts apply; PVS/practice-specific interfaces become country/site packs.

---

# 16. Reha / nursing facility / home-care provider

Needs a **minimum necessary transition view**, not the entire acute-care record.

```text
care needs
mobility
wounds
nutrition
medication
infection-control context
cognitive/communication needs
equipment
follow-up
contacts
source / freshness
```

This is a role/purpose-limited projection.

---

# 17. Emergency department

Potentially one of the highest-value future surfaces because time and uncertainty are extreme.

Target:

```text
identity confidence
allergies / medication
important history
recent admissions/procedures
current active problems
latest critical results
patient summary / ePA / external sources
what is unavailable
```

The UI must prioritise **confidence and freshness**, not completeness theatre.

Emergency use requires very careful break-glass, identity and latency design before production.

---

# 18. ICU

High-frequency, high-risk environment.

CareOS should not try to replace the ICU chart/monitoring system.

Potential role:

- longitudinal context across ICU + hospital sources;
- newly changed external reports;
- source-linked handover;
- goals/decisions/context;
- family/patient narrative continuity.

Autonomous clinical action threshold should be exceptionally high.

---

# 19. Specialists over time

Each specialty gets a projection, not a fork.

Examples:

```text
Infectiology   → micro lifecycle / therapy / isolation / source changes
Oncology       → tumour timeline / pathology / therapy cycles / response / toxicity
Neurology      → symptom/course / imaging / neurophysiology / medication changes
Nephrology     → renal trend / dialysis / fluid / medication dosing context
Cardiology     → ECG/imaging/interventions / meds / longitudinal events
Surgery        → operation / pathology / drains / complications / follow-up
Psychiatry     → longitudinal plan / medication / risk/goals / strong privacy boundaries
Paediatrics    → guardian/delegation / growth/dosing / developmental context
Ob/Gyn         → pregnancy episode / maternal-fetal context / time-critical workflow
```

Every pack declares:

- role views;
- high-value tasks;
- high-risk failures;
- metrics;
- terminology;
- agent capabilities;
- patient explanation needs.

---

# 20. Three hospital first-week simulations

## Hospital A — regional legacy hospital

### Day 0

IT discovers CareOS supports FHIR but their primary useful feed is HL7 v2.

**Correct outcome:** preflight blocks self-service instead of pretending it works.

They can still run synthetic clinician workflow while the bounded HL7 adapter task is evaluated.

### Week 1

No live dependency. Integration engineering learns real ADT/ORU semantics.

Outcome: first reusable HL7 compatibility profile, not one-off site glue.

## Hospital B — university hospital with FHIR/ISiK

### Day 0

Manifest + CapabilityStatement discovery + MPI discovery.

### Day 1–3

Deidentified sandbox, two FHIR sources, wrong-patient/outage tests.

### Day 4–5

Synthetic clinician study with real workflow structure.

Outcome: precise list of what blocks shadow mode.

## Hospital C — hospital group

### Site 1

Adapter/version profile established.

### Site 2

Same product/version combination selected automatically.

Conformance runs with site-specific identity/network configuration.

Outcome metric: **how many engineering hours did Site 2 avoid because Site 1 existed?**

That is the infrastructure flywheel.

---

# 21. "It was always there" UX acceptance criteria

CareOS should fail UX review if the user must routinely:

- log in twice;
- search the patient twice;
- manually copy identifiers;
- choose the source system before asking a normal clinical question;
- understand FHIR/HL7 terminology;
- read a full AI disclaimer every interaction;
- re-enter information already known by an authorised source;
- guess whether information is stale;
- open a chatbot to find basic current context;
- learn a separate mental model for every module.

Target:

```text
patient context follows the user
role follows identity
important change follows workflow
source follows the fact
help follows confusion
```

---

# 22. Never let the user feel trapped

Every interface should offer:

```text
why am I seeing this?
show source
show history/change
flag incorrect
what is pending/unavailable?
what will happen if I click this?
undo/rollback where meaningful
get human help
```

The assistant should explain the product itself, but **product-support AI and clinical AI must remain distinct roles/permissions**.

A user question such as "why is this result red?" should not require a support ticket.

A question such as "should I change the treatment?" must not be routed through a product-help agent pretending to be clinical decision support.
