# CareOS Pilot Measurement Protocol

Goal: determine whether CareOS returns meaningful clinician time **without increasing correction, safety risk or cognitive burden**.

This is a product/health-services evaluation protocol skeleton, not a substitute for ethics/data-protection/research review where such review is required.

## Primary hypothesis

For defined clinical information-retrieval/documentation tasks, CareOS reduces task time and interaction burden while maintaining an acceptable safety/correction profile.

## Pilot progression

### Phase A — synthetic usability
5–10 clinicians, synthetic cases, no patient data.

Measure comprehension, workflow fit, source trust and obvious failure modes.

### Phase B — controlled realistic/de-identified evaluation
Use governed cases and compare CareOS with the normal source-system workflow where permitted.

### Phase C — read-only live-data pilot
Only after G0–G5 pass and local approvals.

## Core task metrics

Per task record:

- baseline completion time;
- CareOS completion time;
- success/failure;
- clicks;
- manual searches;
- phone calls/faxes/manual chases;
- corrections;
- source openings;
- review/uncertainty actions;
- cognitive-effort rating;
- clinician confidence/trust rating;
- whether participant would use again.

## Safety / truth metrics

These are release metrics, not vanity metrics:

- wrong-patient attachment rate;
- provenance coverage;
- unsupported-claim rate;
- wrong-source attribution rate;
- critical silent contradiction miss rate;
- stale-data misrepresentation rate;
- false-alert/review burden;
- correction rate by field/workflow;
- unresolved uncertainty surfaced vs hidden.

## Reliability metrics

- source availability;
- CareOS availability;
- refresh latency;
- stale-data duration;
- connector failure rate;
- degraded-mode frequency;
- time to detect/recover incidents.

## National-impact translation

Only after a verified per-clinician time saving exists may it be multiplied by an eligible user population. National estimates must report:

- measured saving and confidence interval;
- adoption assumption;
- eligible clinician/workflow population;
- working-day assumption;
- implementation/maintenance costs;
- sensitivity range;
- explicit statement that extrapolation is a scenario, not observed national impact.

## Stop criteria

The pilot stops or pauses on predefined events including:

- wrong-patient information;
- unsupported safety-critical claim;
- material authorization/privacy incident;
- source outage represented as current/complete;
- critical contradiction hidden by CareOS;
- correction/safety burden exceeding agreed threshold;
- clinical owner requests stop.

## Decision framework

A good pilot result is not "people liked the UI".

Advance only if there is evidence that:

1. clinicians finish target tasks materially faster/easier;
2. source/provenance remains inspectable;
3. safety-critical miss/correction metrics meet the predefined bar;
4. review/alert burden does not erase the benefit;
5. integration does not add duplicate login/patient search/documentation work;
6. IT/security/privacy operating burden is acceptable.
