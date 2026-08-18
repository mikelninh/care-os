# CareOS Production Readiness Gates

CareOS graduates by **evidence-backed gates, not version numbers or self-awarded scores**.

Machine-readable normal gates: `GET /api/readiness/gates`.  
Machine-readable agent gates: `GET /api/readiness/agents` / `app/agent_readiness.py`.

> **No normal or agent production gate is PASS today. Proposal completeness, synthetic test coverage and production readiness are separate questions.**

## Normal CareOS gates

| Gate | Status | What still blocks PASS |
|---|---|---|
| G0 Scope & safety boundary | **EXTERNAL REVIEW** | independent MDR/MDSW + clinical-safety review for the exact intended use |
| G1 Clinical truth | **BLOCKED** | Holdout #3 recall 26.32% + 100% review burden; fresh development work + future untouched holdout + user evidence |
| G2 German interoperability | **PARTIAL** | real KIS/LIS/vendor sandbox, local terminology/profile behavior, real identity/context launch |
| G3 Privacy & security | **PARTIAL** | provider IdP/context, protected audit/SIEM, KMS/encryption, DSFA/agreements, network controls, pentest |
| G4 Production reliability | **PARTIAL** | target dependency failures, backup/restore RPO/RTO, monitoring/SLO/incident and rollback exercises in target infrastructure |
| G5 Regulatory & quality | **EXTERNAL REVIEW** | formal qualification/classification + applicable AI Act/EHDS assessment + reviewed quality/risk lifecycle |
| G6 Invisible workflow | **PARTIAL** | real KIS/portal context launch, Citrix/VDI/managed-device proof, measured no-second-search/no-copy workflow |
| G7 Hospital deployment | **PARTIAL** | actual hospital systems/owners/approvals, target security/operations evidence and accepted stop thresholds |
| G8 Repeatability | **NOT EVIDENCED** | two independent real hospitals/vendors without a CareOS core-contract fork, with measured reuse/custom work |
| G9 National/EU scale | **RESEARCH ONLY** | actual ePA/TI/KIM/outpatient/EHDS integration + multi-site operating evidence |

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

G1 remains BLOCKED. The current failure mode is conservative, but review-everything / low recall is not a usable clinical product. The frozen holdout is historical evidence, not tuning data.

## G2–G4 internal evidence

Current internal/synthetic evidence includes:

- HAPI FHIR path + bounded same-origin paging;
- loop/cross-origin/partial-search failure closed;
- vendor-neutral connector contract;
- pinned gematik ISiK-oriented validation path;
- explicit shared-enterprise-ID and trusted-MPI/source-ID contracts;
- narrow synthetic/deidentified HL7 v2 ADT/ORU library connector;
- OIDC/JWT verification foundation;
- role/scope/treatment-context authorization concepts;
- patient-context launch contract;
- secure-read coordinator;
- keyed audit pseudonyms + recursive PHI-key rejection;
- tamper-evident local audit chain;
- global/connector kill switches;
- NORMAL/DEGRADED/OFFLINE/RECOVERY contracts;
- source-correction → dependent-artifact invalidation;
- generated non-secret hospital review pack;
- upgrade preflight + canary/promotion/rollback state machine;
- compatibility registry with evidence classes;
- non-root container + live-lock smoke tests;
- CodeQL, dependency audit, SBOM and Dependabot.

These controls do not substitute for real hospital identity/network/audit/KMS/Datenschutz/recovery evidence.

## G6/G7 — clinician/hospital pathway

Prepared:

- synthetic Infectiology reference environment;
- responsive/low-spec clinician experience;
- paired Time Returned to Care study with matched case variants + order counterbalancing;
- PHI-free structured export and safety-gated aggregation;
- hospital capability manifest + preflight;
- hospital review-pack generation;
- read-only integration/discovery plan;
- rollout, rollback and operations runbooks;
- patient/family synthetic experience;
- cross-provider lifecycle contract;
- golden end-to-end regression journey.

## G8/G9 — scale

The architecture now has reusable-adapter, compatibility, conformance and anti-fork contracts, but **repeatability remains unproven until real site A and site B exist**. National/global proposal readiness is not national/global production evidence.

---

# Agent gates — A0 to A9

Normal CareOS readiness does **not** authorize an AI agent. Identifiable agent access requires normal G0–G5 PASS **and** all relevant A0–A9 gates PASS.

| Agent gate | Status | Internal evidence | Still blocks PASS |
|---|---|---|---|
| A0 Workload identity | **PARTIAL** | first-class agent/version + workload binding + revocation reference | real provider workload identity and rotation/revocation evidence |
| A1 Signed delegation | **PARTIAL** | Ed25519 token + issuer/audience/key/JTI + patient/encounter/task/tool/time budgets + single-use/revocation reference store | production signer/key lifecycle + durable shared replay store |
| A2 Tool least privilege | **PARTIAL** | versioned tool registry + deterministic gateway + trusted tool proxy; model cannot choose patient/org/encounter/egress | all real production tools behind proxy + provider conformance evidence |
| A3 Injection/hijacking | **PARTIAL** | compromised-worker harness + agent-redteam CI; exfiltration/cohort/write attempts contained synthetically | real model/provider corpus + malicious tool/MCP cases + independent red team |
| A4 Egress / PHI | **BLOCKED** | deny-default application contracts + deny-all reference network policy | provider-enforced network proxy/allowlist/DLP + approved model/subprocessor flow |
| A5 Agent audit | **PARTIAL** | human+agent+version+delegation+execution+tool audit schema | protected provider audit/SIEM + integrity/review evidence |
| A6 Memory isolation | **PARTIAL** | organisation/patient/encounter/execution namespace; no persistent memory in first agent | real store + retention/deletion + runtime leakage tests |
| A7 Blast radius | **PARTIAL** | runtime-owned tool/record/page/time/subagent budgets + one-time delegation | distributed rate limits/back-pressure/circuit breakers/load exercises |
| A8 Consequential actions | **BLOCKED** | write/send/order disabled; source-linked review-only assistance contract | action-specific confirmation only under a separate approved programme |
| A9 Independent assurance | **EXTERNAL REVIEW** | security model + synthetic phases/evidence | independent security/clinical/Datenschutz/hospital approval |

**No A0–A9 gate is PASS. No identifiable production agent use is approved.**

## Agent phases

| Phase | Current internal state |
|---|---|
| 1 Gateway foundation | **implemented; production assurance partial** |
| 2 Synthetic reasoning worker | **implemented** |
| 3 Hostile-worker/injection containment | **implemented synthetic; assurance partial** |
| 4 Synthetic paired user study | **ready to run** |
| 5 Deidentified/provider sandbox | **contract implemented; actual hospital interface required** |
| 6 Shadow live | **operating contract exists; code-locked** |
| 7 Controlled read-only live assistance | **contract exists; code-locked** |

Core implementation includes the agent policy/delegation/identity/runtime/tool-proxy/audit/red-team/study/sandbox/shadow/assistance modules documented in `docs/AGENT_SECURITY_MODEL.md` and `docs/AGENT_PHASES_1_7.md`.

## Agent live-data lock

`shadow-live` and `read-only-live` operating modes raise a runtime error while G0–G5 or A0–A9 are incomplete. `consequential` mode is unsupported by the current release policy.

The pass criterion is not “the model refused a malicious instruction.” It is that deterministic identity, delegation, tool, data, egress and effect boundaries prevent harmful access/action even if the reasoning worker is compromised.

---

# Immediate critical path

1. Run the paired synthetic clinician/user study and turn misunderstandings/friction into concrete issues/regressions.
2. Get Recare/Pavlo production critique of the integration, lifecycle, provenance and agent assumptions.
3. Improve G1 recall/review burden on a fresh development corpus without tuning Holdout #3.
4. Obtain one approved real read-only/deidentified KIS/LIS/vendor sandbox and actual hospital interface facts.
5. Complete G0/G5/A9 independent clinical, regulatory, security and Datenschutz review for a fixed intended use.
6. Replace reference identity/audit/egress/replay components with provider-grade infrastructure where needed.
7. Run target-environment reliability, back-pressure, backup/recovery, canary and incident exercises.
8. Only after G0–G5 + applicable A-gates PASS: shadow live with zero operational effect.
9. Only after acceptable shadow evidence + hospital go/no-go: controlled read-only assistance.
10. Reproduce at a second hospital/vendor without a core-contract fork.

A green unit test, scan, architecture diagram, sponsor decision or portfolio review can never waive an external assurance gate.