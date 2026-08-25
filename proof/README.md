# CareOS Real-World Proof Sprint 1

Status: **pre-hospital external-evidence campaign**. No identifiable patient data. No clinical-use claim.

## Goal

Move CareOS from a strong synthetic/runnable prototype to **independently inspectable real-world evidence**.

We do not win by adding features. We win when a skeptical outsider can inspect an evidence trail and say exactly which claims survived reality, which failed, and why.

## Proof ladder

1. **Real clinicians on synthetic cases** — observed behavior, not opinions.
2. **Independent clinical/safety/privacy/security critique** — named role, explicit findings, corrections.
3. **Real hospital capability manifest** — systems/vendor versions/interfaces/identity/owners, no secrets or PHI.
4. **Approved vendor/deidentified sandbox** — actual FHIR/ISiK/HL7 behavior and measured integration effort.
5. **Governed shadow workflow** — CareOS runs without influencing care; compare against normal work.
6. **Bounded read-only pilot** — only after institutional approvals and stop/rollback criteria.
7. **Second site/vendor** — test whether knowledge is reusable rather than bespoke consulting.

## Sprint-1 graduation

Sprint 1 is complete only when all of these exist:

- >= 5 complete safe paired clinician sessions for one workflow family;
- observed baseline and CareOS timings, errors, source checks and effort;
- zero hidden safety-stop events in any result presented as positive;
- at least 3 independent reviewer perspectives (clinical/safety, privacy/security, hospital IT/integration);
- one real non-secret hospital capability manifest completed with hospital staff;
- every finding entered in `proof/EVIDENCE_LEDGER.yaml` as **supported / falsified / blocked / unknown**;
- at least one assumption is corrected or falsified. If nothing changes, the test was probably too friendly.

## First bounded workflow

**Physician morning review + documentation preparation.**

The question is not “Do you like CareOS?”

> Can a clinician reconstruct changed/pending/critical context and prepare the bounded documentation task faster or with less friction **without more errors or verification collapse**?

Use the existing `docs/TIME_RETURNED_TO_CARE_STUDY.md`, `CLINICIAN_TEST.md` and study runner. This directory adds the external-evidence discipline around them.

## Evidence rules

- Synthetic cases stay synthetic.
- Participants receive pseudonymous codes; do not store names in exported study records.
- “Uploaded” / “submitted” / “reviewed” are not automatically “verified”.
- Negative results stay visible.
- Unknown timing stays unknown.
- Reviewer comments are evidence, not approvals.
- A hospital manifest is not permission to access systems.
- A sandbox result is not production compatibility.
- A shadow result is not clinical validation.

## OpenAction role

Use OpenAction as the adoption/evidence coordination layer for the pilot:

`claim -> required evidence -> owner -> verifier -> status -> next unlock`

CareOS remains the clinical product and source-linked workflow layer. OpenAction tracks why the next real-world step is or is not justified.

## Immediate sequence

1. Run facilitator dry-run; delete dummy evidence afterwards.
2. Recruit first 5–10 clinicians for synthetic paired sessions.
3. Freeze the preregistration before participant #1.
4. Run sessions and export machine-readable observations.
5. Aggregate without hiding individual pairs.
6. Conduct external reviewer workshop using `INDEPENDENT_REVIEW_PACKET.md`.
7. Complete one hospital discovery workshop using `HOSPITAL_DISCOVERY_WORKSHOP.md`.
8. Decide: **advance / redesign / stop**.
