# Synthetic Before → After Cases

Baseline: **18 August 2026**

> These are inspiration / evaluation designs. They are **not measured CareOS outcomes** and must never be presented as clinical efficacy evidence.

Each case contains:

```text
before workflow
future CareOS workflow
agent role
potential time return
possible patient-impact pathway
failure modes
proof / falsification plan
```

---

# Case 1 — Infectiology morning review

## Before

A physician reviews a complex inpatient:

```text
KIS patient page
→ last progress note
→ medication screen
→ lab
→ microbiology
→ radiology report
→ scanned outside letter
→ infection-control note
→ one call to clarify an unresolved result
→ mentally reconstruct timeline
→ write progress note
```

Synthetic baseline hypothesis: **18 minutes for one complex review**.

## After target

KIS launches CareOS in the same patient/encounter context.

```text
CHANGED
- blood culture status changed preliminary → final
- CRP / renal trend changed
- documented therapy changed

PENDING
- second culture not final
- consult not completed

REVIEW
- allergy statement conflicts between two sources

WORK
- source-linked progress-note draft
```

Physician opens two important sources, edits the draft and approves their own note.

Synthetic target: **6 minutes**.

Potential return: **12 minutes / complex case**.

## Agent role

- compare source-linked state over time;
- identify changed/pending items;
- prepare timeline;
- prepare progress-note draft;
- never decide antibiotic treatment.

## Possible patient-impact pathway

```text
less search burden
→ more reliable visibility of newly finalised / pending information
→ fewer delayed reviews of relevant changes
→ potentially earlier human response
```

This is a plausible mechanism, **not a proven outcome**.

## Failure modes

- preliminary shown as final;
- missing source interpreted as negative;
- wrong patient context;
- draft implies treatment recommendation;
- physician stops opening important sources.

## Proof

Paired study / shadow metrics:

- review time;
- correct answers;
- missed pending items;
- source opens;
- corrections;
- treatment-recommendation misread;
- wrong-patient events;
- newly finalised result detection latency.

Falsify the workflow if speed improves but pending-item detection or source verification worsens.

---

# Case 2 — Nursing shift handover

## Before

```text
read free-text nursing notes
review order/medication changes
review isolation/infection-control information
check separate task list
ask outgoing nurse what changed
write own notes/tasks
```

Synthetic target baseline across a selected patient set: **22 minutes**.

## After target

Role-specific delta:

```text
NEW / CHANGED
- isolation status
- mobility assistance
- medication/order changes

DO NEXT SHIFT
- timed task
- pending sample
- planned transport

REVIEW
- conflicting mobility documentation
```

Source is available behind each consequential item.

Synthetic target: **9 minutes**.

Potential return: **13 minutes per handover set**.

## Agent role

- extract tasks from approved plans;
- draft handover;
- group changes by urgency/time;
- never invent care tasks from unsupported context.

## Possible patient-impact pathway

```text
clearer changes + unresolved work
→ fewer handover omissions
→ more reliable continuity across shifts
```

## Proof

- time;
- omitted critical task count;
- duplicated task count;
- correction count;
- perceived effort;
- alert burden;
- source verification.

Fail if alert count or omission rate increases.

---

# Case 3 — Discharge / aftercare coordination

## Before

```text
identify aftercare need late
search chart for required facts
clarify with ward/doctor
copy information into referral
phone/fax providers
repeat missing information
track replies manually
update hospital record separately
```

Synthetic baseline: **60 minutes for one eligible case**.

## After target

```text
aftercare need visible earlier
→ minimum necessary patient context prepared from sources
→ missing fields explicit
→ approved structured request sent through existing network/rail
→ status replies structured
→ changed source fact triggers review of affected referral fields
→ documentation draft reused
```

Synthetic target: **30 minutes**.

Potential return: **30 minutes / case**.

Recare publicly reports a 30–60 minute-per-case saving for its Discharge product. That is useful external evidence that this workflow category can produce material time savings; it is not evidence for CareOS.

## Agent role

- prepare referral package;
- identify missing fields;
- summarise replies/status;
- prepare patient/family explanation;
- no autonomous placement decision.

## Possible patient-impact pathway

```text
earlier aftercare workflow
+ less coordination delay
→ potentially smoother transfer / fewer avoidable discharge delays
```

## Proof

- time to aftercare workflow start;
- staff minutes/case;
- outbound clarification calls;
- missing-information loops;
- time from medically ready → transition where causally appropriate;
- inappropriate data-sharing events.

---

# Case 4 — Hospital → GP / specialist continuity

## Before

Patient is discharged.

Later the practice may receive:

- discharge letter;
- KIM message/document;
- ePA material;
- patient-carried paper;
- patient verbal explanation.

The GP/specialist reconstructs what changed and which follow-up remains pending.

Synthetic baseline hypothesis: **15 minutes** of information reconstruction for a complex post-discharge contact.

## After target

The receiving practice gets a governed structured summary through national/standard rails:

```text
what happened
what changed in medication
what remains pending
what follow-up was requested
source documents
issuer / trust context
```

CareOS/PVS projection shows the change set without forcing the practice to use the hospital UI.

Synthetic target: **6 minutes**.

Potential return: **9 minutes / complex transition**.

## Possible patient-impact pathway

```text
clearer continuity
→ fewer lost follow-up tasks / repeated history reconstruction
→ potentially fewer duplicated tests / coordination delays
```

EHDS itself identifies better data exchange as a path to avoiding unnecessary duplicate tests; CareOS would need local prospective evidence for any product-specific effect.

## Proof

- reconstruction time;
- follow-up task completeness;
- medication discrepancy rate;
- duplicate-information requests;
- source trust/availability;
- practice adoption.

---

# Case 5 — Patient leaves hospital understanding the plan

## Before

Patient receives:

- verbal explanation under stress;
- dense discharge letter;
- medication changes that may be hard to compare;
- pending results that may be easy to forget;
- follow-up appointments/instructions spread across documents.

Later they or family call because they are uncertain.

## After target

Patient view:

```text
WHAT HAPPENED
plain-language summary, visibly generated from source record

MEDICATION CHANGES
old → current documented state + source

PENDING
what is not yet final + who owns follow-up

NEXT
appointments / GP / specialist / therapy / warning instructions as documented

QUESTIONS
patient agent helps prepare questions, not medical decisions
```

## Time target

Patient time is not the primary goal here.

Measure **understanding and coordination burden**.

## Possible patient-impact pathway

```text
better comprehension + visible pending/follow-up ownership
→ fewer misunderstandings and missed follow-up steps
→ potentially safer continuity
```

## Proof

- teach-back comprehension score;
- medication-change comprehension;
- pending-result awareness;
- follow-up recall;
- patient confidence;
- avoidable clarification contacts;
- correction/flag rate.

No claim about readmission/mortality without a properly designed outcome study.

---

# Case 6 — Newly finalised result after transfer / discharge

This is a safety-focused case where the value may be **attention reliability**, not raw time.

## Before

A result is pending when the patient changes ward or leaves hospital.

Later it becomes final.

Responsibility may depend on local workflow, inbox/task systems and handover quality.

## After target

```text
pending item is a first-class graph/task object
→ source changes preliminary/pending → final
→ deterministic routing policy identifies owning workflow/team
→ bounded agent prepares source-linked change summary
→ human acknowledges / acts in existing clinical process
→ audit records notification/acknowledgement
```

## Potential patient-impact pathway

```text
explicit ownership + lifecycle tracking
→ lower chance that finalisation disappears between handoffs
→ potentially faster human review of relevant late results
```

## Proof

- percentage of pending items with named owner;
- finalisation → acknowledgement latency;
- lost/unacknowledged item rate;
- false/duplicate notification rate;
- escalation burden;
- patient-safety review.

Do not build this as generic AI alerting. It must integrate with existing responsibility/workflow semantics and avoid alert fatigue.

---

# Evaluation rule across all cases

```text
TIME / CONVENIENCE
        +
CORRECTNESS
        +
PENDING / FAILURE STATE
        +
SOURCE VERIFICATION
        +
HUMAN CONTROL
        =
eligible for rollout discussion
```

A faster workflow with one important new safety failure is **not a win**.

CareOS encodes this principle in `app/time_returned_to_care.py`.
