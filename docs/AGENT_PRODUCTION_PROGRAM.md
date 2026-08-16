# CareOS Agent Production Programme

Status: **implementation programme — agents are not approved for identifiable live clinical use**.

Baseline: 2026-08-16.

## Mission

Build agent capability without turning a probabilistic model into a security principal, policy engine, clinical truth authority or autonomous clinical actor.

> **The model may reason. The CareOS Agent Gateway decides what the agent can see and do.**

The programme is intentionally separate from normal CareOS G0–G9. Normal production readiness never implies agent readiness.

## Target architecture

```text
Clinician / approved workflow
          │
          │ authenticated explicit delegation
          ▼
┌───────────────────────────────────────────────┐
│              CAREOS AGENT GATEWAY             │
│                                               │
│ workload identity                             │
│ signed delegation verification                │
│ patient + encounter + task binding            │
│ tool registry + risk metadata                 │
│ deterministic authorization                   │
│ egress allowlist                              │
│ budgets / loop / recursion limits             │
│ memory namespace                              │
│ audit / non-repudiation                       │
│ human confirmation boundary                   │
└──────────────────────┬────────────────────────┘
                       │ narrow admitted tools only
                       ▼
             untrusted reasoning worker
                       │
                 proposes tool calls
                       │
                       ▼
             Agent Gateway re-authorizes
                       │
            ┌──────────┴───────────┐
            ▼                      ▼
     approved read tool      prepared draft
            │                      │
            ▼                      ▼
     CareOS truth layer        human review
```

No model call is security-critical. A fully hijacked model must remain bounded by the gateway.

## Production principles

1. **Agents are delegated principals, never human-session proxies.**
2. **No patient access by default.**
3. **One patient / encounter / task per bedside execution by default.**
4. **Tool availability is policy, not prompt.**
5. **Read, prepare, communicate and write are distinct capabilities.**
6. **All model/tool content is untrusted input.**
7. **Prompt-injection resistance is based on blast-radius containment, not model refusal.**
8. **No arbitrary patient search for bedside agents.**
9. **No arbitrary network egress.**
10. **No long-lived cross-patient memory.**
11. **Every action attributes both human delegator and agent identity/version.**
12. **Break glass remains a human act.**
13. **Consequential actions require separate human confirmation at action time.**
14. **Sub-delegation is disabled by default.**
15. **Agent versions are evaluated like safety-relevant software changes.**

## Workstreams

### W0 — Use-case and intended-purpose firewall

First production-eligible use case: **source-linked morning-review / handover preparation from already admitted CareOS facts**.

Allowed first scope:

- read minimum-necessary CareOS facts for the current patient/encounter;
- inspect pending vs final state;
- prepare a draft summary/handover;
- cite supporting CareOS fact/source identifiers;
- abstain/escalate.

Not allowed:

- diagnosis;
- treatment recommendation;
- prescribing/order placement;
- direct patient communication;
- KIS/ePA write-back;
- cohort search;
- external web research with PHI;
- autonomous break glass.

Exit evidence: named intended purpose, clinical-safety review, regulatory impact review.

### W1 — Agent/workload identity (A0)

Build:

- first-class `agent_id` + version;
- cryptographically verifiable workload identity in production;
- short-lived audience-bound credentials;
- revocation/kill switch;
- no shared generic production agent account.

Internal implementation can define the contract; PASS requires real provider/workload identity infrastructure.

### W2 — Signed delegation (A1)

Build:

- cryptographically signed delegation envelope;
- unique delegation/execution ID;
- issuer + key ID;
- organisation/patient/encounter/task binding;
- allowed operations/tools/data categories;
- expiry/not-before;
- budget limits;
- egress policy;
- replay protection contract.

No human bearer token is passed to the model or downstream tools.

### W3 — Tool registry and least privilege (A2)

Every tool gets immutable/versioned metadata:

- stable tool ID/version;
- owner/trust tier;
- effect (`read`, `prepare`, future consequential class);
- target system;
- data categories;
- patient scoping;
- egress destination;
- max records/pages;
- timeout/rate limits;
- idempotency/replay semantics;
- audit requirement;
- human confirmation requirement.

The model only sees tools already admitted by the gateway.

### W4 — Agent execution sandbox

Build a state machine for each execution:

```text
CREATED → ACTIVE → COMPLETED
               ↘ DENIED
               ↘ ABORTED
               ↘ EXPIRED
```

Track deterministically:

- tool-call count;
- pages/records;
- elapsed runtime;
- external calls;
- recursion depth;
- current patient/encounter/task;
- model + agent version;
- kill-switch state.

No model-controlled counter or timeout.

### W5 — Memory isolation (A6)

Memory namespace:

```text
organisation / patient / encounter / execution
```

Rules:

- no global clinical conversational memory;
- no patient-A material in patient-B context;
- execution-local memory is destroyed by default;
- any retained derived state has purpose + retention + provenance + deletion policy;
- cohort/research memory is a different product purpose and permission model.

### W6 — Egress/data-loss prevention (A4)

Build:

- deny-by-default network policy;
- exact host/service allowlist;
- per-tool egress declaration;
- minimum-data projection before any model/tool call;
- PHI category enforcement;
- no secrets/tokens in prompts;
- no unrestricted prompts in generic telemetry;
- model/subprocessor inventory.

PASS requires target-environment controls and tests, not only application policy.

### W7 — Agent audit / non-repudiation (A5)

Each execution records structured events for:

- human delegator;
- agent ID/version;
- delegation/execution ID;
- patient pseudonymous reference;
- task/purpose;
- tool requested;
- authorization decision/reason;
- source/resource categories accessed;
- model/provider where relevant;
- egress host/category;
- human confirmation;
- outcome/abstention/error;
- limits exceeded / injection signals.

No raw clinical free text in generic audit telemetry.

### W8 — Human confirmation and consequential actions (A8)

First production programme keeps consequential actions disabled.

Future confirmation must be **action-specific**, displaying:

- exact patient/encounter;
- exact proposed action;
- destination system/recipient;
- supporting source facts;
- exact data leaving CareOS;
- record mutation/communication consequences.

A generic session-level “agent may act for me” consent is insufficient.

### W9 — Injection/hijacking red team (A3)

Test malicious content in:

- discharge letter/PDF;
- lab comments;
- KIM/email/message;
- tool metadata;
- tool result;
- external page;
- model-generated tool arguments.

Primary success criterion:

> Even if the model follows the malicious instruction, deterministic policy prevents unauthorized patient access, tools, egress and consequential action.

### W10 — Abuse/availability controls (A7)

Build/test:

- record/page/tool limits;
- runtime deadline;
- recursion disabled by default;
- per-agent and per-provider rate limits;
- source-system back-pressure;
- circuit breakers;
- cost/token ceilings;
- mass-action detection;
- kill switch per agent/version/execution/tool.

### W11 — Independent review (A9)

Before identifiable PHI:

- independent security red team;
- clinical-safety review;
- Datenschutz review of agent/model/tool data flows;
- regulatory/intended-purpose review;
- actual hospital CISO/IT acceptance;
- provider-specific model/subprocessor approval.

## Agent gates

| Gate | Internal target | PASS evidence |
|---|---|---|
| A0 Identity | workload-identity contract | real verifiable provider workload identity + revocation test |
| A1 Delegation | signed narrow envelope | production signer/verifier + replay/expiry/audience tests |
| A2 Tool least privilege | versioned registry + gateway | all production tools registered and policy-tested |
| A3 Injection resilience | adversarial harness | independent red team; hostile model remains bounded |
| A4 Egress | deny-default app/network model | provider network/DLP/allowlist evidence |
| A5 Audit | structured agent events | provider protected audit/SIEM + integrity/review test |
| A6 Memory | strict execution namespace | retention/isolation/deletion tests |
| A7 Abuse limits | deterministic budgets | load/rate/circuit-breaker/kill-switch tests |
| A8 Consequential action | disabled initially | later action-specific confirmation + separate release gate |
| A9 Independent review | review package | named qualified reviewers and accepted residual risk |

## End-to-end release ladder

### Agent Stage 0 — deterministic synthetic gateway

No model required. Prove identity/delegation/tool/budget/audit boundaries with synthetic data.

### Agent Stage 1 — synthetic reasoning worker

Connect a model only to synthetic CareOS facts. Run injection and malicious-tool tests.

### Agent Stage 2 — SJK synthetic morning-review study

Clinicians compare normal CareOS vs agent-prepared draft using synthetic cases. Measure:

- completion time;
- corrections;
- source checks;
- omitted pending items;
- unsafe trust/rubber-stamping;
- usefulness;
- review burden.

### Agent Stage 3 — de-identified/provider sandbox

Real interface shape, no identifiable production care. Validate source load, context launch, agent gateway and protected audit.

### Agent Stage 4 — shadow read-only live pilot

Eligible only after normal G0–G5 and A0–A9 PASS. Agent prepares output; clinician workflow does not depend on it; no writes/sends.

### Agent Stage 5 — controlled read-only assistance

Only after shadow evidence and explicit hospital go/no-go. Still no autonomous consequential action.

### Agent Stage 6 — future consequential-action programme

Separate intended purpose, safety case, regulatory/privacy/security review. Not inherited from read-only approval.

## Stop conditions

Immediately disable an agent version/use case if any of these occurs:

- cross-patient access or contamination;
- unauthorized tool/egress success;
- inability to attribute an action to agent + delegator;
- secret/token reaches model-visible content;
- critical clinical omission caused by agent output without visible uncertainty;
- agent bypasses confirmation or treatment-context policy;
- mass execution outside approved scope;
- memory isolation failure;
- repeated injection success with meaningful blast radius;
- audit/SIEM failure where audit is required;
- unexplained behavioral regression after model/agent/tool update.

## Immediate implementation order

1. signed delegation token contract;
2. versioned tool registry;
3. deterministic execution gateway/budget state;
4. memory namespace contract;
5. structured agent audit events;
6. A0–A9 readiness manifest/API;
7. adversarial tests;
8. synthetic SJK morning-review agent behind the gateway;
9. clinician evaluation protocol;
10. external assurance before any identifiable live use.
