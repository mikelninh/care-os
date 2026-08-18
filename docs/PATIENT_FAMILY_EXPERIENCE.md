# CareOS Patient & Family Experience

Status: **synthetic/pre-hospital product contract**. It does not claim live patient-portal integration, legal entitlement beyond connected infrastructure, or clinical advice.

## Purpose

Patients should not merely have access to documents. They should be able to understand:

- what happened;
- what changed;
- what is still pending;
- who owns the next step;
- what happens next;
- what medication changed;
- where the original source is;
- how to ask a question or flag a possible error.

The patient surface is generated from the same source-linked context as clinician workflows, but it has a different information hierarchy and authority model.

## Core invariants

1. **Plain language is presentation, not source mutation.**
2. **Pending/preliminary/unavailable remain explicit.**
3. **Original source wording remains accessible.**
4. **Medication display reports documented state; it is not AI prescribing.**
5. **A patient correction request does not silently rewrite the clinical record.**
6. **Family access uses explicit revocable delegation, not shared credentials.**
7. **No smartphone-only critical path.**

`app/patient_view.py` makes these rules machine-readable.

## Patient agent

Allowed first capabilities:

- explain jargon;
- translate presentation while preserving original wording;
- find the source/document;
- prepare questions for the care team.

The agent must distinguish:

```text
source record
≠ clinician plan
≠ AI explanation
```

It does not create a new diagnosis/treatment truth.

## Proxy / family access

`ProxyGrant` is a dedicated revocable policy object with patient, proxy, scopes and optional expiry.

A future production implementation must bind this to the governing national/provider identity and authorization mechanisms. CareOS must not invent a parallel legal authority system.

## Understanding is the outcome

Do not optimize only for portal visits or chat messages.

Use teach-back questions:

1. What are we still waiting for, and who owns the next step?
2. What medication changed, if anything?
3. What happens next after discharge/this visit?

Measure:

- correct understanding;
- pending-state understanding;
- medication-change understanding;
- follow-up ownership understanding;
- source-location success;
- false reassurance/confidence errors;
- accessibility/friction.

## Synthetic public experience

`https://mikelninh.github.io/careos/patient.html`

The page is synthetic and demonstrates:

- Today;
- Still pending;
- Medication;
- What happens next;
- Sources & access;
- bounded patient helper;
- teach-back.

## Next evidence step

Run a synthetic usability protocol with patients/families/lay users using no real patient data. A live patient-facing pilot requires provider governance, identity/access integration, privacy review and appropriate clinical/legal ownership.
