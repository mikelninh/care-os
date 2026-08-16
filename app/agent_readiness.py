from __future__ import annotations


def agent_gate_manifest() -> dict:
    gates = [
        {
            "id": "A0",
            "name": "Agent/workload identity",
            "status": "PARTIAL",
            "evidence": ["first-class agent_id/version contracts", "separate agent delegation policy"],
            "blockers": ["real provider workload identity", "credential revocation/rotation evidence"],
        },
        {
            "id": "A1",
            "name": "Signed delegation",
            "status": "PARTIAL",
            "evidence": ["Ed25519 signed delegation envelope", "issuer/audience/key-id validation", "patient/encounter/task/tool/time/budget binding"],
            "blockers": ["production delegation issuer", "replay-prevention store", "real key lifecycle"],
        },
        {
            "id": "A2",
            "name": "Tool least privilege",
            "status": "PARTIAL",
            "evidence": ["versioned ToolSpec registry", "deterministic per-call gateway authorization", "read/prepare separated from consequential effects"],
            "blockers": ["all real production tools registered", "provider-specific tool conformance tests"],
        },
        {
            "id": "A3",
            "name": "Injection/hijacking resilience",
            "status": "BLOCKED",
            "evidence": ["policy boundary designed so model refusal is not required for authorization"],
            "blockers": ["model-connected adversarial harness", "malicious document/tool-result tests", "independent red team"],
        },
        {
            "id": "A4",
            "name": "Egress / PHI controls",
            "status": "BLOCKED",
            "evidence": ["deny-by-default egress fields in delegation/tool contracts"],
            "blockers": ["real provider network allowlist/DLP", "approved model/subprocessor data-flow evidence", "egress enforcement outside application process"],
        },
        {
            "id": "A5",
            "name": "Agent audit / non-repudiation",
            "status": "PARTIAL",
            "evidence": ["structured human+agent+delegation+tool audit schema", "PHI-minimized identifiers"],
            "blockers": ["protected provider audit/SIEM integration", "integrity/non-repudiation review", "operational review workflow"],
        },
        {
            "id": "A6",
            "name": "Memory isolation",
            "status": "PARTIAL",
            "evidence": ["organisation/patient/encounter/execution-scoped memory namespace"],
            "blockers": ["real memory store", "retention/deletion tests", "cross-patient leakage test with model runtime"],
        },
        {
            "id": "A7",
            "name": "Abuse / blast-radius limits",
            "status": "PARTIAL",
            "evidence": ["tool/record/page/runtime/sub-agent budgets", "arbitrary patient search denied", "consequential actions disabled"],
            "blockers": ["distributed rate limiting", "source-system back-pressure/circuit breakers", "load/runaway-agent exercises"],
        },
        {
            "id": "A8",
            "name": "Consequential action boundary",
            "status": "BLOCKED",
            "evidence": ["write/external-send denied by release policy", "tool metadata requires confirmation for future consequential tools"],
            "blockers": ["action-specific human confirmation UI", "separate safety/regulatory release programme"],
        },
        {
            "id": "A9",
            "name": "Independent assurance",
            "status": "EXTERNAL REVIEW",
            "evidence": ["agent security model", "agent production programme"],
            "blockers": ["independent security review", "clinical-safety review", "Datenschutz review", "hospital CISO/IT approval"],
        },
    ]
    return {
        "agent_live_identifiable_phi_allowed": False,
        "autonomous_consequential_actions_allowed": False,
        "all_agent_gates_pass": all(gate["status"] == "PASS" for gate in gates),
        "gates": gates,
        "rule": "Normal CareOS production readiness does not imply agent readiness; identifiable agent use requires normal G0-G5 and all A0-A9 PASS.",
    }
