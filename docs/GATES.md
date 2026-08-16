# CareOS Production Readiness Gates

CareOS graduates by **evidence-backed gates, not version numbers**.

Machine-readable normal gates: `GET /api/readiness/gates`.  
Machine-readable agent gates: `GET /api/readiness/agents` / `app/agent_readiness.py`.

> **Reference Architecture readiness is 10/10 for proposal completeness/reviewability. Production readiness is a separate question. No normal or agent production gate is PASS today.**

## Normal CareOS gates

| Gate | Status | What still blocks PASS |
|---|---|---|
| G0 Scope & safety boundary | **EXTERNAL REVIEW** | independent MDR/MDSW + clinical-safety review |
| G1 Clinical truth | **BLOCKED** | Holdout #3 recall 26.32% + 100% review burden; next extractor needs fresh development and a future untouched holdout |
| G2 German interoperability | **PARTIAL** | production terminology/incremental sync + real SJK/KIS/LIS/vendor sandbox |
| G3 Privacy & security | **PARTIAL** | provider IdP/context, protected audit/SIEM, KMS/encryption, DSFA/agreements, applicable C5/customer controls, pentest |
| G4 Production reliability | **PARTIAL** | target dependency failures, backup/restore RPO/RTO, production monitoring/SLO/incident exercise |
| G5 Regulatory & quality | **EXTERNAL REVIEW** | formal qualification/classification + AI Act/EHDS assessment + reviewed quality/risk lifecycle |
| G6 Invisible workflow | **PARTIAL** | real KIS/portal context launch, Citrix/VDI proof, measured no-second-search/no-copy workflow |
| G7 Hospital deployment | **PARTIAL** | actual hospital systems/owners/approvals, target security evidence, pentest, accepted stop thresholds |
| G8 Repeatability | **PARTIAL** | Hospital A + different Hospital B/vendor without a CareOS core fork |
| G9 National/EU scale | **BLOCKED** | actual ePA/TI/KIM/ISiP/outpatient/EHDS integration + multi-site operating evidence |

Identifiable live patient data remains code-locked while any G0–G5 gate is not PASS.

## G1 evidence — Clinical Truth

Implemented safeguards include mandatory `ClinicalFact`/`TruthEnvelope`, provenance/evidence verification, source/version/time semantics, model-untrusted admission, deterministic reconciliation, review barriers for newer unreadable high-risk sources, cross-patient rejection and explicit unknown/review states.

Frozen Holdout #3 (`g1-holdout3-2026-08-16`, fingerprint `e21633181e2d592c9a16653c9a99fb5a0c96dcf787e716dc4ea155cedbfa3ea4`) across 500 synthetic unseen-format cases:

- precision **100%**;
- recall **26.32%**;
- F1 **41.67%**;
- unsupported claims **0**;
- wrong-source claims **0**;
- provenance **100%**;
- critical silent field misses **0**;
- critical silent contradiction misses **0**;
- review case rate **100%**.

G1 remains BLOCKED: the safety failure mode improved, but the review/recall burden is unusable. The holdout is historical evidence, not tuning data.

## G2–G4 internal evidence

Current internal evidence includes:

- HAPI FHIR path + bounded same-origin paging;
- loop/cross-origin/partial-search failure closed;
- vendor-neutral connector contract;
- pinned gematik ISiK5 structural/profile validation;
- OIDC/JWT verification foundation;
- role/scope/treatment-context authorization;
- patient-context launch contract;
- secure-read coordinator;
- keyed audit pseudonyms + recursive PHI-key rejection;
- tamper-evident local audit chain;
- global/connector kill switches;
- incident/rollback/SLO framework;
- non-root container + health/live-lock smoke tests;
- CodeQL, dependency audit, SBOM and Dependabot.

These controls do not substitute for real hospital identity/network/audit/KMS/Datenschutz/recovery evidence.

## G6/G7 — SJK pathway

Prepared:

- synthetic SJK Infectiology reference environment;
- mobile/low-spec clinician test;
- team test + PHI-free measurement tooling;
- Chefarzt decision brief/page;
- IT/Datenschutz/security discovery checklist;
- read-only integration plan;
- hospital assurance pack, deployment patterns and responsibility model;
- SJK agent A/B protocol measuring verification decay.

## G8/G9 — scale

Scale must preserve one core, stable truth/security contracts and vendor-specific logic behind connectors. National proposal readiness is not national production evidence.

---

# Agent gates — A0 to A9

Normal CareOS readiness does **not** authorize an AI agent. Identifiable agent access requires normal G0–G5 PASS **and** all relevant A0–A9 gates PASS.

| Agent gate | Status | Internal evidence | Still blocks PASS |
|---|---|---|---|
| A0 Workload identity | **PARTIAL** | first-class agent/version + workload binding + revocation reference | real provider workload identity and rotation/revocation evidence |
| A1 Signed delegation | **PARTIAL** | Ed25519 token + issuer/audience/key/JTI + patient/encounter/task/tool/time budgets + single-use/revocation reference store | production signer/key lifecycle + durable shared replay store |
| A2 Tool least privilege | **PARTIAL** | versioned tool registry + deterministic gateway + trusted tool proxy; model cannot choose patient/org/encounter/egress | all real production tools behind proxy + provider conformance evidence |
| A3 Injection/hijacking | **PARTIAL** | compromised-worker harness + dedicated agent-redteam CI; exfiltration/cohort/write attempts contained | real model/provider corpus + malicious tool/MCP cases + independent red team |
| A4 Egress / PHI | **BLOCKED** | deny-default application contracts + deny-all reference network policy | provider-enforced network proxy/allowlist/DLP + approved model/subprocessor flow |
| A5 Agent audit | **PARTIAL** | human+agent+version+delegation+execution+tool audit schema | protected provider audit/SIEM + integrity/review evidence |
| A6 Memory isolation | **PARTIAL** | organisation/patient/encounter/execution namespace; no persistent memory in first agent | real store + retention/deletion + model-runtime leakage tests |
| A7 Blast radius | **PARTIAL** | runtime-owned tool/record/page/time/subagent budgets + one-time delegation | distributed rate limits/back-pressure/circuit breakers/load exercises |
| A8 Consequential actions | **BLOCKED** | write/send/order disabled; source-linked review-only assistance contract | action-specific confirmation only under a separate approved programme |
| A9 Independent assurance | **EXTERNAL REVIEW** | security model + phases 1–7 programme + CI evidence | independent security/clinical/Datenschutz/hospital approval |

**No A0–A9 gate is PASS. No identifiable production agent use is approved.**

## Agent phases 1–7

| Phase | Current internal state |
|---|---|
| 1 Gateway foundation | **implemented; production assurance partial** |
| 2 Synthetic reasoning worker | **implemented** |
| 3 Hostile-worker/injection containment | **implemented synthetic; assurance partial** |
| 4 SJK synthetic A/B study | **ready to run with clinicians** |
| 5 Deidentified/provider sandbox | **contract implemented; actual hospital interface required** |
| 6 Shadow live | **implemented as operating mode but code-locked** |
| 7 Controlled read-only live assistance | **implemented as contract but code-locked** |

Core implementation includes:

- `app/agent_policy.py`;
- `app/agent_delegation.py`;
- `app/agent_identity.py`;
- `app/agent_execution_store.py`;
- `app/agent_tools.py`;
- `app/agent_runtime.py`;
- `app/agent_tool_proxy.py`;
- `app/agent_worker.py`;
- `app/agent_orchestrator.py`;
- `app/agent_session.py`;
- `app/agent_audit.py`;
- `app/agent_redteam.py`;
- `app/agent_study.py`;
- `app/agent_sandbox.py`;
- `app/agent_shadow.py`;
- `app/agent_assistance.py`;
- `app/agent_modes.py`.

Evidence workflow: `.github/workflows/agent-redteam.yml` generates `careos-agent-redteam-evidence`.

Detailed programme: `docs/AGENT_PHASES_1_7.md` and `docs/AGENT_SECURITY_MODEL.md`.

## Agent live-data lock

`shadow-live` and `read-only-live` operating modes raise a runtime error while G0–G5 or A0–A9 are incomplete. `consequential` mode is unsupported by the current release policy.

The pass criterion is not “the model refused a malicious instruction.” It is that deterministic identity, delegation, tool, data, egress and effect boundaries prevent harmful access/action even if the reasoning worker is compromised.

---

# Immediate critical path

1. Improve G1 recall/review burden on a fresh development corpus without tuning Holdout #3.
2. Run SJK synthetic clinician test, then the paired CareOS-vs-agent A/B protocol.
3. Complete G0/G5/A9 independent clinical, regulatory, security and Datenschutz review.
4. Obtain one real read-only KIS/LIS/vendor sandbox and actual SJK IT interface facts.
5. Replace reference agent replay/identity/audit/egress components with provider-grade infrastructure.
6. Run target-environment reliability, rate/back-pressure and recovery exercises.
7. Only after G0–G5 + A0–A9 PASS: shadow live with zero operational effect.
8. Only after acceptable shadow evidence + hospital go/no-go: controlled read-only assistance.
9. Reproduce at a second hospital/vendor without a core fork.

A green test, scan, architecture score or sponsor decision can never waive an external assurance gate.
