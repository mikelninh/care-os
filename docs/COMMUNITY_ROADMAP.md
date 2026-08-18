# CareOS Community Roadmap

> **Many people can improve healthcare. The repository should make it obvious where to help.**

This roadmap is for contributors who want a useful, bounded problem instead of a giant “build healthcare AI” brief.

CareOS is still synthetic / pre-hospital research. The roadmap therefore prioritises work that can be proven without identifiable patient data.

## How to choose work

Pick the smallest problem that produces real evidence.

Prefer:

> **one failure → one fix → one regression test**

or:

> **one workflow pain → one UX improvement → one measurable outcome**

over broad speculative feature expansion.

---

# 🟢 Starter — a few hours

Good for first-time contributors.

### Accessibility pass

- keyboard navigation through clinician case tabs;
- visible focus states across synthetic demos;
- screen-reader labels for status / source controls;
- reduced-motion checks;
- contrast / zoom regression checks.

**Proof:** automated/manual accessibility checklist + screenshots where useful.

### Mobile / legacy viewport fixtures

- test 320 / 360 / 390 px widths;
- low-height laptop / Citrix-style viewport;
- long German clinical strings;
- tab overflow / status-chip collision;
- large text / browser zoom.

**Proof:** screenshots or Playwright-style layout assertions if introduced.

### Better degraded-state copy

Create concise user-facing states for:

- source unavailable;
- partial read;
- stale source;
- pending result;
- contradictory source;
- unauthorised action.

**Proof:** fixture + UI state + regression test.

### Synthetic fixture expansion

Add clearly synthetic cases for:

- corrected lab result;
- cancelled order;
- duplicate observation;
- delayed result;
- contradictory medication list;
- document with malicious instruction text.

**Proof:** fixture + expected truth/state outcome.

---

# 🔵 Builder — 1–3 days

### Agent trace explorer

Build a clean local viewer for:

```text
run_id
model + prompt version
tool proposal
policy decision
tool latency
evidence IDs
draft result
eval result
human correction
```

**Why:** make agent failure review dramatically faster.

### Clinician study report UI

Take anonymous paired-study exports and render:

- paired task-time deltas;
- errors;
- pending-work misses;
- source opens;
- acceptance without verification;
- safety-stop events;
- honest sample-size limitations.

**Rule:** never imply clinical validation.

### Synthetic connector sandbox

Implement a small fake hospital source with realistic:

- paging;
- latency;
- outages;
- stale state;
- wrong-patient resource;
- corrected data.

Then run CareOS against it.

### Error-budget / SLO simulator

Simulate connector latency and availability to explore what clinician UX should do under degraded conditions.

---

# 🟣 Interoperability — 2–7 days

### IPS conformance path

- export a synthetic CareOS summary to International Patient Summary;
- validate against the chosen IPS IG;
- document fields that cannot safely round-trip;
- keep original clinical text and source state.

### Berlin → another country fixture

Extend the existing portability work with another synthetic country pack.

Acceptance criteria:

- `pending` remains pending;
- contradiction remains contradiction;
- original wording remains available;
- translation is presentation metadata, not source mutation;
- issuer trust is independent from FHIR validity.

### Terminology mapping provenance

Add mapping metadata:

```text
source code/system/version
mapped code/system/version
mapping method
mapping version
review state
```

### ISiK / FHIR adversarial fixtures

Add cases for:

- partial bundle;
- duplicate resource;
- late page failure;
- corrected resource;
- patient reference mismatch;
- unexpected extension;
- unsupported profile version.

---

# 🔴 Security / reliability — 2–7 days

### Agent capability fuzzing

Generate malformed / adversarial tool proposals against the deterministic Agent Gateway.

Test:

- unknown tool;
- extra patient field;
- hidden write intent;
- oversized page request;
- recursion attempt;
- egress request;
- schema-smuggling field;
- stale delegation.

### Prompt-injection corpus

Create a synthetic corpus of hostile clinical documents:

- “ignore policy” text;
- fake system-message formatting;
- tool-call instructions;
- encoded instruction strings;
- misleading authority labels;
- mixed clinical + malicious text.

Measure containment rather than model cleverness.

### Audit integrity test suite

Attempt:

- dropped event;
- reordered event;
- altered event payload;
- replayed event;
- missing actor identity;
- clock skew.

### Kill-switch exercise

Build a synthetic operational drill:

> compromised agent detected → revoke → confirm new calls fail → preserve audit → recover cleanly.

---

# 🟠 Evaluation / ML — 3–10 days

### Recall vs review-burden frontier

CareOS currently has very high synthetic precision but low recall.

Build analysis that plots candidate extraction configurations against:

```text
precision
recall
review-case rate
unsupported claims
critical silent misses
```

Goal: understand the useful operating frontier rather than optimise one metric blindly.

### Abstention / calibration eval

Test when a model should:

- propose;
- ask for review;
- abstain;
- block.

### Agent regression benchmark

Create a frozen synthetic suite that tests:

- grounding;
- pending retention;
- contradiction retention;
- recommendation confusion;
- patient scope;
- tool policy;
- degraded-source handling.

### Study power / uncertainty tooling

For formative clinician studies, report uncertainty honestly for small N rather than overstating effects.

---

# 🎨 Product / design — 1–7 days

### “Five seconds to orient” clinician test

Test whether a clinician can answer quickly:

- what needs attention now?
- what is pending?
- what is contradictory?
- where did this fact come from?
- what did the agent do vs the source say?

### Low-click source verification

Prototype faster evidence inspection without turning the interface into citation clutter.

### Shift-handover mode

Explore a view optimised specifically for:

- unresolved items;
- changes since last review;
- source uncertainty;
- next-human ownership.

### Calm failure UX

Make safety failures understandable without alarming users unnecessarily or hiding seriousness.

---

# 🌍 Global health — 3–14 days

### Country-pack contract

Define a stable plugin interface separating:

```text
core truth semantics
core agent safety
global portability
        ↓
country identity / terminology / law / national services
```

### Low-bandwidth portable summary

Create a human-readable minimal summary that remains useful when a receiving setting cannot run the full stack.

### Trust / issuer verification prototype

Experiment with a synthetic signed portable summary where:

- FHIR validity;
- document signature;
- issuer trust;
- revocation;
- receiving policy

remain distinct states.

---

# 🏥 Work that requires a real hospital partner

These are important but should **not** be simulated into fake claims:

- real KIS / LIS integration;
- hospital SSO / treatment-context launch;
- production KMS / SIEM / DLP;
- DSFA / DPO review;
- protected audit deployment;
- target-environment load / recovery;
- live clinician workflow study;
- shadow deployment;
- limited live read-only use;
- second-hospital repeatability.

These require permission, governance and real infrastructure.

---

# Contribution quality bar

A contribution does not need to be huge.

It should be **specific, testable and honest**.

Strong:

> “Added wrong-patient rejection for paginated FHIR page 2, with regression test.”

Weak:

> “Improved AI safety.”

Strong:

> “Reduced mobile source-verification interaction from four taps to two in the synthetic workflow.”

Weak:

> “Improved UX.”

Strong:

> “IPS export preserves pending state in Berlin→Hanoi round-trip fixture.”

Weak:

> “Added global interoperability.”

---

# The invitation

You do not need permission to care about this problem.

You do not need to be a healthcare veteran to contribute a careful test, a better interaction, a safer API boundary or a cleaner interoperability fixture.

And you do not need to know everything before starting.

> **Find one piece of friction or one way the system can fail. Make it better. Show the evidence.**

That is enough to move the mission forward.
