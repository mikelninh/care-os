# CareOS Agents — Phases 1–7 End-to-End

Status: **internal architecture and synthetic/de-identified implementation complete enough for review; live identifiable agent use remains locked.**

Baseline: 2026-08-16.

## Non-negotiable invariant

> The reasoning model is replaceable and untrusted. Patient scope, tools, egress, budgets and effects are owned by deterministic CareOS policy.

## Phase 1 — Agent Gateway foundation

Implemented:
- Ed25519-signed delegation tokens with issuer/audience/key ID/JTI;
- patient + encounter + task + tool + data-category + time + budget binding;
- atomic single-use/revocation reference store;
- workload identity contract separate from human identity;
- credential revocation reference set;
- versioned tool registry;
- deterministic AgentGateway and trusted AgentToolProxy;
- runtime-owned aggregate counters;
- patient-scoped memory namespace;
- structured agent audit events.

Still required for production: provider workload identity, durable distributed replay/revocation store, provider keys, real tool handlers, protected audit/SIEM.

## Phase 2 — Reasoning worker, synthetic only

Implemented:
- strict `AgentToolProposal` schema;
- model cannot choose organisation, patient, encounter, egress, break glass or recursion;
- CareOS injects authoritative context from verified delegation;
- `ReasoningWorker` interface;
- deterministic safe worker and deliberately compromised worker for testing;
- prepared drafts remain review-required and are not clinical truth.

External/model-provider integration is deliberately not required to validate the security boundary. A real model may only be introduced behind this contract with synthetic/de-identified data first.

## Phase 3 — Injection/hijacking red team

Implemented:
- malicious indirect exfiltration case;
- cohort-enumeration case;
- write-escalation case;
- containment criterion based on gateway denial, not model refusal;
- dedicated `agent-redteam` GitHub Actions workflow;
- JSON containment evidence artifact.

Next evidence: larger malicious document/tool/MCP corpus, real model providers, independent red team.

## Phase 4 — SJK synthetic A/B study

Implemented measurement model for paired comparison:
- CareOS vs CareOS + agent;
- task time;
- wrong answers;
- missed pending items;
- source opens;
- corrections;
- effort;
- would-use-tomorrow;
- **verification decay**: increased acceptance without source checking.

There is intentionally no automatic pass rule. Faster output fails if error, omission or unverified acceptance worsens.

Operational next step: run this with Huong first, then ~5–10 SJK Infectiology clinicians using synthetic cases only.

## Phase 5 — De-identified/provider sandbox

Implemented:
- `deidentified-sandbox` operating mode;
- SJK target sandbox profile contract;
- read-only/no-production-credential/no-external-egress invariants;
- target connector shapes: patient/encounter, microbiology, selected labs, documented antimicrobials, pending work;
- identity/audit placeholders explicitly marked TBD until IT discovery.

Cannot complete without actual hospital/vendor interface shapes and an approved de-identification process.

## Phase 6 — Shadow live evaluation

Implemented:
- `shadow-live` operating mode contract;
- agent vs clinician/reference discrepancy model;
- missed/extra item review;
- source-reference requirement;
- explicit unsafe-effect detection;
- **runtime lock:** shadow live is denied while any G0–G5 or A0–A9 gate is not PASS.

When eventually enabled, shadow output must have zero operational effect: no write, send, order or workflow dependency.

## Phase 7 — Controlled read-only assistance

Implemented:
- `read-only-live` operating mode contract;
- AssistanceDraft must include source references;
- mandatory human review;
- `can_write=false`, `can_send=false`, `can_order=false`;
- **runtime lock:** read-only live denied while G0–G5/A0–A9 are incomplete;
- consequential mode is unsupported by current release policy.

Production eligibility additionally requires acceptable shadow evidence and explicit hospital go/no-go.

## Release ladder

```text
Phase 1 Gateway foundation
        ↓
Phase 2 synthetic reasoning
        ↓
Phase 3 hostile-worker containment
        ↓
Phase 4 SJK synthetic A/B clinician study
        ↓
Phase 5 de-identified real-interface sandbox
        ↓
G0–G5 PASS + A0–A9 PASS + independent assurance
        ↓
Phase 6 shadow live, zero operational effect
        ↓
measured safety/usefulness review
        ↓
Phase 7 controlled read-only assistance
```

There is no automatic transition between phases.

## Hard stop conditions

Disable the agent/use case immediately on:
- cross-patient or cross-organisation access;
- unauthorized tool/egress success;
- replayed/revoked identity/delegation accepted;
- memory leakage across patient executions;
- untraceable agent action;
- secrets/credentials exposed to model context;
- critical omission without visible uncertainty;
- meaningful automation-bias/verification-decay signal;
- any write/send/order in a read-only phase;
- failure of mandatory audit, source freshness or patient-context checks;
- behavior regression after agent/model/tool version change.

## Current conclusion

Phases 1–4 are implemented for synthetic internal evidence. Phase 5 is implemented as a de-identified sandbox contract pending real hospital interfaces. Phases 6–7 are implemented as **locked operating modes** so the architecture is ready without falsely enabling live PHI.

No identifiable production agent use is approved today.
