# Time Returned to Care — Cross-Role Study Protocol

Status: **synthetic workflow evaluation protocol**. This is not clinical efficacy validation and does not authorize live patient-data research.

## Question

> Can CareOS reduce the time and friction required to complete a bounded healthcare workflow **without increasing safety errors or reducing source verification?**

## Roles / first three workflows

### Physician — morning review + documentation preparation
Baseline task: reconstruct the synthetic patient from the provided KIS/LIS/document surfaces, identify changed/pending information and prepare the required structured note fields.

CareOS task: complete the matched task using the source-linked context surface.

Product target to test: **20–30 minutes returned per affected shift workflow**, not assumed.

### Nursing — handover
Baseline task: reconstruct shift changes, pending work and care-relevant exceptions across the provided synthetic sources and prepare handover.

CareOS task: complete the matched handover using the role-specific changed/pending/work view.

Product target to test: **10–15 minutes returned per affected shift workflow**, not assumed.

### Discharge / case management — coordination preparation
Baseline task: identify required aftercare context, missing information and prepare a synthetic referral/coordination package.

CareOS task: complete the matched preparation using source-linked context and missing-field support.

Product target to test: **15–20 minutes returned per eligible case**, not assumed.

## Design

Use paired observations. Each participant gets the baseline and CareOS condition for the same workflow family with different synthetic case variants.

Counterbalance order where feasible:

- odd participant codes: baseline → CareOS;
- even participant codes: CareOS → baseline.

Do not collect names. Use pseudonymous participant codes. Do not include real patient data or free-text clinical data in exported metrics.

## Capture

`app/time_returned_to_care.py` defines the machine-readable observation contract:

- elapsed task seconds;
- systems opened;
- searches;
- context switches;
- copy/paste actions;
- clarification contacts;
- wrong answers;
- missed pending items;
- source opens;
- corrections;
- accepted-without-source-check events;
- cognitive effort 1–5;
- bounded friction tags;
- explicit safety stops.

## Safety stops

A speed improvement is not a product win if the CareOS condition produces:

- wrong patient;
- more missed pending work;
- unsupported claim;
- stale-as-current interpretation;
- draft-as-recommendation confusion;
- verification collapse.

Safety stops override time savings.

## Evidence threshold

Do not highlight a directional aggregate for a role before:

1. **≥5 complete safe pairs** for that role/workflow family;
2. zero observed safety-stop events in the highlighted set;
3. no detected verification collapse;
4. individual-pair distribution remains visible, not only the average/median.

This is a minimum threshold for a synthetic directional result, **not** a claim of clinical effectiveness.

## Aggregation

```bash
python scripts/aggregate_time_returned_to_care.py study-export.json --json-out report.json
```

The aggregator refuses to mark a role aggregate publishable when the minimum pair threshold or safety gate is not met.

## What happens after a synthetic result

Synthetic success permits the next question only:

> Is this worth taking into a governed real-workflow study?

A real hospital study requires the accountable institution, clinicians, privacy/data-protection review, study design appropriate to the intended claim, real workflow baselines and explicit stop criteria.

## Product rule

If the workflow cannot return meaningful time without increasing verification burden or errors, **change the workflow/product hypothesis**. Do not optimize the demo until the metric looks good.
