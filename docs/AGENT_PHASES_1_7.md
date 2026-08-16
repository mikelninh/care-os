# CareOS Agents — Phases 1–7 End-to-End

Status: **internal architecture plus synthetic/de-identified implementation complete enough for serious review; identifiable live agent use remains locked.**

Baseline: 2026-08-16.

## Non-negotiable invariant

> The reasoning model is replaceable and untrusted. Patient scope, identity, tools, egress, budgets and effects are owned by deterministic CareOS policy.

The security pass criterion is not that a model refuses a malicious instruction. It is that a compromised worker still cannot exceed its delegated capability envelope.

## Phase 1 — Agent Gateway foundation

Implemented:

- Ed25519-signed delegation tokens with issuer/audience/key ID/JTI;
- patient + encounter + task + tool + data-category + time + budget binding;
- atomic single-use/revocation reference store;
- workload identity contract separate from human identity;
- credential revocation reference set;
- versioned tool registry;
- deterministic `AgentGateway` and trusted `AgentToolProxy`;
- runtime-owned aggregate counters;
- patient/encounter/execution-scoped memory namespace;
- structured agent audit events;
- orchestration controller enforcing mode → workload identity → revocation → one-time delegation → gateway.

Still required for production:

- provider workload identity;
- durable distributed replay/revocation store;
- provider-managed signing/key lifecycle;
- real provider tool handlers/connectors;
- protected audit/SIEM.

## Phase 2 — Reasoning worker, synthetic/de-identified only

Implemented:

- strict `AgentToolProposal` schema;
- model cannot choose organisation, patient, encounter, egress, break glass or recursion;
- CareOS injects authoritative context from verified delegation;
- `ReasoningWorker` interface;
- deterministic safe worker and deliberately compromised worker;
- provider-neutral HTTPS JSON model adapter restricted to `synthetic` and `deidentified-sandbox` modes;
- exact model endpoint host policy;
- first adapter forbids retention/training on supplied context;
- model/provider responses schema-validated before reaching the gateway;
- minimum-data model projection keeps only delegated source-linked categories and omits direct identifier fields from the fixed projection shape;
- prepared drafts remain source-linked, review-required and outside trusted clinical truth.

A real model provider is intentionally **not yet approved for live PHI**. The adapter exists so candidate providers/models can be evaluated behind the same deterministic boundary with synthetic/de-identified data first.

## Phase 3 — Injection / hijacking containment

Implemented synthetic hostile-worker corpus currently covers:

1. indirect exfiltration;
2. cohort/all-patient enumeration;
3. clinical write escalation;
4. hidden/admin-tool invocation;
5. undelegated sensitive-category expansion;
6. external-send attempt.

Additional schema tests prove the reasoning worker cannot express authoritative patient/organisation/encounter, break-glass, egress or recursion overrides.

Evidence:

- dedicated `.github/workflows/agent-redteam.yml`;
- agent-specific security tests;
- JSON `careos-agent-redteam-evidence` artifact;
- containment succeeds only when deterministic policy denies every harmful capability attempt.

Still required:

- broader malicious document/PDF/email/tool/MCP corpus;
- actual candidate model/provider testing;
- independent security red team.

## Phase 4 — SJK synthetic A/B clinician study

Implemented:

- paired study measurement model for CareOS vs CareOS + agent;
- task time;
- wrong answers;
- missed pending items;
- source opens;
- corrections;
- effort;
- would-use-tomorrow;
- **verification decay**: increased acceptance without source checking;
- standalone browser study page with no backend upload.

Synthetic A/B page:

**https://mikelninh.github.io/careos/sjk/agent.html**

There is intentionally no automatic pass rule. Faster output fails if errors, omissions, unverified acceptance or cognitive burden worsen.

Operational next step: run first with Huong as a usability sanity check, then approximately 5–10 voluntarily participating SJK Infectiology clinicians if locally appropriate.

## Phase 5 — De-identified/provider sandbox

Implemented:

- `deidentified-sandbox` operating mode;
- SJK target sandbox profile contract;
- read-only / no-production-credentials / no-external-egress invariants;
- target connector shapes: patient/encounter, microbiology, selected labs, documented antimicrobials, pending work;
- identity/audit placeholders explicitly TBD until hospital IT discovery;
- model adapter allowed only under an approved synthetic/de-identified endpoint policy;
- deny-all agent-worker Kubernetes NetworkPolicy reference artifact.

Cannot complete without:

- actual SJK/provider interface shapes;
- approved de-identification process;
- provider test identity/audit endpoints;
- provider-enforced network isolation.

The Kubernetes policy is reference architecture, **not evidence that SJK or another hospital currently enforces it**.

## Phase 6 — Shadow live evaluation

Implemented:

- `shadow-live` operating-mode contract;
- agent vs clinician/reference discrepancy model;
- missed/extra item review;
- source-reference requirement;
- unsafe-effect detection;
- runtime lock: shadow live is rejected while any G0–G5 or A0–A9 gate is not PASS.

When eventually enabled, shadow output has **zero operational effect**:

- no source-system write;
- no order;
- no message;
- no patient communication;
- no downstream workflow may depend on the agent output.

Required evidence before transition: all core/agent gates, hospital approval, independent assurance and a named shadow-study protocol/stop owner.

## Phase 7 — Controlled read-only assistance

Implemented:

- `read-only-live` operating-mode contract;
- source-linked `AssistanceDraft`;
- mandatory human review;
- `can_write=false`;
- `can_send=false`;
- `can_order=false`;
- runtime lock while G0–G5/A0–A9 are incomplete;
- consequential mode explicitly unsupported by current release policy.

Production eligibility additionally requires acceptable Phase-6 shadow evidence and explicit clinical/IT/security/Datenschutz go/no-go.

## End-to-end execution chain

```text
approved human/workflow
        ↓
signed delegation authority
        ↓
separate workload identity
        ↓
revocation + one-time activation
        ↓
CareOS Agent Gateway
        ↓
untrusted reasoning worker
        ↓ strict proposal schema
CareOS binds authoritative patient/task context
        ↓
Agent Gateway re-authorizes
        ↓
trusted Tool Proxy
        ↓
CareOS truth/connectors
        ↓
source-linked review-only draft
        ↓
audit + consume delegation
```

A denied/harmful worker request aborts the execution and revokes the reference delegation rather than allowing a later request to continue inside the same run.

## Release ladder

```text
Phase 1 Gateway foundation
        ↓
Phase 2 synthetic/de-identified reasoning
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

**Phases 1–3:** implemented for internal synthetic/de-identified security evidence.  
**Phase 4:** implemented and ready for the first human synthetic A/B test.  
**Phase 5:** provider/de-identified sandbox architecture implemented; real hospital interfaces are the blocker.  
**Phases 6–7:** code contracts exist but are intentionally hard-locked until normal and agent production gates plus external assurance are complete.

No identifiable production agent use is approved today.
