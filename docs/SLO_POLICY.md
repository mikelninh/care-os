# CareOS Reliability / SLO Policy

Status: **framework, not production SLO claims**. Numerical targets must be set from the actual hospital workflow, source-system constraints and measured pilot evidence.

## Why ordinary uptime is insufficient

A clinical context service can be reachable while still unsafe because its source data are stale, incomplete, mismatched or unaudited. CareOS therefore separates application availability from **clinical-data usability**.

## Service indicators

For every production deployment measure at least:

### Application
- request availability/error rate;
- latency by critical route;
- deployment/rollback success;
- authentication dependency health.

### Source data
- connector availability;
- last successful refresh;
- data age relative to workflow-specific freshness policy;
- pagination/synchronization completeness;
- version/reconciliation failures;
- stale/unavailable duration.

### Clinical truth
- provenance coverage;
- unsupported-claim rate;
- critical silent contradiction misses;
- patient-context mismatches;
- review/ambiguity rate;
- correction rate.

### Security / audit
- authorization denials by reason;
- break-glass events;
- audit delivery success/latency;
- privileged/admin access;
- security-event detection and response time.

## Safety budget

CareOS must not trade a safety-critical correctness metric for conventional uptime. If source integrity/currentness cannot be established, the correct service state may be **degraded/unavailable**, even if that reduces apparent availability.

Example principle:

> 99.9% endpoint uptime with stale clinical truth is worse than a visible outage.

## Workflow-specific freshness

There is no universal clinical freshness number. Each source/workflow must define a policy with the responsible clinical/integration owner.

Example configuration fields:

```text
source_id
workflow
expected_update_mode
max_age_for_quiet_rendering
max_age_for_visible_stale_rendering
action_when_threshold_exceeded
owner
```

The current `SourceState` implementation provides the mechanism; the hospital-specific policy provides the actual thresholds.

## Error-budget response

When a safety/reliability indicator exceeds its agreed limit:

1. stop expansion;
2. determine whether affected view/connector must be disabled;
3. use the runtime kill switch where needed;
4. return clinicians to existing source workflow;
5. investigate and preserve evidence;
6. restore only after mitigation is validated.

## Backup / recovery

CareOS should minimize authoritative state because primary clinical systems remain source of truth. For CareOS-owned state that must persist—configuration, audit references, approvals, local policy, review state, operational metadata—define:

- backup scope/frequency;
- encryption and access controls;
- RPO/RTO;
- restore test cadence;
- dependency required for recovery;
- evidence of successful restores.

No RPO/RTO target is claimed until deployment architecture and measured restore tests exist.

## Gate evidence

G4 reaches PASS only when the actual deployment has:

- numerical, clinically approved freshness/SLO thresholds;
- monitoring and alerting wired to them;
- failure-injection evidence;
- tested backup/restore with measured RPO/RTO;
- executable kill switch/rollback;
- incident-response exercise;
- demonstrated degraded-mode UX for critical dependencies.
