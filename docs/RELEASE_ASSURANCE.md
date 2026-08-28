# CareOS Release Assurance

This document separates **what the repository exercises automatically** from what still requires external clinical, hospital, privacy, security or regulatory evidence.

CareOS is a pre-hospital research system. Passing this matrix is an engineering gate, **not clinical validation or authorization for production PHI**.

## Assurance layers

| Layer | Current evidence | Meaning |
|---|---|---|
| Golden clinical lifecycle | `app/end_to_end_journey.py` + regression tests | preliminary → source-linked context → draft → outage → correction → recovery/reconciliation → stale derived work → human review/audit |
| Clinical state semantics | automated tests | pending ≠ negative; unavailable ≠ absent; documented therapy ≠ AI recommendation; agent draft ≠ source truth |
| Patient identity / isolation | access-policy, gateway, graph and red-team tests | wrong-patient and cross-context access must fail closed |
| Agent authority | agent gateway/policy/delegation/hijacking/red-team suites | model cannot grant itself patient, tool, operation or write authority |
| Provenance / stale state | graph/lifecycle/invalidation tests | source corrections invalidate or flag derived work rather than silently preserving it |
| Degraded/offline/recovery | runtime and recovery scenarios | normal operation may resume only after reconciliation |
| FHIR / ISiK / HL7 research paths | integration/validation workflows | research compatibility paths are executable; named production-vendor compatibility is not claimed |
| Security/static analysis | CodeQL + platform/agent red-team workflows | code and authority boundaries receive automated adversarial/static checks |
| Public clinical UX demo | portfolio DOM smoke + manual desktop/mobile visual QA | source review → human status review → documentation preparation → documentation review → ready-for-transfer; conflicts block release |
| Frozen clinical-truth holdout | scheduled G1 benchmark | current 500-case holdout remains a blocker, not a marketing metric |

## Public interactive demo

<https://mikelninh.github.io/careos/clinical.html>

The public demo uses synthetic data and demonstrates the human-review workflow. It does **not** write to a KIS/PVS, recommend treatment or imply clinical validation.

The demo deliberately contains negative paths:

- a pending result remains pending rather than becoming negative;
- conflicting discharge information blocks release until human clarification;
- documentation can be prepared and reviewed, but the demo only marks it **ready for transfer** — it does not perform a production write.

## Adversarial / edge-case families

The repository includes automated coverage for scenarios such as:

- wrong patient / wrong encounter;
- prompt injection and agent hijacking;
- unavailable source;
- stale/corrected source result;
- unauthorized write escalation;
- bounded delegation and tool access;
- provenance and patient-local graph integrity;
- degraded/offline/recovery transitions;
- reconciliation before returning to NORMAL.

See the test suite and workflows rather than treating this list as a completeness claim.

## CI entry points

Key workflows include:

- `.github/workflows/test.yml`
- `.github/workflows/container-smoke.yml`
- `.github/workflows/codeql.yml`
- `.github/workflows/agent-redteam.yml`
- `.github/workflows/platform-redteam.yml`
- `.github/workflows/fhir-integration.yml`
- `.github/workflows/isik5-validation.yml`
- `.github/workflows/g1-dev.yml`
- `.github/workflows/g1-holdout3.yml`
- `.github/workflows/hospital-self-install.yml`

## Known blocker

The frozen 500-case synthetic clinical-truth holdout currently reports **26.32% recall with 100% review-case burden**. Production G1 therefore remains blocked.

Do not tune against the frozen holdout just to improve the public number. Improvements belong on fresh development data, then the holdout is used as an independent gate.

## What engineering E2E does not prove

Even a completely green repository does **not** prove:

- clinical safety in real patient care;
- real clinician time savings;
- production KIS/LIS interoperability;
- lawful/approved PHI operation in a hospital;
- medical-device or other regulatory status;
- multi-hospital repeatability;
- 24/7 operational reliability.

Those require real clinicians, approved/deidentified vendor environments, hospital IT/security/privacy review, governed shadow workflows and eventually bounded production pilots.

## Release rule

A claim may only move from **implemented** to **proven** when the evidence type matches the claim. Synthetic engineering evidence can unblock engineering work; it cannot silently substitute for clinical or institutional evidence.
