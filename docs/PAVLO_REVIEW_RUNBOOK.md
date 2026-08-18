# CareOS → Pavlo / Recare Review Runbook

Baseline: **18 August 2026**

Purpose: make the conversation useful even if there are only 90 seconds, and make every deeper claim easy to inspect rather than oversell.

## The posture

Do **not** pitch CareOS as a product Recare should adopt.

Use this frame:

> I independently converged toward many of the problems Recare already solves in production. I pushed especially hard on source state/provenance, bounded agent authority, failure/recovery behavior, workflow evidence and repeatable integration. I want to learn which ideas survive your real architecture, which you already solve better, and which assumptions I should delete.

The desired outcome is not approval of CareOS. It is a technically serious discussion and a better map of production reality.

---

# 90 seconds

## 0–20s — problem

> My north star is simple: return time to care without making clinical information less trustworthy. My partner is a physician, so I started from the time lost reconstructing context and documenting across fragmented systems.

## 20–50s — proof

Open:

`https://mikelninh.github.io/recare/`

Show:

1. source-linked clinical context;
2. pending stays pending;
3. contradiction remains visible;
4. documented therapy is not an AI recommendation;
5. agent draft remains human-reviewed.

## 50–70s — break it

Run one failure case:

- wrong patient; or
- source unavailable; or
- unauthorised write.

Point:

> The interesting part to me is not whether the model says no. It is whether deterministic identity/tool/effect boundaries make the unsafe action impossible even if the worker is bad.

## 70–90s — bridge to Recare

> Then I realised Recare is already operating much of the product layer I was independently converging toward. I don't want to build a parallel stack. I'm most interested in which of these reliability/integration ideas survive your real hospitals and where I could help implement them.

Stop talking. Ask a question.

---

# Five-minute path

### 1. Recare work sample

`https://mikelninh.github.io/recare/`

Question it answers:

> Can I build and reason about a bounded agentic clinical workflow?

### 2. Golden end-to-end journey

`https://mikelninh.github.io/careos/journey.html`

Question it answers:

> What happens when the source changes while the AI-derived work is already downstream?

Show:

```text
preliminary result
→ source-dependent draft
→ outage
→ corrected/final result
→ recovery
→ supersession
→ stale draft reopened
→ audit
→ patient view
→ follow-up lifecycle
```

### 3. One infrastructure idea

Open README or `docs/HOSPITAL_SCALE_FOUNDATION.md`.

Show only one flywheel:

```text
hospital capability manifest
→ adapter/version evidence
→ conformance
→ shadow/canary
→ compatibility knowledge
→ regression
→ next compatible hospital gets easier
```

Then ask:

> How much of Recare integration today is already configuration/conformance versus custom engineering, and where does that model break down?

---

# Fifteen-minute technical path

Use only if Pavlo wants to go deeper.

1. `README.md` — orientation + claim boundary.
2. `docs/RECARE_COLLABORATION_MAP.md` — overlap without claiming internal gaps.
3. `app/end_to_end_journey.py` — composed regression path.
4. `app/agent_tool_proxy.py` / agent policy — deterministic authority.
5. `app/patient_id_resolver.py` — no fuzzy/model patient matching.
6. `app/rollout_control.py` — evidence-gated promotion/rollback.
7. `app/compatibility_registry.py` — reuse without auto-approval.
8. `docs/GATES.md` — show what is deliberately still blocked.
9. `docs/CURRENT_STATUS_AND_GAPS.md` — strongest evidence that the project is not hiding its weaknesses.

---

# Questions to ask Pavlo

Do not ask all of these. Pick the thread he reacts to.

## Integration architecture

- Do you already have an internal adapter SDK or equivalent reusable integration abstraction?
- How much of a new hospital is configuration versus custom engineering today?
- How do you represent vendor/product/version compatibility and known deviations?
- Where do HL7/FHIR integrations actually hurt most: transport, identity, semantic mapping, lifecycle state, local workflow or operations?
- What normally determines time from signed hospital to first useful integrated workflow?
- Which integration task is repeated often enough that you most want to productise it?

## Clinical state / provenance

- How do you normalise preliminary/final/corrected/cancelled/pending states across heterogeneous KIS/LIS/document sources?
- What is your hardest real case where unavailable or pending data can look like absence?
- How does source provenance survive through Patient Overview / Agent / Docs into human review?
- When sources conflict, where is the resolution represented and who owns it?

## Agents

- Where does model authority end in the production architecture?
- How are patient/task/tool scopes enforced outside the model?
- Which agent failure has taught the team the most so far?
- What do you replay in evals after an integration/model/prompt/tool change?

## Rollout / operations

- How do vendor/KIS upgrades get regression-tested before broad rollout?
- What can one hospital/site kill locally without waiting for a shared control plane?
- What production failure is much harder than it looks from outside?

## Team / role

- If I joined, where would you want an AI engineer to spend time with interoperability/implementation rather than only model code?
- What is the highest-leverage problem I could own end to end in the first 60–90 days?
- Which part of CareOS would you tell me to delete immediately after seeing Recare's real architecture?

That last question is intentionally strong.

---

# Hard questions Pavlo may ask us

## “How much of this is real?”

Answer:

> The public clinical flows, agent containment, failure/recovery, install/identity/rollout contracts and tests are runnable synthetic/pre-hospital work. I have no real KIS/LIS deployment, production PHI operation or clinical validation, and I don't present it as if I do.

## “Why did you build a Patient Overview if Recare already has one?”

> I started from the problem independently and later realised the overlap was much larger than I thought. That made Recare more interesting. I now treat the UI as a research/reference surface; I am more interested in the underlying correctness/eval/integration principles than preserving a competing product.

## “Do you actually know hospital interoperability?”

> Not at production depth yet. I know the standards/architecture well enough to build a falsifiable integration model, but real vendor behavior is a deliberate open gate. That is exactly why I want production critique rather than claiming expertise I haven't earned.

## “Your clinical-truth benchmark is weak.”

> Correct. The frozen synthetic holdout has high precision/provenance but only 26.32% recall and 100% review burden. I keep G1 blocked because review-everything is not a useful product. The next work is a fresh development corpus and real user behavior—not tuning the holdout until it looks pretty.

## “Why so much safety architecture for a read-only prototype?”

> Because the cost of changing the authority model after applications and workflows depend on it is much higher. But I am happy to simplify any mechanism that production reality shows is unnecessary.

## “What if Recare already has all of this?”

> Great. Then CareOS did its job as a learning artifact. I would discard the duplicate implementation and work on the real unsolved problem.

## “What is the actual product?”

> The first product hypothesis is intentionally narrow: five-second orientation around changed/pending/conflicting source-linked context plus a reviewable draft for one high-friction workflow. The larger interoperability fabric is the endgame, not the initial sales pitch.

---

# What we should never say

Avoid:

- “CareOS is production ready.”
- “CareOS solves hospital interoperability.”
- “We support HL7 in production.”
- “This saves 20–30 minutes.”
- “Recare is missing X.”
- “Our architecture is 10/10.”
- “Agents cannot fail.”
- “Hospitals can self-install CareOS today.”
- “This is clinically validated.”

Prefer:

- implemented synthetically;
- contract / reference implementation;
- target to test;
- external evidence required;
- production hypothesis;
- I want your criticism.

---

# The one sentence to remember

> **I don't want to prove CareOS right. I want to find the production problem where this way of thinking is useful.**

That is the conversation.