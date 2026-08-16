# ADR-011 — Agents are delegated principals, never human-session proxies

**Status:** Accepted  
**Date:** 2026-08-16

## Context

CareOS may eventually expose clinical context to AI agents or tool-using automation. Agents create a distinct risk class because they interpret untrusted data, dynamically select tools and may execute actions faster and at a larger scale than a human user.

Allowing an agent to reuse a clinician's broad browser session, bearer token or break-glass authority would turn the agent into a confused deputy and make least privilege, attribution and blast-radius control substantially weaker.

## Decision

Every CareOS agent is a **first-class separately identified delegated principal**.

An agent must:

- have its own verifiable workload/agent identity;
- receive a short-lived signed delegation;
- be bound to organisation, purpose, task and patient/encounter where applicable;
- receive only an explicit allowlist of tools and operations;
- have stricter rate/time/data limits than the delegating human;
- never inherit a human browser bearer token;
- never autonomously invoke break glass;
- never gain write capability merely because the human has write capability;
- be attributable separately from the human in audit;
- treat retrieved content/tool metadata as untrusted;
- fail deterministic authorization checks at the tool/data boundary independent of model reasoning.

Agent delegation is non-transitive by default. Sub-agents, if ever supported, must receive strictly narrower explicitly authorized capability envelopes.

## Consequences

Positive:

- lower blast radius for prompt injection or agent hijacking;
- clear human vs agent attribution;
- enforceable least privilege;
- easier token revocation and kill-switch operation;
- agent security can be evaluated independently of model refusal behavior;
- future MCP/tool integrations fit the same authorization architecture.

Costs:

- additional identity/delegation infrastructure;
- tool registry and policy enforcement required;
- more explicit confirmation UX;
- some agent workflows become less convenient than simply reusing human credentials.

These costs are accepted because CareOS handles highly sensitive clinical data.

## Rejected alternatives

### Reuse clinician session/token

Rejected. It provides excessive authority and poor attribution.

### Trust the model/system prompt to obey scope

Rejected. Natural-language instructions are not an authorization boundary.

### Give agents broad read-only access because writes are disabled

Rejected. Confidentiality breaches, cross-patient access and bulk exfiltration remain severe even without writes.

### Allow any user-configured MCP/tool server

Rejected for clinical production. Servers/tools require explicit admission, identity and policy review.

## Related

- `docs/AGENT_SECURITY_MODEL.md`
- ADR-004 models are untrusted
- ADR-006 read/write separation
- ADR-007 patient identity
- `docs/TRUST_AND_DATA_FLOW.md`
- `docs/RISK_REGISTER.md`
