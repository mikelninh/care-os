# CareOS Risk Register

Status: initial living risk register. Severity/probability scales and residual-risk acceptance require qualified clinical/regulatory review before live deployment.

| ID | Hazard | Potential harm | Current controls/evidence | Current state | Required next evidence |
|---|---|---|---|---|---|
| R1 | Wrong patient context | Clinician acts on another patient's information | `TruthEnvelope` cross-patient rejection; context binding; treatment-context policy | OPEN / high concern | real KIS identity/context integration + adversarial wrong-patient testing + clinical review |
| R2 | Unsupported extracted fact | False clinical belief | exact document evidence-span firewall; untrusted extractor boundary | OPEN / high concern | new extractor + future untouched holdout + unsupported-claim release threshold |
| R3 | Hidden contradiction | One conflicting source silently wins | governed contradiction engine; frozen red-team metric | OPEN / high concern | new contradiction architecture evaluation; critical silent-miss threshold met |
| R4 | Stale data shown as current | Outdated clinical belief | explicit source state/currentness; stale truth withheld in secure read coordinator | OPEN | real source freshness policy + failure injection |
| R5 | Source outage looks like absence | Missing result interpreted as negative | unavailable source returns null truth/count unknown; secure read withholds | CONTROL DESIGNED | real connector outage tests and UI verification |
| R6 | Incomplete FHIR search | Important records silently omitted | bounded pagination; loops/max-page/cross-origin continuation fail closed | CONTROL IMPLEMENTED (generic FHIR) | real vendor pagination/load test |
| R7 | Unauthorized patient access | Confidentiality/privacy breach | asymmetric JWT verifier; role/scope/treatment-context policy; break-glass semantics | OPEN | hospital IdP/context integration + immutable audit + pen test |
| R8 | Audit unavailable | Untraceable access | secure read withholds patient truth if required success audit fails | CONTROL DESIGNED | production immutable audit/SIEM + outage test |
| R9 | Clinical write-back error | Source record corrupted / unsafe action | transactional/live write-back unsupported; runtime controls default prepared outputs off | CONTROLLED BY SCOPE | separate programme before any write-back |
| R10 | Model/version regression | Previously safe workflow becomes unsafe | transformer versions on facts; gate/CI discipline | OPEN | release comparison suite + model/data version registry + rollback evidence |
| R11 | Guideline drift | Old/withdrawn guidance shown as current | governed source watcher/review architecture | OPEN | approved version registry + clinician governance evidence |
| R12 | PHI leakage in telemetry/support | Confidentiality breach | audit schema forbids clinical text fields; provider-data-plane preference | OPEN | production telemetry review + DLP/log tests + support-access policy |
| R13 | Dependency/supply-chain compromise | Service/security/integrity impact | pinned dependencies; SBOM; dependency scanning; CodeQL; release discipline | OPEN | signed release/provenance + deployment-specific supply-chain review |
| R14 | Automation bias / rubber-stamp review | Incorrect output accepted without verification | source/provenance visible; uncertainty states | OPEN | clinician usability study measuring verification behavior |
| R15 | Regulatory scope drift | Uncontrolled MDSW/AI Act obligations and risk | written intended purpose; G0/G5 external review gate | OPEN | independent qualification/classification + change-control process |
| R16 | Agent hijacking / indirect prompt injection | Agent follows hostile instructions embedded in clinical/external data | agent model requires data/content to remain untrusted; deterministic tool/data authorization; narrow delegation | OPEN / critical | adversarial agent-hijacking suite + independent security review |
| R17 | Excessive agent authority | Bulk confidentiality/integrity impact from one compromised/mistaken agent | separate agent identity; proposed signed patient/task/tool/time envelope; no default write/break-glass | OPEN / critical | implemented agent identity/delegation/policy enforcement + red team |
| R18 | Cross-patient agent memory/context | PHI or clinical reasoning from Patient A leaks into Patient B | proposed per-org/patient/execution memory namespace; no shared patient memory | OPEN / critical | implemented memory isolation + adversarial cross-patient tests |
| R19 | Agent audit ambiguity | Harm cannot be attributed to human vs agent/model/tool | proposed dual human+agent+execution+tool audit chain | OPEN / high concern | production audit schema + integrity/non-repudiation tests |
| R20 | Malicious/compromised MCP or tool server | PHI exfiltration, credential theft, policy bypass or harmful actions | proposed allowlist, server identity, short-lived auth, tool schema/version policy | OPEN / critical | controlled tool registry + server admission process + hostile-tool tests |
| R21 | Runaway/bulk agent execution | KIS/LIS overload, broad patient enumeration, repeated unsafe action | proposed hard ceilings on patients/pages/tools/time/recursion/egress | OPEN / high concern | implemented quotas/rate limits/loop detection + load/abuse tests |
| R22 | Agent credential theft/replay | Unauthorized automated access to clinical data | proposed short-lived audience-bound task-scoped credentials + revocation | OPEN / critical | workload identity/delegation implementation + replay/expiry tests |
| R23 | Agent egress to unapproved model/tool | PHI disclosed to external party/subprocessor | provider-side PHI principle; proposed explicit agent egress allowlist and field policy | OPEN / critical | DLP/egress enforcement + deployment-specific model/tool contracts and tests |

## Agent-specific rule

An agent is never treated as the clinician. It must be a separately identified delegated principal with **less authority** than its human/service sponsor. Natural-language instructions and model refusal behavior are not authorization boundaries. See `docs/AGENT_SECURITY_MODEL.md` and ADR-011.

## Risk handling rule

- No risk is “closed” because code exists.
- Safety-critical risks require verification evidence and named acceptance ownership.
- Any release-changing truth, identity, authorization, clinical scope, agent capability or write capability must update this register.
- New evidence may increase risk ratings; that is a measurement improvement, not a project failure.
