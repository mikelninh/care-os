# CareOS Incident Response — clinical context system

Status: target operating model. Named hospital/CareOS contacts, tooling and contractual timelines must be filled for each deployment.

## Incident classes

### P0 — immediate patient-safety / severe security concern
Examples:
- wrong-patient information;
- authorization bypass / widespread illegitimate access;
- clinical source corruption or material integrity failure;
- unsupported critical claim presented as confirmed;
- source outage displayed as current/complete;
- confirmed PHI exfiltration with active exposure.

Default action: activate kill switch / isolate affected component, preserve evidence, notify clinical + security leadership immediately under the agreed process.

### P1 — serious but contained
Examples:
- repeated extraction/provenance failure in a limited workflow;
- connector data significantly stale beyond policy;
- audit path failure;
- suspected PHI leakage into telemetry;
- critical dependency degradation without evidence of patient impact.

Default action: disable affected function/connector if safety cannot be assured; investigate with elevated monitoring.

### P2 — operational degradation
Examples:
- non-critical latency;
- isolated UI defect;
- recoverable connector retry issue;
- non-safety-affecting reporting bug.

## Response sequence

1. **Detect** — monitoring, user report, audit anomaly, test, security alert.
2. **Classify** — patient safety, confidentiality, integrity, availability, scope.
3. **Contain** — connector kill switch, account/session block, feature disable, deployment rollback.
4. **Preserve** — logs/audit/build/config/source versions without unnecessary PHI copying.
5. **Notify/escalate** — deployment-specific legal/security/clinical process.
6. **Eradicate/fix** — root cause and compensating controls.
7. **Recover** — controlled restoration with targeted regression evidence.
8. **Review** — root cause, affected patients/users/sources, missed detection opportunities, corrective/preventive actions.

## Evidence that must be reconstructable

- application/build/version;
- connector/source version and freshness;
- clinical fact provenance and transformation version;
- user identity/access decision;
- configuration/policy version;
- timestamps;
- relevant audit/security events;
- exact rollback/change performed.

## Clinical integrity rule

An integrity incident is not treated as an ordinary SaaS bug merely because confidentiality was unaffected. If CareOS could have changed what a clinician believed about a patient, clinical-safety review is part of incident handling.

## Recovery rule

Do not restore a disabled workflow because the service is merely reachable again. Restore only after the failure mode has a tested mitigation and the responsible owner accepts the residual risk.
