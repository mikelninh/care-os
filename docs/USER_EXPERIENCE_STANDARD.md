# CareOS User Experience Standard

Baseline: **18 August 2026**

> **A critical healthcare interface should reduce cognitive work, not relocate it.**

This standard applies to clinician, nursing, patient, operations and hospital-IT surfaces. It is a target design contract, not evidence that every current CareOS demo satisfies it.

---

# 1. Five-second orientation

On opening a patient/workflow, the intended user should be able to answer quickly:

1. Who is this?
2. What changed?
3. What needs attention?
4. What is pending/uncertain/conflicting?
5. Where did the consequential information come from?

If a screen cannot support those questions, adding more AI is lower priority than fixing hierarchy.

---

# 2. One job, one primary surface

Do not create a universal dashboard containing every available field.

Role surfaces should be purpose-limited:

- physician: clinical change + decision context + drafts;
- nursing: handover + care tasks + exceptions;
- pharmacy: medication reconciliation + relevant safety context;
- diagnostics: indication + prior context + lifecycle;
- discharge/case management: coordination + missing fields + status;
- patient: understandable timeline + next steps + access/share;
- IT: integration health + compatibility + conformance + rollout;
- security/privacy: data flow + authority + audit + unresolved risks.

Deep information remains reachable but does not compete with the primary job.

---

# 3. Information hierarchy

Default clinical hierarchy:

```text
patient identity / encounter
        ↓
NOW / NEEDS ATTENTION
        ↓
CHANGED
        ↓
PENDING / CONFLICT / STALE / UNAVAILABLE
        ↓
relevant current context
        ↓
work / draft / next human action
        ↓
source details / history
```

Do not let an AI summary occupy more visual authority than source state or patient identity.

---

# 4. Source verification must be cheap

Consequential content should provide source inspection in **one interaction where feasible**.

The source view should make it easy to identify:

- source system/document;
- original value/wording;
- effective/recorded time;
- source version;
- lifecycle state;
- relevant evidence span;
- mapping/translation where applicable.

Verification should not require navigating back through five source applications when CareOS already has a governed deep link/reference.

---

# 5. State must be understandable without a legend

Never rely on color alone.

Use explicit language/icons for:

- pending;
- preliminary;
- final;
- corrected;
- cancelled;
- stale;
- unavailable;
- contradictory;
- patient/encounter mismatch;
- agent draft;
- human confirmed.

The user should not need to know CareOS vocabulary to understand whether something is current or trustworthy.

---

# 6. No dead ends

Every failure state should answer:

```text
what failed?
what is still available?
what should I do now?
will retry help?
who/what owns the next step?
```

Bad:

> Error 500.

Better:

> Microbiology is temporarily unavailable. The last successful refresh was 14:08 and may be stale. Do not interpret missing results as negative. Open the LIS directly or continue with the rest of the patient context.

---

# 7. Progressive disclosure

Default view: calm and concise.

One interaction deeper: evidence, history, metadata.

Another layer: technical lineage/audit for authorised users.

Do not surface implementation internals to clinicians merely because engineers find them useful.

---

# 8. Corrections must be easy

For AI/derived output:

```text
accept
edit
reject
show source
why is this here?
report problem
```

A correction should create useful structured evidence for evaluation without punishing the user with a long form.

Never hide model errors through silent backend cleanup.

---

# 9. Agent UX

The in-product agent should feel like an excellent assistant who knows its boundaries.

It can answer product/workflow questions such as:

- “Why is this marked pending?”
- “Where did this result come from?”
- “Why can't I send this yet?”
- “What changed since yesterday?”
- “What do I need to fill before this referral is ready?”
- “What does this error mean?”

It must distinguish:

```text
SOURCE FACT
HUMAN PLAN
DERIVED CONTEXT
AI DRAFT / EXPLANATION
```

When asked a clinical question beyond its intended authority, route to evidence/approved clinical-support path or state the boundary. Never fake certainty merely to avoid user frustration.

---

# 10. Keyboard / workstation

For hospital desktop/Citrix use:

- keyboard reachable primary actions;
- predictable focus order;
- shortcut discovery, not memorisation requirement;
- no hover-only critical controls;
- strong zoom/large-text behavior;
- long German clinical strings tested;
- low-height laptop/Citrix viewport tested;
- no horizontal-scroll dependency for core work;
- loading should preserve context rather than jump layout.

---

# 11. Tablet / touch

- touch targets suitable for standing/rounds use;
- no dense tiny table as only view;
- important patient banner stays visible;
- clear current/previous patient transition;
- accidental taps on consequential actions require confirmation/undo where safe;
- source preview works without precision tapping;
- portrait and landscape supported where device fleet requires it.

---

# 12. Shared terminals

- previous patient/session never leaks into next user;
- logout/lock obvious and fast;
- patient switch is visually unmistakable;
- stale browser tab/session detected;
- re-auth for governed consequential operation;
- no local-download default for PHI;
- clipboard behavior considered in provider policy.

---

# 13. Patient experience

Patient language should answer human questions, not reproduce the clinician UI.

Default:

```text
What happened?
What changed?
What is still being checked?
What do I need to do?
Who is responsible for the next step?
When should I expect something?
Where is the original document?
Who can see my information?
How can I correct/ask/share?
```

Plain-language content:

- never replaces source wording;
- keeps uncertainty visible;
- separates AI explanation from clinician-authored plan;
- supports accessible language/translation;
- avoids alarmist risk wording without context.

---

# 14. Accessibility and inclusion

Minimum direction:

- WCAG-aligned web patterns;
- keyboard access;
- screen-reader semantic structure;
- non-color status;
- zoom/large text;
- reduced motion;
- high contrast;
- understandable language;
- multilingual presentation;
- no smartphone-only critical patient pathway;
- proxy/caregiver pathways;
- consider cognitive impairment and low digital literacy explicitly.

Accessibility regressions are product regressions.

---

# 15. Notification doctrine

Every notification must justify interruption.

Classify:

```text
FYI — no interruption
TASK — appears in work queue
TIME-SENSITIVE — bounded notification
CRITICAL — explicit clinical/provider-defined criteria only
```

AI must not invent urgency classification outside governed rules.

Measure alert burden and ignored/dismissed notifications. More alerts can be worse than less context.

---

# 16. Latency doctrine

Perceived speed matters, but not more than correctness.

Targets should vary by interaction:

- patient/identity/context shell: near-immediate from local/provider services where possible;
- source-linked orientation: fast enough not to trigger manual fallback;
- generative draft: can be slower and cancellable;
- background sync: must expose freshness rather than block UI indefinitely.

Never display a plausible old summary as if current merely to avoid a loading state.

---

# 17. Success test

The best UX outcome after adoption:

> **Users stop thinking about CareOS. They think about the patient and the work.**

The strongest sign of product pull is not a high “AI wow” score. It is that returning to the old workflow feels unnecessarily difficult.
