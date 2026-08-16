from __future__ import annotations


def agent_gate_manifest() -> dict:
    gates = [
        {
            "id": "A0", "name": "Agent/workload identity", "status": "PARTIAL",
            "evidence": ["first-class agent/version contract", "workload identity binding contract", "credential revocation reference implementation"],
            "blockers": ["real provider workload identity issuer", "provider credential rotation/revocation evidence"],
        },
        {
            "id": "A1", "name": "Signed delegation", "status": "PARTIAL",
            "evidence": ["Ed25519 signed delegation", "issuer/audience/key validation", "patient/encounter/task/tool/time/budget binding", "atomic single-use/revocation reference store"],
            "blockers": ["durable shared replay store", "production delegation authority and key lifecycle"],
        },
        {
            "id": "A2", "name": "Tool least privilege", "status": "PARTIAL",
            "evidence": ["versioned ToolSpec registry", "deterministic AgentGateway", "trusted tool proxy", "model cannot choose patient/org/encounter/egress/break-glass fields"],
            "blockers": ["real provider tools behind proxy", "provider tool conformance evidence"],
        },
        {
            "id": "A3", "name": "Injection/hijacking resilience", "status": "PARTIAL",
            "evidence": ["compromised-worker harness", "six malicious exfiltration/cohort/write/admin/category-expansion attempts contained by deterministic policy", "dedicated agent-redteam CI artifact"],
            "blockers": ["real model/provider red team", "larger malicious document/tool/MCP corpus", "independent red team"],
        },
        {
            "id": "A4", "name": "Egress / PHI controls", "status": "BLOCKED",
            "evidence": ["deny-by-default egress in delegation/tool/gateway contracts", "synthetic and deidentified modes default to no external egress", "fixed minimum-data model projection strips direct identifier fields and requires source-linked delegated categories", "reference deny-all agent network policy"],
            "blockers": ["provider network egress proxy/allowlist/DLP", "approved model/subprocessor data flow", "network enforcement outside application process"],
        },
        {
            "id": "A5", "name": "Agent audit / non-repudiation", "status": "PARTIAL",
            "evidence": ["human+agent+version+delegation+tool audit schema", "PHI-minimized identifiers", "synthetic end-to-end agent audit preview"],
            "blockers": ["protected provider audit/SIEM", "integrity/non-repudiation review", "operational review workflow"],
        },
        {
            "id": "A6", "name": "Memory isolation", "status": "PARTIAL",
            "evidence": ["organisation/patient/encounter/execution-scoped namespace", "no persistent memory in first synthetic agent"],
            "blockers": ["real memory store", "retention/deletion proof", "cross-patient leakage test with real model runtime"],
        },
        {
            "id": "A7", "name": "Abuse / blast-radius limits", "status": "PARTIAL",
            "evidence": ["tool/record/page/runtime/sub-agent budgets", "runtime-owned aggregate counters", "single-use delegation reference store", "arbitrary patient search denied"],
            "blockers": ["distributed rate limiting", "source back-pressure/circuit breakers", "load/runaway-agent exercises"],
        },
        {
            "id": "A8", "name": "Consequential action boundary", "status": "BLOCKED",
            "evidence": ["write/external-send disabled", "read-only AssistanceDraft requires sources+human review", "consequential operating mode unsupported"],
            "blockers": ["action-specific confirmation UI only if future programme approved", "separate safety/regulatory release programme"],
        },
        {
            "id": "A9", "name": "Independent assurance", "status": "EXTERNAL REVIEW",
            "evidence": ["agent security model", "phases 1-7 programme", "agent red-team CI"],
            "blockers": ["independent security review", "clinical-safety review", "Datenschutz review", "hospital CISO/IT approval"],
        },
    ]
    return {
        "agent_live_identifiable_phi_allowed": False,
        "autonomous_consequential_actions_allowed": False,
        "all_agent_gates_pass": all(gate["status"] == "PASS" for gate in gates),
        "implemented_operating_modes": ["synthetic", "deidentified-sandbox", "shadow-live-locked", "read-only-live-locked", "consequential-unsupported"],
        "gates": gates,
        "rule": "Normal CareOS production readiness does not imply agent readiness; live identifiable agent use requires G0-G5 and A0-A9 PASS.",
    }
