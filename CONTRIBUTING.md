# Contributing to CareOS

> **We are all in this together.**

CareOS exists to explore one question:

> **Can we return time to care without making clinical information less trustworthy?**

This is not a closed product exercise. Healthcare is too important, too complicated and too interconnected for one person or one team to solve well.

If you are a software engineer, clinician, interoperability specialist, security engineer, designer, researcher, data scientist, product thinker or simply someone who has lived through painful healthcare workflows: **you are welcome here.**

## Before anything else

CareOS is currently **synthetic / pre-hospital research only**.

Please do **not** submit:

- identifiable patient data;
- screenshots or exports containing PHI;
- real credentials, API keys or hospital secrets;
- proprietary hospital/vendor material you are not authorised to share;
- code that silently weakens patient binding, provenance, review or write restrictions.

If a contribution needs real healthcare data to be useful, design the interface with synthetic fixtures first.

## The contribution contract

A good CareOS contribution should make at least one of these better:

1. **Time returned to care**
2. **Clinical correctness / provenance**
3. **Interoperability**
4. **Agent containment / safety**
5. **Observability / evaluation**
6. **Hospital implementation**
7. **Accessibility / clinician UX**
8. **Cross-border portability**

And it must not casually weaken these invariants:

- pending ≠ negative;
- unavailable ≠ absent;
- stale ≠ current;
- documented therapy ≠ AI recommendation;
- agent draft ≠ source truth;
- patient / encounter scope is authoritative outside the model;
- read permission does not imply write permission;
- source failure must fail visibly;
- consequential facts must remain traceable to evidence.

## Pick a lane

You do not need to understand the whole architecture before contributing.

### 🟢 Good first contributions

Useful for someone learning the repo:

- improve a synthetic fixture;
- add an edge-case regression test;
- improve accessibility / keyboard navigation;
- improve mobile behaviour;
- clarify error or degraded-state copy;
- add documentation examples;
- add a synthetic interoperability case;
- improve developer setup / local tooling.

### 🔵 Clinical workflow / UX

Help answer: **does this remove work or add another screen?**

Examples:

- reduce clicks / information hunting;
- improve source inspection;
- make pending / stale / contradictory states easier to scan;
- build better keyboard-first workflows;
- test low-resolution / legacy-browser layouts;
- improve paired clinician-study instrumentation.

### 🟣 Interoperability

Examples:

- FHIR / ISiK fixtures and validation;
- terminology / unit mapping provenance;
- IPS export / import validation;
- country-pack interfaces;
- synthetic KIS / LIS connector adapters;
- partial-read, paging and outage tests;
- cross-border round-trip tests.

### 🔴 Security / agent reliability

Examples:

- prompt-injection cases;
- wrong-patient / patient-switch races;
- delegated-tool abuse;
- resource exhaustion / recursion tests;
- audit-chain integrity;
- model-gateway hardening;
- write-escalation / egress abuse;
- red-team fixtures and replay tooling.

### 🟠 Evaluation / data science

Examples:

- agent-quality evals;
- clinician A/B statistics;
- verification-decay measures;
- calibration / abstention metrics;
- recall-review burden analysis;
- regression dashboards;
- reproducible synthetic benchmark tooling.

### 🌍 Global health / portability

Examples:

- International Patient Summary conformance;
- translation provenance;
- terminology mapping across countries;
- verifiable issuer / trust experiments;
- synthetic Germany ↔ another-country fixtures;
- low-bandwidth / offline rendering.

## Fast local setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.lock
uvicorn app.main:app --reload
```

Run tests:

```bash
pytest
```

Recare capstone:

```bash
uvicorn app.recare_api:app --reload --port 8010
```

Then inspect:

```text
GET  /health
GET  /api/capabilities
GET  /api/eval-suite
POST /api/run
```

## How to propose a change

Small, reviewable contributions are preferred.

A strong pull request explains:

```text
Problem
What real workflow / failure does this address?

Change
What did you add or change?

Evidence
Which test / fixture / screenshot / measurement demonstrates it?

Safety
Could this alter patient scope, provenance, clinical state, permissions or write behaviour?

Limitations
What does this still not prove?
```

If a change affects a clinical or safety invariant, add a regression test.

If you cannot write the test yet, open an issue and describe the failure precisely before building a large implementation.

## Design principles for contributors

### Prefer boring reliability over magical behaviour

A visible `SOURCE UNAVAILABLE` state is better than a fluent guess.

### Make uncertainty inspectable

Do not hide pending, contradictory, stale or unverified information behind a single confidence score.

### Keep authority outside the model

Models can interpret and propose. Patient scope, permissions, write authority and evidence requirements belong in deterministic controls.

### Integrate before replacing

FHIR / ISiK / HL7 / stable vendor interfaces first. CareOS should compose with existing systems rather than demand a giant migration.

### Measure workflow outcomes

A feature is not successful because it uses AI. Ask whether it saves time, reduces search/copy work and preserves verification.

### Fail visibly

Source outage, partial reads, policy denial and unsupported output should be understandable to both users and operators.

## Review standard

Not every contribution needs production-grade depth, but the claim must match the evidence.

Examples:

- synthetic test → say **synthetic test**;
- prototype → say **prototype**;
- architecture proposal → say **proposal**;
- formative clinician study → say **formative study**;
- production evidence → only after real production evidence exists.

We would rather publish an honest limitation than an inflated metric.

## Community behaviour

Be kind, specific and rigorous.

Critique the system, evidence and assumptions — not the person.

Healthcare brings together people from very different disciplines. Engineers will miss clinical context. Clinicians will not know every systems constraint. Security reviewers will deliberately break things. Designers will question the workflow. That tension is useful when it stays respectful.

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License and contribution terms

CareOS is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE).

Unless you explicitly state otherwise, a contribution intentionally submitted for inclusion in CareOS is provided under the same Apache-2.0 terms, consistent with section 5 of the license. You retain copyright in your original contribution.

If your employer or another party owns rights in work you want to contribute, make sure you are authorised to submit it.

Do not contribute third-party code, data, documents or assets unless their licence and provenance are compatible and clearly documented.

## Where to start

- [README](README.md) — 10-second project orientation
- [Community roadmap](docs/COMMUNITY_ROADMAP.md) — useful work grouped by difficulty
- [Current gaps](docs/CURRENT_STATUS_AND_GAPS.md) — what cannot be honestly claimed yet
- [Architecture V2](docs/ARCHITECTURE_V2.md) — deeper system model
- [Hospital rollout](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md) — how this meets reality

If you see a better way to return time to care safely, **show us.**
