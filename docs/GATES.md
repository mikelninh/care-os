# CareOS Production Readiness Gates

CareOS graduates by **evidence-backed gates, not version number**.

Machine-readable normal gates: `GET /api/readiness/gates` in `app/readiness_gates.py`.
Agent-specific machine-readable gates: `app/agent_readiness.py`.

> **Reference Architecture readiness is 10/10 for proposal completeness/reviewability. Production readiness is a different question. No normal or agent production gate is PASS yet.**

| Gate | Status | What still blocks PASS |
|---|---|---|
| G0 Scope & safety boundary | **EXTERNAL REVIEW** | Independent MDR/MDSW + clinical-safety review |
| G1 Clinical truth | **BLOCKED** | Holdout #3: 26.3% recall + 100% review burden; next extractor needs fresh development and future untouched holdout |
| G2 German interoperability | **PARTIAL** | Production terminology, incremental sync, real SJK/KIS/LIS/vendor sandbox |
| G3 Privacy & security | **PARTIAL** | Real hospital IdP/context, protected audit/SIEM, KMS/encryption, hospital DSFA/agreements, applicable C5/customer controls, pentest |
| G4 Production reliability | **PARTIAL** | Real-dependency failure injection, backup/restore RPO/RTO, production monitoring/SLO exercise |
| G5 Regulatory & quality | **EXTERNAL REVIEW** | Formal qualification/classification, AI Act/EHDS assessment, reviewed risk/QMS lifecycle |
| G6 Invisible workflow integration | **PARTIAL** | Real KIS/portal context launcher, Citrix/VDI proof, measured no-copy/no-second-search workflow |
| G7 Hospital deployment kit | **PARTIAL** | Actual hospital systems/owners/approvals, target security evidence, pentest, accepted stop thresholds |
| G8 Repeatable deployment | **PARTIAL** | Hospital A + different Hospital B/vendor without a CareOS core fork |
| G9 National/EU scale | **BLOCKED** | Actual ePA/TI/KIM/ISiP/outpatient/EHDS integrations and multi-site operating evidence |

## Reference architecture evidence

The proposal package includes:

- `docs/ARCHITECTURE_V2.md` — canonical technical reference architecture;
- `docs/GOVERNMENT_REFERENCE_ARCHITECTURE.md` — German public-sector architecture;
- `docs/GOVERNMENT_ONE_PAGER_DE.md`;
- `docs/DEPLOYMENT_PATTERNS.md`;
- `docs/TRUST_AND_DATA_FLOW.md`;
- `docs/NATIONAL_INTEGRATION_MAP.md`;
- `docs/TECHNICAL_DOCUMENTATION_INDEX.md`;
- `docs/ASSURANCE_CROSSWALK.md`;
- `docs/RESPONSIBILITY_MODEL.md`;
- `docs/PROCUREMENT_REQUIREMENTS.md`;
- `docs/AGENT_SECURITY_MODEL.md`;
- `docs/AGENT_PRODUCTION_PROGRAM.md`;
- `docs/AGENT_SECURITY_BASELINE.md`;
- Architecture Decision Records under `docs/adr/`, including ADR-011 for delegated agents;
- machine-readable `architecture/reference-architecture.json` with CI invariants.

The architecture score is intentionally **not used to unlock live data**.

## G1 — Clinical truth

Implemented safeguards include:

- mandatory `ClinicalFact` / `TruthEnvelope` contract;
- source identity/version/time semantics where supplied;
- document/model outputs untrusted until source evidence is mechanically verified;
- exact source quote independently located by CareOS;
- model-proposed effective clinical time not trusted;
- assertion maturity separate from extraction confidence;
- confidence never silently chooses a winner between conflicting assertions;
- deterministic case reconciliation downstream of extractors;
- a newer unresolved high-risk source can block older parsed state from appearing current;
- cross-patient truth rejected;
- ambiguous/unknown facts route to review.

### Frozen Holdout #3

**ID:** `g1-holdout3-2026-08-16`  
**Fingerprint:** `e21633181e2d592c9a16653c9a99fb5a0c96dcf787e716dc4ea155cedbfa3ea4`

Across 500 synthetic unseen-format cases:

- precision **100%**;
- recall **26.32%**;
- F1 **41.67%**;
- unsupported claims **0**;
- wrong-source claims **0**;
- provenance coverage **100%**;
- critical silent field misses **0**;
- critical silent contradiction misses **0**;
- review case rate **100%**.

G1 remains **BLOCKED**: safer, but the recall/review burden is unusable. Holdout #3 is historical evidence and is not tuning data.

## G2 — German interoperability

Internal evidence:

- real HAPI FHIR integration path;
- bounded same-origin Bundle pagination;
- cross-origin continuation, loops and silent truncation fail closed;
- vendor-neutral `ConnectorReadResult = SourceState + TruthEnvelope` contract;
- pinned gematik reference-validator + ISiK5 plugin workflow;
- structural/profile validation kept separate from terminology validation;
- explicit national/EU integration map.

A real hospital/vendor path is still required.

## G3 — Security & privacy

Internal evidence includes:

- asymmetric OIDC/JWT verification foundation;
- role/scope/treatment-context authorization;
- short-lived user/organisation/patient context launch;
- break-glass semantics;
- secure-read coordinator that can withhold truth on authorization, source, identity or required-audit failure;
- keyed audit pseudonyms + recursive PHI-key rejection;
- tamper-evident local audit chain;
- provider-side PHI / control-plane separation;
- threat/data-flow/responsibility/DSFA/AVV assurance documentation;
- CodeQL;
- scheduled dependency vulnerability audit;
- CycloneDX SBOM;
- Dependabot;
- explicit agent security model and delegated-principal ADR.

Still external: real provider IdP, production audit/SIEM, KMS/encryption, hospital agreements/approval, applicable C5/customer-control evidence and independent pentest.

## G4 — Reliability / operations

Internal evidence includes:

- explicit `current / stale / unavailable / unknown` source state;
- fail-closed pagination/partial reads;
- global and connector-specific kill switches;
- deployment/rollback and incident-response runbooks;
- SLO framework;
- safety failure-injection CI;
- non-root container image + health check;
- container CI proving synthetic startup;
- container CI proving `live-readonly` does not start while G0–G5 are incomplete;
- transactional/write-back mode unsupported.

Still external: target-environment dependency failures, recovery drills, RPO/RTO, production monitoring and incident exercises.

## G5 — Regulatory / quality

Internal preparation includes intended-purpose/safety boundary, regulatory baseline, risk register, change control, technical-documentation index and assurance crosswalk. CareOS does not self-award MDR/MDSW classification, AI Act/EHDS applicability or QMS sufficiency.

## G6/G7 — SJK reference pathway

Prepared: synthetic SJK Infectiology environment, low-spec/mobile test, 5-minute team-test protocol + measurement tooling, Chefarzt brief/page, read-only integration discovery checklist, staged SJK plan, hospital assurance pack, responsibility matrix, deployment patterns, procurement requirements and pilot stop criteria.

## G8 — Repeatability

Scale must preserve one core with vendor logic behind connectors and specialty/country/language/audience composition. PASS still requires Hospital A + a different Hospital B/vendor without a CareOS core fork.

## G9 — National / EU scale

The reference architecture is proposal-grade and includes national rails, anti-lock-in procurement principles and EHDS-forward documentation. G9 remains **BLOCKED** because proposal completeness is not operating evidence.

# Agent production gates — A0 to A9

Normal CareOS readiness does **not** automatically authorize an AI agent. Identifiable patient-data access requires normal G0–G5 PASS **and** all relevant A0–A9 gates PASS.

| Agent gate | Status now | Internal evidence | Still blocks PASS |
|---|---|---|---|
| A0 Agent/workload identity | **PARTIAL** | explicit agent ID/version and separate-principal contract | real provider workload identity, revocation/rotation |
| A1 Signed delegation | **PARTIAL** | Ed25519 signed envelope; issuer/audience/key ID; patient/encounter/task/tool/data/time/budget binding | production issuer/key lifecycle + replay prevention |
| A2 Tool least privilege | **PARTIAL** | versioned `ToolSpec` registry; deterministic tool/effect/data/egress authorization | register/conformance-test every real production tool |
| A3 Injection/hijacking resilience | **BLOCKED** | hostile-request containment tests; security does not rely on model refusal | model-connected adversarial corpus + independent red team |
| A4 Egress controls | **BLOCKED** | deny-default delegation/tool egress contracts | provider network/DLP enforcement + approved model/subprocessor path |
| A5 Agent audit | **PARTIAL** | human + agent + version + delegation + execution + tool structured audit schema | protected provider audit/SIEM + integrity/review evidence |
| A6 Memory isolation | **PARTIAL** | organisation/patient/encounter/execution-scoped pseudonymous namespace | real memory store + retention/deletion/leakage tests |
| A7 Abuse/blast-radius limits | **PARTIAL** | hard tool/record/page/runtime/sub-agent limits; arbitrary patient search denied | distributed rate limits, back-pressure, circuit breakers, load/runaway tests |
| A8 Consequential actions | **BLOCKED** | write/external-send disabled; future tool contract requires confirmation | action-specific human confirmation + separate safety/regulatory release |
| A9 Independent agent review | **EXTERNAL REVIEW** | security model + production programme + external baseline | independent security/clinical/Datenschutz/hospital review |

### Agent Stage 0 evidence now implemented

The repository now contains:

- `app/agent_policy.py` — narrow delegation authorization;
- `app/agent_delegation.py` — Ed25519 signed delegation envelope;
- `app/agent_tools.py` — versioned tool registry/risk metadata;
- `app/agent_runtime.py` — deterministic gateway + execution budgets + memory namespace;
- `app/agent_audit.py` — PHI-minimized dual-attribution agent audit events;
- `app/agent_readiness.py` — A0–A9 machine-readable gate manifest;
- `app/synthetic_agent.py` — first gateway-backed synthetic SJK morning-review flow;
- adversarial tests for cross-patient access, egress, undeclared tools/data, write/break-glass escalation, recursion and budget bypass.

**No A0–A9 gate is PASS today. No identifiable production agent use is approved.**

The pass criterion is not “the model refused the attack.” It is that deterministic policy/capability boundaries prevent harmful access/action even if the reasoning worker is hijacked.

## Live-data lock

Identifiable live patient data remains locked while any of G0–G5 is not PASS. If agentic access is added, identifiable agent use additionally remains locked until the relevant A0–A9 gates pass.

A green test, security scan or architecture score is never sufficient to pass an external assurance gate.

## Immediate critical path

1. **G1:** improve recall/review burden on a fresh development corpus without tuning Holdout #3.
2. **SJK Stage 0:** collect measured synthetic clinician workflow evidence.
3. **Agent Stage 1:** connect a reasoning worker only to synthetic facts through the gateway; build indirect-prompt-injection/tool-hijacking red-team harness.
4. **G0/G5/A9:** independent clinical-safety, medical-software, security and Datenschutz review.
5. **G2:** one real read-only KIS/LIS/vendor sandbox.
6. **G3/A0/A4/A5:** real hospital IdP/workload identity, protected audit/KMS, network egress policy, hospital-specific Datenschutz/security evidence and pentest.
7. **G4/A7:** target-environment failure, backup/restore, rate/back-pressure and incident exercises.
8. **G8:** reproduce at a second hospital/vendor without a core fork.
