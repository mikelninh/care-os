# CareOS Agent Security Model

Status: proposal-grade security architecture. Agents are **not** authorised for live clinical use merely because this document exists.

## 1. Core rule

> **An AI agent is a separately identified delegated principal, never the clinician and never the system of record.**

A CareOS agent must receive narrower authority than the human/service that delegated the task. It may not inherit a clinician browser session, bearer token, break-glass privilege or unrestricted patient-search capability.

## 2. Threat model

Agents create risks beyond ordinary service accounts because they can interpret untrusted clinical content and dynamically choose tools/actions.

High-concern threats include:

1. **Indirect prompt injection / agent hijacking** — a clinical document, external message, web page or tool result contains instructions that try to redirect the agent.
2. **Confused deputy** — an agent uses legitimate CareOS privileges for a task the initiating user was not authorised to perform.
3. **Excessive agency** — an agent receives more tools, permissions, patients, data categories or autonomy than required.
4. **Cross-patient contamination** — facts or memory from Patient A influence Patient B.
5. **Credential/token theft or replay** — agent credentials are stolen and reused outside the delegated task.
6. **Data exfiltration** — PHI is sent to an unapproved model, MCP server, tool, URL, log, analytics system or support channel.
7. **Tool injection / malicious tool metadata** — a tool/server description or response manipulates agent behavior.
8. **Write escalation** — a read-oriented agent gains the ability to update KIS/LIS/ePA records, send messages, order tests or trigger external workflows.
9. **Break-glass laundering** — an agent inherits or repeatedly invokes emergency access without a contemporaneous human decision.
10. **Unbounded enumeration** — an agent browses large cohorts, staff lists or patient populations beyond the task scope.
11. **Automation bias at scale** — a flawed agent repeats the same mistake across many patients faster than a human could.
12. **Memory leakage** — long-lived agent memory retains PHI or mixes organisations/patients.
13. **Supply-chain/tool compromise** — a model, MCP server, plugin, connector or model-hosting component is compromised.
14. **Audit ambiguity** — logs attribute the action only to the human, hiding what the agent actually decided or called.
15. **Availability/resource abuse** — runaway loops or recursive agents exhaust FHIR/KIS/model capacity.

## 3. Delegated authority envelope

Every agent execution must be bound to an explicit signed delegation envelope containing at minimum:

- `agent_id` and agent/version identity;
- `delegating_actor`;
- `organisation`;
- exact `patient_ref` and `encounter_ref` where applicable;
- approved purpose/task identifier;
- allowed data categories;
- allowed tools;
- allowed operations (`read`, `prepare`, etc.);
- prohibited operations;
- maximum records/results/pages;
- maximum tool calls / execution time;
- egress policy;
- memory policy;
- start time and short expiry;
- unique execution/session ID;
- human-confirmation requirements.

Authority must be **non-transitive by default**. An agent may not mint another equally privileged agent unless an explicitly approved orchestration policy allows a strictly narrower sub-delegation.

## 4. Agent identity

Agents require first-class identity separate from human users.

Required production properties:

- workload identity or cryptographically verifiable agent identity;
- short-lived credentials;
- audience-bound tokens;
- organisation-bound delegation;
- patient/task-bound authorization;
- no reuse of human browser bearer tokens;
- no shared generic `careos-agent` production account;
- revocation/kill switch per agent and per execution;
- version identity included in audit.

## 5. Default permissions

Default agent capability is **no patient access**.

The preferred ladder is:

```text
none
  ↓ explicit delegation
read minimum-necessary source data
  ↓ explicit task policy
prepare draft / structured candidate
  ↓ human review
human performs consequential action
```

Production agents are **not** permitted by default to:

- search arbitrary patients;
- enumerate cohorts;
- invoke break glass;
- change allergies/medications/diagnoses;
- place/cancel orders;
- send external communications;
- write to KIS/LIS/ePA;
- alter access policy;
- alter audit records;
- change CareOS safety configuration;
- export patient data;
- call arbitrary URLs or arbitrary MCP servers.

Any future write capability is a separate production programme and must be granted at the tool/API boundary, not merely requested in natural language.

## 6. Tool security boundary

Tool availability is determined by policy, **not by the model**.

Each tool must declare machine-enforceable metadata:

- stable tool ID/version;
- owner/trust tier;
- read/write effect;
- PHI categories accepted/returned;
- target system;
- network destination;
- maximum scope;
- idempotency/replay behavior;
- audit requirements;
- required human confirmation;
- timeout/rate limits.

The agent may only choose among tools already admitted into its signed delegation envelope.

Tool descriptions, model-produced arguments, external content and MCP/tool responses are treated as untrusted input.

## 7. Prompt-injection / content boundary

Clinical documents, emails, web pages, PDFs, scanned text, user-generated notes and tool outputs are **data**, never trusted policy instructions.

Controls:

- system/policy instructions originate outside retrieved clinical content;
- retrieved content is labelled with source/trust metadata;
- model outputs cannot modify authorization policy;
- high-risk actions require deterministic policy checks after model reasoning;
- tool arguments are schema validated and independently authorized;
- arbitrary URL fetching is disabled unless explicitly required;
- secrets/tokens are never placed in model-visible prompts;
- prompt-injection attempts are logged as security signals where feasible;
- attack strings must be part of agent red-team evaluation.

The security design assumes prompt injection may never be solved perfectly at the model layer. Damage is therefore bounded by **capability isolation and least privilege**.

## 8. Patient-context isolation

Each agent execution is patient-scoped by default.

Rules:

- patient identity is fixed before clinical retrieval;
- a tool result with a mismatched patient is rejected;
- no cross-patient shared conversational memory;
- caches/memory are namespaced by organisation + patient + execution;
- agent context is destroyed or retained only under explicit policy after completion;
- cohort-level agents require a separate approved analytics/research purpose and are not a hidden extension of bedside access.

## 9. Model and egress policy

A model is never implicitly allowed to receive PHI because an agent needs reasoning.

Each deployment must define:

- approved model(s) and hosting location;
- whether identifiable data may leave provider boundary;
- exact permitted fields;
- retention/training policy;
- subprocessor chain;
- network egress allowlist;
- encryption;
- prompt/tool logging policy;
- fallback when model is unavailable.

If the task can be completed without identifiable PHI leaving the provider data plane, that is the preferred design.

## 10. Human confirmation

Consequential operations require explicit human confirmation at the moment of action.

A confirmation UI must show:

- what the agent wants to do;
- which patient/encounter;
- which source facts support it;
- destination system/recipient;
- exact data leaving CareOS;
- whether the operation changes a record or communicates externally.

A generic confirmation such as “allow agent to help with this patient today” is insufficient for consequential actions.

## 11. Break glass

Agents cannot autonomously invoke break glass.

If future emergency workflows include agents:

1. a human initiates break glass;
2. the human supplies the reason;
3. the resulting agent delegation is short-lived and task-scoped;
4. the agent identity and human sponsor are both audited;
5. post-event review distinguishes human decision from agent actions.

## 12. Audit / non-repudiation

Every agent action must produce an audit chain that identifies:

- human delegator;
- agent identity + version;
- execution/session ID;
- patient/encounter scope;
- task/purpose;
- source resources accessed;
- tools considered/called;
- deterministic authorization decision;
- model/provider where relevant;
- data egress destination/category;
- human confirmations;
- final outcome/error/abstention;
- break-glass context if applicable.

Do not log unrestricted prompts/clinical free text to generic telemetry.

## 13. Rate, blast-radius and loop controls

Every agent execution has hard ceilings:

- patients per execution;
- records/pages retrieved;
- tool calls;
- recursion/sub-agent depth;
- elapsed time;
- tokens/model cost;
- outbound requests;
- write/communication count (future only).

Exceeding a ceiling stops the agent and creates a reviewable event.

## 14. MCP / external tool servers

MCP or equivalent tool protocols are **not** implicitly trusted.

Production policy:

- only allowlisted servers/endpoints;
- strong server identity and TLS;
- OAuth/short-lived authorization where applicable;
- least-privilege scopes;
- no token passthrough from a user to arbitrary downstream servers;
- exact redirect URI validation for authorization flows;
- tool schemas pinned/versioned;
- server/tool metadata treated as untrusted input;
- no arbitrary user-added MCP server in clinical production;
- server changes trigger security/conformance review.

## 15. Agent-specific release gates

No agent may access identifiable live patient data until all normal CareOS G0–G5 gates pass **and** these agent gates pass:

| Agent gate | Requirement |
|---|---|
| A0 Identity | separate verifiable agent/workload identity |
| A1 Delegation | patient/task/tool/time bounded signed delegation |
| A2 Tool least privilege | allowlisted tools + deterministic authorization |
| A3 Injection resilience | adversarial content/tool red-team with bounded blast radius |
| A4 Egress | explicit PHI/model/tool destination policy + tests |
| A5 Audit | agent + human + tool attribution and integrity |
| A6 Memory isolation | patient/org isolation + retention tests |
| A7 Abuse limits | rate/loop/recursion/patient ceilings |
| A8 Consequential action | human confirmation; write-back remains disabled until separately approved |
| A9 Independent review | security/clinical safety review of the actual agent use case |

**Current status: all A0–A9 are NOT PASS for identifiable production use.**

## 16. Required adversarial tests

Before production, simulate at least:

- malicious instruction embedded in a lab result/comment;
- prompt injection inside a PDF/discharge letter;
- malicious MCP/tool description;
- tool response requesting secrets or a second tool call;
- patient A content instructing retrieval of Patient B;
- agent asked to enumerate all HIV patients;
- agent asked to export records to an external URL;
- agent asked to ignore treatment-context policy;
- stolen/replayed delegation token;
- expired delegation token;
- agent tries to invoke break glass;
- agent tries a write tool absent from its envelope;
- recursive agent spawning;
- runaway pagination/tool loop;
- compromised model suggesting policy bypass;
- external model outage;
- agent version changes behavior on same test corpus.

The test passes when **policy and capability boundaries prevent harm**, not merely when the model refuses the malicious instruction.

## 17. Safe first agent use cases

The first acceptable CareOS agent experiments should be low-consequence and synthetic/de-identified, for example:

- prepare a source-linked morning-review draft;
- identify which synthetic results are still pending;
- draft a handover from already surfaced CareOS facts;
- compare two synthetic source versions and flag differences;
- assemble an evidence bundle for human review.

Do not begin with autonomous ordering, prescribing, patient messaging, record modification or broad patient search.

## 18. Architectural invariant

> **Agents may propose, retrieve and prepare within a narrow delegated envelope. Deterministic CareOS policy—not the model—decides what data or tools they are permitted to access.**
