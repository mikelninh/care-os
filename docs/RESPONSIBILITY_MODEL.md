# CareOS Responsibility Model

Purpose: prevent a common production failure mode — technically sound controls with unclear ownership.

A real deployment must replace generic role names with named accountable organisations/people.

## Roles

- **CareOS product/platform** — software architecture, release, core security, connector framework, evidence package.
- **Provider clinical owner** — clinical workflow, intended local use, clinical stop criteria.
- **Provider IT/integration** — KIS/LIS interfaces, network, device/VDI, local platform operations.
- **Provider Informationssicherheit / CISO** — security acceptance, monitoring, incident coordination.
- **Provider Datenschutz / DSB** — privacy governance/assessment.
- **Regulatory/quality owner** — classification, quality/risk lifecycle where required.
- **Independent assessor** — penetration test, regulatory/clinical-safety or other independent review where required.

## Responsibility matrix

| Area | CareOS | Provider | Independent / external |
|---|---|---|---|
| Core architecture / truth contracts | **A/R** | C | C |
| KIS/LIS source correctness | C | **A/R** | vendor may support |
| Connector implementation | R | A/C | vendor may support |
| Patient/encounter authoritative identifiers | C | **A/R** | source vendor |
| Hospital IdP / user lifecycle | C | **A/R** | IdP vendor |
| CareOS token verification | **A/R** | C | security review |
| Role/treatment-context policy definition | R | **A** | DSB/CISO/clinical C |
| Clinical workflow design | C | **A/R** | clinical evaluator C |
| Data-flow / purpose definition | R | **A** | DSB C |
| DSFA/DPIA | support | **A/R** | DSB / legal |
| AVV/DPA / subprocessors | R | **A** | legal/DSB C |
| Cloud C5 provider evidence | R for selected service | **A** for acceptance/customer controls | auditor/provider |
| Customer-side C5 controls | C | **A/R** | audit as required |
| Encryption / KMS platform implementation | R | **A/C** | security assessor C |
| Provider keys/secrets ownership | C/R by pattern | **A** | C |
| Application audit event generation | **A/R** | C | test/review |
| Central audit/SIEM retention | C | **A/R** | C |
| Threat model | **R** | **A/C** for deployment | pentester C |
| Penetration test | support/remediate | A/C | **R** |
| Backup/restore | R by deployment pattern | **A** | test evidence |
| Kill switch / rollback decision | R technical | **A** operational/clinical | C |
| Clinical safety stop criteria | C | **A/R** | independent reviewer C |
| MDR/MDSW classification | support | C | **A/R qualified owner** |
| AI Act/EHDS applicability | support | C | **A/R qualified owner** |
| Production release decision | R evidence | **A jointly** | review evidence |
| Live-data activation | cannot self-authorize | **A** after gates/reviews | C |

Legend: **A** accountable, **R** responsible, C consulted.

## Shared-responsibility rules

1. CareOS cannot certify the hospital's identity source, network, source data quality or customer-side cloud controls.
2. The hospital cannot treat a vendor security document as proof that local deployment controls are correctly implemented.
3. A cloud provider's C5 evidence does not remove provider/customer responsibilities.
4. A clinically approved workflow does not waive security/privacy/regulatory gates.
5. A technically green connector does not prove clinical usefulness.
6. A senior sponsor cannot waive wrong-patient, audit, access-control or critical silent-error stop conditions.

## Named deployment record

Before live data, record at least:

- clinical sponsor;
- clinical safety owner;
- IT/integration owner;
- CISO/Informationssicherheit owner;
- Datenschutz/DSB owner;
- incident commander/escalation contacts;
- KIS/LIS vendor contacts;
- CareOS release owner;
- key/KMS owner;
- audit/SIEM owner;
- kill-switch authority;
- rollback authority;
- regulatory/quality reviewer;
- penetration-test provider.
