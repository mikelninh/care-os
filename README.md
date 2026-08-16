# CareOS

> **Patient history without the hunt. Document once, reuse safely.**

[![tests](https://github.com/mikelninh/care-os/actions/workflows/test.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/test.yml)
[![agent-redteam](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml)
[![supply-chain](https://github.com/mikelninh/care-os/actions/workflows/supply-chain-security.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/supply-chain-security.yml)

## What CareOS is

CareOS is a **clinician-first, federated clinical context layer** for fragmented healthcare systems.

It sits beside KIS/PVS/EHR/LIS/RIS/ePA systems rather than replacing them. Authoritative records stay in source systems. Routine identifiable patient data stays in the provider data plane or a dedicated provider-controlled tenant; the shared control plane distributes software, versioned packs, policy/configuration and non-PHI operational metadata.

**First specialty:** Infectiology.  
**North star:** return meaningful time to care without making clinical information less trustworthy, current, auditable or understandable.

Public demos are synthetic only and are **not for clinical use**.

- SJK Infectiology synthetic team test: https://mikelninh.github.io/careos/sjk/
- SJK Chefarzt / leadership view: https://mikelninh.github.io/careos/sjk/chef.html
- General clinician demo: https://mikelninh.github.io/careos/

---

# Reference Architecture: **10 / 10 proposal readiness**

This means **architecture-package completeness and reviewability**, not production approval, certification or clinical validation.

The architecture is ready for serious review by clinicians, Chefarzt/medical leadership, hospital CIO/CISO/Datenschutz, government architects, gematik/public-sector stakeholders and funding partners.

Core package:

- [Reference Architecture V2](docs/ARCHITECTURE_V2.md)
- [German Government Reference Architecture](docs/GOVERNMENT_REFERENCE_ARCHITECTURE.md)
- [Government One-Pager DE](docs/GOVERNMENT_ONE_PAGER_DE.md)
- [Trust & Data Flow](docs/TRUST_AND_DATA_FLOW.md)
- [Deployment Patterns](docs/DEPLOYMENT_PATTERNS.md)
- [National / EU Integration Map](docs/NATIONAL_INTEGRATION_MAP.md)
- [Technical Documentation Index](docs/TECHNICAL_DOCUMENTATION_INDEX.md)
- [Assurance Crosswalk](docs/ASSURANCE_CROSSWALK.md)
- [Responsibility Model](docs/RESPONSIBILITY_MODEL.md)
- [Public-Sector Procurement Requirements](docs/PROCUREMENT_REQUIREMENTS.md)
- [Architecture Decision Records](docs/adr/README.md)
- machine-readable [`architecture/reference-architecture.json`](architecture/reference-architecture.json)

## Central architecture

```text
                            CAREOS CONTROL PLANE

          releases · pack versions · policy/config bundles
       terminology metadata · guidelines · non-PHI operations
                                 │
                       no routine identifiable PHI
                                 │
═════════════════════════════════╪════════════════════════════════════
                                 │
                    PROVIDER / HOSPITAL DATA PLANE
                                 │
 KIS/EHR ─┐
 LIS/Micro├──────> Connector Gateway
 RIS/PACS ┤               │
 PVS      ┤               ▼
 ePA/TI   ┤        Patient + Encounter Identity
 KIM      ┤               │
 Docs     ┘               ▼
                    Clinical Truth Layer
                           │
       provenance · time · freshness · terminology · units
                           │
                           ▼
                 reconciliation / review
                           │
                           ▼
                    policy enforcement
                      │           │
                      ▼           ▼
                  Human UX    Agent Gateway
                                  │
                          delegated tools only
                                  │
                                  ▼
                       untrusted reasoning worker
```

> **Keep systems of record. Standardize the trustworthy context layer above them.**

---

# Production readiness is deliberately separate

CareOS graduates by evidence-backed gates, not version numbers.

| Gate | Status | Main blocker |
|---|---|---|
| G0 Scope & safety | **EXTERNAL REVIEW** | independent clinical-safety + MDR/MDSW assessment |
| G1 Clinical truth | **BLOCKED** | safe but unusably conservative recall/review burden |
| G2 German interoperability | **PARTIAL** | real KIS/LIS/vendor sandbox + terminology/sync evidence |
| G3 Privacy & security | **PARTIAL** | provider IdP/KMS/audit/DSFA/pentest evidence |
| G4 Reliability | **PARTIAL** | target-environment recovery/failure/SLO evidence |
| G5 Regulatory & quality | **EXTERNAL REVIEW** | formal classification/applicability + quality lifecycle |
| G6 Invisible workflow | **PARTIAL** | real KIS patient-context launch/no-second-search proof |
| G7 Hospital deployment | **PARTIAL** | hospital-specific owners/approvals/evidence |
| G8 Repeatability | **PARTIAL** | Hospital A + different Hospital B/vendor without core fork |
| G9 Germany/EU scale | **BLOCKED** | actual national/EU integrations + multi-site evidence |

**No normal production gate is PASS. Identifiable live patient data remains locked.**

`CAREOS_DATA_MODE=live-readonly` refuses startup while G0–G5 are incomplete. Transactional/write-back mode remains unsupported.

See [GATES](docs/GATES.md), [Safety Case](docs/SAFETY_CASE.md) and [Hospital Assurance Pack](docs/HOSPITAL_ASSURANCE_PACK.md).

---

# Clinical truth: AI is not the source of truth

```text
FHIR / KIS / LIS / documents
             ↓
       source / connector
             ↓
      untrusted candidates
             ↓
 exact source-evidence verification
             ↓
    ClinicalFact / TruthEnvelope
             ↓
 identity · provenance · time · units · terminology · source state
             ↓
 reconciliation / contradiction / review / freshness
             ↓
        policy enforcement
             ↓
          clinician view
```

A surfaced clinical fact preserves source/provenance, original wording/value, timestamps/version where available, explicit clinical time, transformer/model version, trust/review state and exact evidence for document-derived facts.

Models may propose structure. They may **not** silently create trusted clinical truth, invent source offsets/dates, resolve contradictions by confidence, merge patient identities, turn missing data into a negative finding, or autonomously choose treatment/write to production systems.

## Frozen Holdout #3

After replacing unsupported certainty with evidence verification + explicit review barriers, the frozen 500-case synthetic unseen holdout produced:

| Metric | Result |
|---|---:|
| Precision | **100%** |
| Provenance coverage | **100%** |
| Unsupported claims | **0** |
| Wrong-source claims | **0** |
| Critical silent field misses | **0** |
| Critical silent contradiction misses | **0** |
| Recall | **26.32%** |
| Review case rate | **100%** |

This is **not a pass**. The system became safer but far too conservative to solve the workflow. G1 remains BLOCKED and Holdout #3 is not tuning data.

See [Benchmark](docs/BENCHMARK.md).

---

# Agentic CareOS: zero trust for the reasoning worker

CareOS does **not** treat an AI agent as “the doctor, automated.”

> **An agent is a separately identified, narrowly delegated principal. The model may reason; deterministic CareOS policy decides what it can see and do.**

The model cannot choose the organisation, patient, encounter, break-glass state, recursion policy or network destination. Those come from trusted runtime/delegation context.

```text
Clinician / approved workflow
        ↓ explicit delegation
Delegation authority
        ↓ signed narrow token
Workload identity
        ↓
┌──────────────────────────────────┐
│       CAREOS AGENT GATEWAY       │
│                                  │
│ identity + revocation            │
│ single-use delegation            │
│ patient/encounter/task binding   │
│ versioned tool registry          │
│ deterministic authorization      │
│ record/page/tool/runtime budgets │
│ memory namespace                 │
│ audit                            │
│ deny-default egress              │
└──────────────┬───────────────────┘
               │ admitted capabilities only
               ▼
      untrusted reasoning worker
               │ proposes call
               ▼
          Agent Gateway
               │
               ▼
        trusted Tool Proxy
               │
       CareOS truth/connectors
```

Implemented foundations include:

- [`app/agent_delegation.py`](app/agent_delegation.py) — Ed25519-signed delegation;
- [`app/agent_identity.py`](app/agent_identity.py) — separate workload identity/revocation contract;
- [`app/agent_execution_store.py`](app/agent_execution_store.py) — single-use/revocation reference store;
- [`app/agent_tools.py`](app/agent_tools.py) — versioned tool capability registry;
- [`app/agent_runtime.py`](app/agent_runtime.py) — deterministic gateway and runtime-owned budgets;
- [`app/agent_tool_proxy.py`](app/agent_tool_proxy.py) — only trusted tool execution path;
- [`app/agent_worker.py`](app/agent_worker.py) — strict untrusted worker schema and review-only draft firewall;
- [`app/agent_orchestrator.py`](app/agent_orchestrator.py) — identity → replay → gateway execution controller;
- [`app/agent_session.py`](app/agent_session.py) — reasoning worker behind the gateway;
- [`app/agent_audit.py`](app/agent_audit.py) — human + agent + tool attribution;
- [`app/agent_redteam.py`](app/agent_redteam.py) — hostile-worker containment harness;
- [`app/agent_modes.py`](app/agent_modes.py) — synthetic/deidentified/live mode locks.

## Agent phases 1–7

| Phase | Internal state | What it means |
|---|---|---|
| 1 Gateway foundation | **IMPLEMENTED / PARTIAL assurance** | signed delegation, workload identity contract, replay/revocation reference, tool proxy, budgets |
| 2 Reasoning worker | **IMPLEMENTED synthetic** | untrusted worker interface behind gateway; no live PHI |
| 3 Hijacking red team | **IMPLEMENTED synthetic / PARTIAL assurance** | compromised worker attempts exfiltration/cohort search/write and is contained |
| 4 SJK A/B study | **READY TO RUN** | paired CareOS vs CareOS+agent measurement incl. verification decay |
| 5 Deidentified sandbox | **IMPLEMENTED contract / external interface needed** | read-only, no prod credentials, no external egress |
| 6 Shadow live | **IMPLEMENTED BUT LOCKED** | code path exists; cannot enter until G0–G5 + A0–A9 PASS |
| 7 Read-only live assistance | **IMPLEMENTED BUT LOCKED** | source-linked + mandatory human review; no write/send/order |

See [Phases 1–7](docs/AGENT_PHASES_1_7.md), [Agent Security Model](docs/AGENT_SECURITY_MODEL.md), [Agent Production Programme](docs/AGENT_PRODUCTION_PROGRAM.md) and [SJK Agent Study Protocol](docs/SJK_AGENT_STUDY_PROTOCOL.md).

## Independent agent gates

| Agent gate | Status |
|---|---|
| A0 Workload identity | **PARTIAL** |
| A1 Signed delegation / replay | **PARTIAL** |
| A2 Tool least privilege | **PARTIAL** |
| A3 Injection/hijacking resilience | **PARTIAL** |
| A4 Egress / PHI controls | **BLOCKED** |
| A5 Agent audit | **PARTIAL** |
| A6 Memory isolation | **PARTIAL** |
| A7 Blast-radius limits | **PARTIAL** |
| A8 Consequential actions | **BLOCKED** |
| A9 Independent assurance | **EXTERNAL REVIEW** |

No A0–A9 gate is PASS. **Identifiable patient data may not be used by an agent today.** Normal CareOS production readiness would not automatically approve agent use.

The reference deployment includes a deny-all agent-worker network policy artifact at [`deploy/agent-sandbox-networkpolicy.yaml`](deploy/agent-sandbox-networkpolicy.yaml). It is reference architecture, not proof of provider-side network enforcement.

---

# Infectiology first

The Infectiology pack prioritizes:

- specimen + collection time + organism;
- preliminary vs final microbiology;
- susceptibility/resistance;
- anti-infective therapy **as documented**, not recommended by CareOS;
- isolation/infection-prevention status;
- relevant devices;
- fever/inflammatory-marker trends;
- pending cultures/screens/follow-ups;
- provenance for every surfaced fact.

> **Pending ≠ negative. Unavailable ≠ absent.**

The SJK reference is synthetic product research, not an official hospital system or endorsement.

---

# German / EU integration direction

CareOS consumes national/EU rails instead of inventing a parallel stack:

- ISiK / FHIR for hospital interoperability where applicable;
- ISiP for care/nursing contexts where applicable;
- provider/TI identity and treatment-context signals;
- ePA / TI / KIM as ecosystem rails;
- EHDS-forward interoperability/logging documentation.

Current evidence includes real FHIR transport, bounded Bundle pagination and pinned gematik ISiK5 structural/profile validation in CI. ISiK profile validation is explicitly **not** treated as proof of terminology validity or gematik confirmation.

See [National/EU Integration Map](docs/NATIONAL_INTEGRATION_MAP.md).

---

# SJK validation ladder

```text
0. synthetic clinician workflow test
        ↓
1. actual workflow mapping + sponsor decision
        ↓
2. IT / Datenschutz / security discovery
        ↓
3. synthetic/deidentified KIS/LIS sandbox
        ↓
4. independent assurance
        ↓
5. shadow workflow study
        ↓
6. limited live read-only pilot — only if G0–G5 PASS
        ↓
7. second hospital / different vendor
```

The agent lane adds its own A0–A9 gates and never bypasses this ladder.

See [SJK End-to-End Plan](docs/SJK_END_TO_END_PLAN.md), [Team Test Protocol](docs/SJK_TEAM_TEST_PROTOCOL.md), [SJK Agent Study](docs/SJK_AGENT_STUDY_PROTOCOL.md) and [Pilot Measurement Protocol](docs/PILOT_MEASUREMENT_PROTOCOL.md).

---

# Security / production engineering foundations

Current internal evidence includes:

- OIDC/JWT verification foundation;
- treatment-context authorization;
- patient-context binding;
- fail-closed secure reads;
- kill switches;
- PHI-minimized/tamper-evident local audit foundations;
- dependency lock;
- CodeQL;
- scheduled vulnerability audit;
- CycloneDX SBOM;
- Dependabot;
- non-root container;
- live-data startup lock;
- dedicated safety and agent-redteam CI.

Still external before live PHI: provider IdP, KMS/secrets/encryption deployment, protected central audit/SIEM, hospital DSFA/agreements/approval, applicable C5/customer controls, target-environment recovery testing and independent penetration testing.

---

# Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Useful endpoints:

- clinician UI: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`
- normal gate board: `http://127.0.0.1:8000/api/readiness/gates`
- agent gate board: `http://127.0.0.1:8000/api/readiness/agents`
- synthetic agent tool manifest: `http://127.0.0.1:8000/api/agents/synthetic-tools`
- data-mode lock: `http://127.0.0.1:8000/api/readiness/data-mode`

## Tests / CI

```bash
pytest -q
python -m benchmark.redteam_unseen
python scripts/agent_redteam_report.py
```

CI includes regression tests, real HAPI FHIR integration, ISiK5 validation, safety failure injection, frozen G1 evidence, agent containment red-team, CodeQL, dependency vulnerability audit and CycloneDX SBOM.

---

## Safety status

**Synthetic/public prototype only. Not for clinical use.**

CareOS currently performs no production clinical writes, makes no autonomous diagnosis/treatment decisions, does not silently merge ambiguous patients, keeps uncertainty/source failure explicit, and refuses live patient-data startup while core assurance gates are incomplete.

Agent use is stricter: normal CareOS readiness does not imply agent readiness, and live agent modes are separately code-locked behind G0–G5 + A0–A9.

### Product thesis

**One patient. One understandable story. Every source preserved. Less hunting, less duplicate documentation, more time for care.**
