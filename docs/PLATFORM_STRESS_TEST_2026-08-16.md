# CareOS Whole-Platform Stress Test — 2026-08-16

Status: **synthetic/de-identified internal adversarial pass; not production approval**.

Validated head before this documentation-only commit: `62a4b0a567df17a827f7002cda6a92f61d14587b`.

## Purpose

This review treated CareOS as a hostile pre-pilot environment rather than a demo. The goal was to find ways the platform could show the wrong patient, trust the wrong source, overclaim impact, leak data, execute hostile content, grant excessive privilege, allow an agent to escape its delegation, or silently turn unavailable/ambiguous/cancelled clinical state into reassuring certainty.

The review covered the clinician UI, Infectiology/Oncology/Neurology use cases, legacy inbox/documentation, FHIR transport, patient binding, clinical read orchestration, truth reconciliation, document extraction, audit, break-glass, impact measurement, agent/model boundaries, replay/concurrency, API input bounds and live-data release locks.

## Final internal evidence

The dedicated `platform-redteam` workflow completed successfully on the validated head.

- full regression + adversarial suite: **266 passed**;
- delegation replay contention: **256 attempts → 1 accepted, 255 denied**;
- hostile agent corpus: **6/6 contained**;
- model projection stress: **10,000 candidate facts → max 50 admitted source-linked facts**, no forbidden direct-identifier key in the fixed projection;
- specialty structural evidence: Infectiology **6 cards / 4 pending / 6 timeline events**, Oncology **5 / 3 / 4**, Neurology **4 / 3 / 4**, with source coverage in all tested cards/timeline events;
- impact-integrity attack: forged client claim of `999999` saved minutes was ignored; server recomputed **9.0 min** from raw evidence;
- failed-fast task: **0 credited saved minutes**;
- cancelled clinical assertion: cancelled target was removed from the current surface;
- browser patient-switch guards: stale focus/timeline responses cannot overwrite the newly active patient;
- live patient data, identifiable-PHI agent use and consequential autonomous actions remained locked;
- machine-readable evidence artifact was uploaded by CI.

A separate 500-case unseen benchmark workflow also exists. Its purpose is different: it measures extraction/truth utility and keeps G1 visibly blocked when recall/review burden is inadequate. A successful system/security stress run does not override that clinical-truth gate.

## Material gaps found and fixed in this review

| Severity | Finding | Fix now in main |
|---|---|---|
| **Critical** | FHIR search trusted server-side patient filters; a hostile/buggy source could return patient B and CareOS could attach it to patient A | Patient resource ID and patient/subject/for references are re-validated before snapshot/truth conversion |
| **Critical** | A cancelled clinical assertion could leave the result it cancelled on the current surface | Cancellation/supersession is processed before current-state reconciliation; unbound cancellation blocks older/equal same-concept state |
| **High** | Public FHIR integration endpoints could become a future live-PHI bypass around clinical authorization/audit | Lab/demo FHIR routes are explicitly disabled for live mode; future live reads must use authenticated clinical orchestration |
| **High** | Specialty UI rendered clinical strings through raw `innerHTML` | Dynamic specialty clinical values are escaped before HTML rendering |
| **High** | Fast A→B patient switching could allow slower patient-A network responses to overwrite patient-B browser state | Focus/timeline requests are generation- and patient-bound before rendering |
| **High** | Break-glass could be requested by an ordinary scoped clinician without a separately granted emergency privilege | `break_glass_allowed` must come from authoritative hospital policy/identity context; reason + elevated audit still required |
| **High** | Emergency access context was lost in generic audit events | Audit records now preserve organisation, elevated audit level and break-glass flag without storing the free-text emergency reason |
| **High** | Connector exceptions could bubble internal/provider details | Clinical read orchestration converts connector crashes into generic source-unavailable state and withholds truth |
| **High** | Agent model adapter lacked redirect, request/response size and proposal-count ceilings | Redirects are denied; request/response bytes and proposal count are bounded; endpoint host/port/HTTPS rules tightened |
| **High** | Model projection could starve valid facts because its cap applied before delegated-category filtering | Cap now applies after filtering; total input and per-fact byte size are also bounded |
| **High** | Document text/candidate ingestion was effectively unbounded | Document text and extracted candidate counts/field sizes are bounded before truth construction |
| **High** | A fast failed pilot task could still count as time saved | Failed tasks get zero credited savings |
| **High** | Aggregate impact endpoint trusted client-computed savings | Aggregates are recomputed from bounded raw measurements and ignore forged `saved_minutes` |
| **Medium** | Oncology/Neurology packs did not provide the same source-linked timeline depth as Infectiology | Both now have multi-event source-linked synthetic timelines for shared provenance testing |
| **Medium** | API query/aggregate inputs had weak exhaustion bounds | Search/query/count/aggregate inputs are bounded and invalid requests fail validation |

## Workflow scenarios now tested end to end

1. **Infectiology morning review** — microbiology, pending/final-state language, source references, documented anti-infective therapy without treatment recommendation.
2. **Oncology handover** — diagnosis/stage, molecular pathology, therapy cycle, toxicity and open tumor-board/response work.
3. **Neurology change review** — baseline vs new change, imaging and pending reassessment.
4. **Legacy inbox** — ambiguous patient match must block automatic attachment and require human review.
5. **Documentation reuse** — note → prepared handover/tasks while production write-back remains absent.
6. **Pilot measurement** — failure and forged-savings attacks cannot create false impact.
7. **Agent workflow/readiness** — synthetic tool surface exists, while live identifiable PHI and consequential actions remain locked.
8. **Unknown resources** — invalid patient/specialty/inbox resources fail cleanly rather than returning plausible data.

## Remaining blockers — deliberately not claimed as solved

### 1. G1 clinical truth utility — **BLOCKER**

The architecture is safer, but the frozen unseen evidence still shows that extraction recall/review burden is not good enough to declare the clinical truth layer useful in production. The next extractor work must use fresh development data and another untouched holdout; the existing frozen holdout must not become tuning data.

### 2. Real KIS/LIS/vendor behavior — **BLOCKER**

Synthetic FHIR and HAPI validation cannot prove real hospital interoperability. We still need an actual read-only/de-identified provider sandbox with real interface shapes, pagination quirks, terminology, partial failures, latency, stale feeds and vendor-specific behavior.

### 3. Provider security infrastructure — **BLOCKER**

Still missing: real hospital IdP/workload identity, patient/encounter context resolver, distributed delegation replay/revocation, KMS/secrets, protected immutable audit/SIEM, network egress/DLP, approved model/subprocessor flow and independent penetration test.

### 4. Production load / back-pressure / recovery — **HIGH**

The concurrency tests prove narrow invariants, not hospital-scale operations. Target-environment tests still need rate limiting, queues, source-system back-pressure, circuit breakers, timeout storms, recovery drills, RPO/RTO and SLO/alerting exercises.

### 5. File/PDF/OCR security boundary — **HIGH**

Text/candidate ingestion is bounded, but a production scan/PDF service still requires file-type validation, malware scanning, parser sandboxing, decompression-bomb protection and OCR-specific adversarial testing.

### 6. Model free-text PHI / DLP — **HIGH**

The fixed model projection removes direct identifier fields, but clinical scalar/free-text values can themselves contain identifying material. This is one reason live external-model PHI use remains locked pending provider-side minimization/DLP and approved data-flow evidence.

### 7. Browser estate, accessibility and low-spec evidence — **HIGH**

The static demo has safety guards, but it has not been validated on the actual managed hospital browser/Citrix/VDI estate, with keyboard-only use, screen readers, accessibility review, zoom/high-contrast behavior and low-spec performance under realistic latency.

### 8. Human factors / automation bias — **HIGH**

Verification decay is instrumented but has no human evidence yet. A faster workflow is a failure if clinicians stop checking sources, miss pending work, or rubber-stamp agent drafts. The synthetic A/B clinician study is the next evidence step.

### 9. Regulatory, Datenschutz and clinical-safety assurance — **EXTERNAL**

MDR/MDSW qualification/classification, AI Act/EHDS applicability, DSFA/DPIA, AVV/DPA, hospital clinical-safety acceptance and residual-risk acceptance must be reviewed by qualified external stakeholders. Internal architecture/tests cannot self-award these approvals.

## Current conclusion

The internal deterministic platform is materially stronger after this review, and the final whole-platform synthetic/de-identified red-team run passes. The review also demonstrated why CareOS must remain gate-driven: multiple serious issues were found only after earlier green test runs.

**What this pass means:** the tested internal invariants survived the current synthetic/de-identified attack suite.

**What this pass does not mean:** production-ready, Datenschutz-approved, clinically validated, hospital-integrated, certified, or approved for identifiable patient data.

## Next evidence tranche

The next highest-value work is no longer generic feature expansion. It is:

1. clinician synthetic A/B testing and workflow observation;
2. actual de-identified KIS/LIS/provider sandbox discovery;
3. provider identity/context/audit/egress integration;
4. target-environment performance/failure/recovery testing;
5. independent security, Datenschutz, clinical-safety and regulatory review;
6. only after the relevant G/A gates pass: zero-effect shadow evaluation, then controlled read-only assistance.
