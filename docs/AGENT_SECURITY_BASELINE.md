# CareOS Agent Security Baseline

Status: current external-security baseline for architecture review. Checked **2026-08-16**.

This document is not a certification claim. It records external direction that informs the CareOS agent security model and should be re-checked before any production proposal or deployment.

## NIST — agent identity, authorization and audit

NIST NCCoE's 2026 concept paper on software and AI-agent identity/authorization explicitly calls out the need to address:

- identification of AI/software agents;
- authorization;
- auditing;
- non-repudiation;
- prompt-injection prevention/mitigation.

CareOS response:

- agent identity is separate from human identity;
- patient/task/tool/time delegation is explicit and narrower than the delegator;
- each tool call is deterministically re-authorized;
- human + agent + delegation + tool are separately attributable in audit;
- prompt injection is assumed possible, so capability boundaries limit blast radius.

Source checked:

- https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd

## NIST CAISI — indirect prompt injection remains an open security problem

NIST CAISI reported in March 2026 that a large public agent red-team competition found at least one successful agent-hijacking attack against every evaluated frontier model. The relevant threat is indirect prompt injection: malicious instructions are embedded in content such as external data and cause an agent to attempt unintended actions or exfiltration.

CareOS response:

> Security acceptance never depends on the model refusing the hostile instruction. The Agent Gateway must prevent the unauthorized tool/data/egress/action even when the reasoning worker is compromised.

Source checked:

- https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition

## MCP — current authorization direction

The MCP project released specification version **2026-07-28** with authorization hardening and a stateless request/response core. The current direction strengthens resource/audience binding and authorization metadata rather than relying on broad token passthrough.

For CareOS, any MCP or MCP-like server is treated as an external tool boundary, not an implicitly trusted extension.

Required CareOS constraints include:

- allowlisted server identity/endpoints;
- resource/audience-bound authorization;
- short-lived credentials;
- no clinician bearer-token passthrough to arbitrary servers;
- exact redirect/authorization metadata validation where applicable;
- pinned/versioned tool schemas;
- tool metadata/results treated as untrusted input;
- gateway policy remains authoritative even if an MCP server/tool attempts instruction injection.

Sources checked:

- https://blog.modelcontextprotocol.io/posts/2026-07-28/
- https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization

## CareOS security design implication

The external baseline supports the architectural choice that an agent should be treated as a **software workload with explicit identity and delegated authority**, not as a conversational proxy that automatically inherits a human user's rights.

This baseline should be reviewed at least when:

- an agent gains a new tool or data category;
- a model/provider changes;
- MCP protocol/auth implementation changes;
- a deployment enables network egress;
- patient search/cohort capability is proposed;
- any consequential action is proposed;
- a material NIST/BSI/gematik/EU agent-security baseline changes.
