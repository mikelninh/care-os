# CareOS Critical-Service Game Day

Status: **synthetic / pre-production operations exercise**. Passing this exercise is not a substitute for a target-hospital disaster/downtime test.

## Goal

Practice the human + technical response to failures before a hospital is allowed to depend on CareOS.

The exercise tests whether the team can answer quickly:

1. What capability failed?
2. Is authoritative/legacy care still available?
3. What must users do now?
4. What scope is affected?
5. Which narrow kill/rollback action is safest?
6. What evidence is required before recovery/promotion?

## Roles

Assign explicit people before starting:

- incident commander;
- platform/SRE responder;
- interoperability responder;
- security/privacy escalation;
- clinical-safety escalation;
- hospital communication owner;
- rollback/release owner;
- observer/scribe.

One person may cover multiple roles in a small synthetic drill. Responsibilities must still be explicit.

## Inputs

Use only synthetic/deidentified environments.

Capture:

- deployment/release identifier;
- hospital/site profile;
- adapter versions;
- model/agent/tool versions where applicable;
- start time;
- initial normal health snapshot;
- rollback artifact/reference;
- legacy fallback path.

## Scenario A — model provider unavailable

Inject: model endpoint fails while source context remains healthy.

Expected:

- C0/C1 source-linked context remains available;
- model/agent assistance visibly unavailable;
- no silent model swap;
- no write/send capability appears;
- incident classified below a C1 context outage if no other risk exists;
- users are told they may continue with source-linked context.

## Scenario B — LIS/FHIR source unavailable

Inject: one clinical source cannot be refreshed.

Expected:

- other admitted context may remain visible;
- failed source named;
- completeness/freshness warning visible;
- absence conclusions dependent on the source disabled;
- legacy/source fallback instruction available;
- agent claims depending on the missing source suppressed.

## Scenario C — identity service unavailable

Expected:

- no patient guessing/fuzzy remap;
- new agent/consequential sessions disabled;
- current permitted read-only context follows the explicit policy;
- hospital is told how to continue through the authoritative workflow.

## Scenario D — corrected result arrives during outage

Flow:

```text
network/source outage
→ result v1 is last known
→ source publishes corrected v2 while CareOS cannot refresh
→ connectivity returns
→ CareOS enters RECOVERY, not NORMAL
→ versions/events reconcile
→ v2 supersedes v1
→ graph identifies dependent derived artifact
→ unsigned AI draft becomes review-required
→ signed human record is not silently rewritten
→ invalidation is audited
→ only then can the context return to NORMAL
```

This scenario is represented in `app/recovery_reconciliation.py` and `tests/test_recovery_reconciliation.py`.

## Scenario E — wrong-patient / authority risk

Inject a condition suggesting patient isolation or action authority may be compromised.

Expected:

- classify as systemic safety incident (SEV0 baseline);
- contain before optimizing availability;
- use the narrowest safe kill scopes (agent/tool/workflow/site/release as appropriate);
- affected hospital(s) receive direct instruction;
- preserve evidence/audit;
- no automatic re-enable.

## Scenario F — bad adapter/release across more than one site

Expected:

- stop wider fleet promotion;
- affected adapter/release can be killed without disabling unrelated source truth;
- known-good version remains available;
- compatibility/conformance fixture is created from the failure;
- second site is protected from the same known defect before re-promotion.

## Exercise evidence

Record for every scenario:

- detection source/time;
- classification;
- affected capability/site scope;
- first safe user instruction;
- selected kill/rollback scope;
- time to containment (exercise measurement, not SLA claim);
- evidence inspected;
- recovery criteria;
- recovery decision;
- regression/runbook changes;
- unresolved risks.

## Pass criteria

A synthetic game day passes only if:

- authoritative/legacy fallback is clear;
- outage does not become false clinical absence;
- no hidden clinical write/send is queued;
- patient/authority uncertainty fails closed;
- recovery requires reconciliation where relevant;
- rollback/kill ownership is explicit;
- hospital communication says what failed, what still works and what to do;
- at least one reusable regression/runbook lesson is captured for each meaningful injected failure.

## Production gate

Before a contractual critical-service SLA, repeat relevant exercises in the approved target environment with the actual hospital, identity, networking, audit, KIS/LIS dependencies, on-call organisation and contractual responsibilities.
