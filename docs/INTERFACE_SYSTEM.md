# CareOS Interface System

Baseline: **18 August 2026**

> Goal: every user should feel unusually capable without needing to understand the underlying interoperability, AI or infrastructure complexity.

The interface must make **state, source, uncertainty and next action** obvious before it makes AI impressive.

---

# 1. Universal interaction grammar

Every CareOS surface should reuse the same small vocabulary:

```text
NOW       what is currently documented / relevant
CHANGED   what became new or different
PENDING   what is not complete/final yet
REVIEW    contradiction / uncertainty / human decision needed
NEXT      tasks / follow-up / workflow
SOURCE    where the item came from
HELP      why am I seeing this / what does this mean?
```

A user should learn this once across all modules.

---

# 2. Visual state must not rely on colour alone

Clinical state uses text/icon/shape + colour:

```text
● Final
◐ Preliminary
… Pending
↻ Corrected
! Contradiction
⏱ Stale
× Unavailable
? Unknown
```

Never use a green/red indicator without a readable state label.

---

# 3. Progressive disclosure

Default:

```text
important current context
changes
pending/review items
next work
```

One interaction deeper:

```text
full source
history
mapping lineage
raw/original value
related graph context
```

Do not show an engineer's provenance JSON to a clinician by default.

Do not hide provenance so deeply that it becomes practically inaccessible.

---

# 4. Patient context follows the user

Ideal clinical launch:

```text
KIS opens patient P / encounter E
        ↓
CareOS receives trusted launch context
        ↓
header visibly confirms identity
        ↓
no second patient search
```

The user should never manually paste a patient ID.

Patient switch:

- clears previous transient context;
- invalidates cached source mappings where required;
- cancels inappropriate in-flight agent/tool context;
- visibly confirms the new patient.

---

# 5. Physician home

Above the fold:

```text
PATIENT / ENCOUNTER

CHANGED SINCE LAST REVIEW        PENDING / REVIEW

NOW
problems · documented therapies · important trends

WORK
plan / tasks / drafts
```

Agent affordances are contextual:

```text
Summarise changes
Build timeline
Draft note
Explain discrepancy
Show supporting sources
```

Not a giant empty chat box.

---

# 6. Nursing home

Above the fold:

```text
SHIFT CHANGES
DO NEXT
OVERDUE / PENDING
CARE-RELEVANT EXCEPTIONS
```

Task completion does not silently change source clinical facts.

Voice capture may create a draft; user confirms before it becomes governed documentation.

---

# 7. Patient home

Language first, not coding first:

```text
Today
What changed
What is still waiting
What happens next
Medicines
Documents and sources
My access / privacy
Ask / flag possible error
```

Every AI explanation carries a clear presentation marker such as:

> **Plain-language explanation generated from the source record. It does not replace your clinician's advice.**

Avoid alarming "risk scores" without a validated clinical purpose and explanation path.

---

# 8. IT / operations home

No patient narrative by default.

```text
sites
sources
adapter versions
compatibility
identity
source health/freshness
latency/errors
release/policy/model versions
degraded workflows
rollback
```

Drill into patient-level trace only under governed operational need.

---

# 9. Help that follows confusion

Every important element should answer:

```text
What is this?
Why am I seeing it?
Where did it come from?
When was it last updated?
What can I do?
What happens if I do it?
Who can help if this looks wrong?
```

## Product-support agent

The product-help agent may explain:

- interface;
- source-state labels;
- how to find a feature;
- why a button is unavailable;
- how to report an issue.

It has **no clinical decision authority**.

## Clinical workflow agent

A separately authorised agent may use source-linked patient context under the clinical workflow's delegation.

Do not merge these identities merely because one chat UI is convenient.

---

# 10. Frustration budget

CareOS should track friction like reliability.

Examples:

```text
second login
second patient search
manual re-entry
unnecessary modal
unexplained disabled button
support ticket needed for normal task
slow response
lost draft
unexpected session expiry
repeated consent/context prompt
```

Target metric: **avoidable friction events per shift / workflow**.

A product can save five minutes in AI drafting and lose them again through authentication or navigation.

---

# 11. Performance UX

Targets for future production environments:

- shell responds immediately;
- skeleton/progressive states instead of frozen screens;
- source failure appears as source failure, not spinning forever;
- long agent work can be cancelled;
- draft work survives safe page navigation where policy permits;
- keyboard shortcuts for high-frequency workstation users;
- touch targets suitable for tablet/gloves where relevant;
- no animation required for understanding.

---

# 12. Old hardware / managed environments

Design target:

- evergreen browser where hospital permits;
- graceful older managed browser support agreed per deployment;
- no GPU;
- minimal client memory;
- low-bandwidth tolerant for core view;
- works behind hospital proxy/VDI architecture;
- accessible without browser extensions;
- no administrator installation for the normal user.

Exact compatibility becomes a tested hospital profile, not a marketing statement.

---

# 13. Accessibility

Target WCAG-aligned interaction design:

- keyboard navigable;
- visible focus;
- screen-reader semantics;
- colour not sole signal;
- scalable text;
- plain-language mode;
- reduced-motion support;
- readable contrast;
- touch-friendly tablet controls;
- avoid dense hover-only interactions.

Clinical urgency does not excuse inaccessible software.

---

# 14. Notification philosophy

Do not create one more noisy notification system.

A notification needs:

```text
owner
workflow
urgency
reason
source
expiry/resolution condition
acknowledgement semantics
escalation semantics
```

Default preference:

> put information in the workflow where the user will naturally encounter it.

Push/interrupt only when waiting would be meaningfully worse.

---

# 15. Correction UX

Users need a safe way to say "this is wrong".

Correction is not direct mutation of every upstream source.

```text
flag item
→ specify issue category
→ preserve original source/value
→ route to responsible workflow/source owner
→ track correction/reconciliation state
→ show resolution
```

Patient correction requests and clinician source corrections may have different legal/workflow paths but share the same transparency principle.

---

# 16. Trust cues

Trust should come from inspectability, not anthropomorphic confidence.

Good:

```text
Source: LIS · Observation/123
Final · 11:42
Changed from preliminary at 10:18
Viewed source
```

Bad:

```text
✨ AI confidence: 98%
```

unless that confidence has a validated, useful meaning for the specific workflow.

---

# 17. No-dark-pattern healthcare

Never:

- make the safer/manual option hard to find;
- preselect consequential approval;
- use urgency styling to push product adoption;
- hide source uncertainty to improve perceived simplicity;
- frame correction as user failure;
- make opt-out/offboarding deliberately painful;
- game clinicians into "AI engagement".

The interface serves care, not engagement metrics.

---

# 18. Super-user without configuration burden

CareOS should infer safe presentation from role/workflow context, while letting advanced users customise non-safety-critical layout/preferences.

Safe customisation:

- panel order;
- saved filters;
- keyboard shortcuts;
- preferred density;
- notification preferences within policy.

Not user-customisable without governance:

- patient identity policy;
- clinical lifecycle semantics;
- source trust;
- write authority;
- required safety banners;
- audit requirements.

---

# 19. UX proof

Before broad rollout measure:

```text
time to first useful action
training minutes
wrong-navigation events
second-search events
source-open behavior
correction flow completion
help requests
abandonment
perceived effort
safety comprehension
```

Target aspiration:

> **A new authorised user can complete the core role workflow safely after a 10–15 minute orientation using synthetic cases.**

If they require a manual to understand current/pending/source state, redesign the UI.
