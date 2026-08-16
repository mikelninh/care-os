from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.agent_data_projection import project_for_model
from app.agent_execution_store import InMemoryDelegationStore
from app.agent_policy import AgentDelegation, AgentOperation
from app.agent_readiness import agent_gate_manifest
from app.agent_redteam import run_containment_suite
from app.readiness_gates import gate_manifest
from app.specialties import SPECIALTY_PACKS

NOW = datetime.now(timezone.utc)


def check(name: str, ok: bool, detail: dict | str) -> dict:
    return {"name": name, "pass": bool(ok), "detail": detail}


def replay_contention() -> dict:
    store = InMemoryDelegationStore()

    def activate(i: int) -> bool:
        try:
            store.activate_once("platform-stress-jti", f"exec-{i}", now=NOW)
            return True
        except PermissionError:
            return False

    with ThreadPoolExecutor(max_workers=32) as pool:
        results = list(pool.map(activate, range(256)))
    return {"attempts": len(results), "accepted": sum(results), "rejected": len(results) - sum(results)}


def specialty_evidence() -> dict:
    rows = {}
    for pack_id, pack in SPECIALTY_PACKS.items():
        demo = pack["demo"]
        rows[pack_id] = {
            "cards": len(demo.get("cards") or []),
            "pending": len(demo.get("pending") or []),
            "timeline": len(demo.get("timeline") or []),
            "card_source_coverage": all(bool(c.get("source")) for c in demo.get("cards") or []),
            "timeline_source_ref_coverage": all(
                bool(e.get("source")) and bool(e.get("ref")) for e in demo.get("timeline") or []
            ),
        }
    return rows


def hostile_agent_evidence() -> dict:
    delegation = AgentDelegation(
        agent_id="careos-rounds-agent",
        agent_version="stress-1",
        delegating_actor="synthetic-clinician",
        organisation="synthetic-provider",
        patient_ref="synthetic-patient-1",
        encounter_ref="synthetic-encounter-1",
        task_id="morning-review",
        allowed_tools={"read-clinical-context", "prepare-handover"},
        allowed_operations={AgentOperation.READ, AgentOperation.PREPARE},
        allowed_data_categories={"microbiology", "medication", "tasks"},
        issued_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=10),
        max_tool_calls=8,
        max_records=100,
        max_pages=8,
        max_runtime_seconds=120,
    )
    return run_containment_suite(delegation, now=NOW)


def model_projection_evidence() -> dict:
    facts = [
        {
            "fact_id": f"f-{i}",
            "category": "microbiology" if i % 2 == 0 else "genetics",
            "value": f"synthetic-{i}",
            "source_ref": f"source-{i}",
            "patient_id": "must-never-cross-fixed-shape",
        }
        for i in range(10_000)
    ]
    projected = project_for_model(facts, allowed_categories={"microbiology"}, max_facts=50)
    forbidden_keys = {"patient_id", "patient_ref", "name", "dob", "address", "email", "phone"}
    return {
        "input_facts": len(facts),
        "projected_facts": len(projected),
        "max_facts": 50,
        "forbidden_key_leak": any(forbidden_keys & set(row) for row in projected),
        "all_source_linked": all(bool(row.get("source_ref")) for row in projected),
    }


def main() -> int:
    replay = replay_contention()
    specialties = specialty_evidence()
    hostile = hostile_agent_evidence()
    projection = model_projection_evidence()
    core = gate_manifest()
    agents = agent_gate_manifest()

    checks = [
        check("delegation-replay-contention", replay["accepted"] == 1, replay),
        check(
            "specialty-provenance",
            all(
                row["cards"] > 0
                and row["pending"] > 0
                and row["timeline"] >= 3
                and row["card_source_coverage"]
                and row["timeline_source_ref_coverage"]
                for row in specialties.values()
            ),
            specialties,
        ),
        check("hostile-agent-containment", hostile["pass"] and hostile["contained"] == hostile["total"], hostile),
        check(
            "model-data-minimization",
            projection["projected_facts"] <= projection["max_facts"]
            and not projection["forbidden_key_leak"]
            and projection["all_source_linked"],
            projection,
        ),
        check(
            "live-data-locks",
            core.get("live_patient_data_allowed") is False
            and agents.get("agent_live_identifiable_phi_allowed") is False
            and agents.get("autonomous_consequential_actions_allowed") is False,
            {
                "live_patient_data_allowed": core.get("live_patient_data_allowed"),
                "agent_live_identifiable_phi_allowed": agents.get("agent_live_identifiable_phi_allowed"),
                "autonomous_consequential_actions_allowed": agents.get("autonomous_consequential_actions_allowed"),
            },
        ),
    ]

    known_gaps = [
        {
            "severity": "BLOCKER",
            "id": "g1-clinical-truth-utility",
            "gap": "Clinical truth extraction remains blocked by low recall/high review burden on frozen unseen evidence; synthetic provenance safety is not enough for workflow utility.",
        },
        {
            "severity": "BLOCKER",
            "id": "real-provider-security",
            "gap": "No real hospital IdP, KMS/secrets deployment, protected audit/SIEM, DLP/egress enforcement, production signing authority or independent penetration test yet.",
        },
        {
            "severity": "BLOCKER",
            "id": "real-kis-lis-sandbox",
            "gap": "No real KIS/LIS/vendor sandbox or hospital interface behavior has been exercised; synthetic FHIR cannot prove vendor interoperability.",
        },
        {
            "severity": "HIGH",
            "id": "audit-multiprocess",
            "gap": "Local tamper-evident audit-chain file is evidence scaffolding, not a concurrent multi-process immutable production audit sink.",
        },
        {
            "severity": "HIGH",
            "id": "model-free-text-phi",
            "gap": "Fixed model projection removes direct identifier fields but scalar clinical values may still contain identifiers/free text; live model use therefore remains blocked pending provider-side PHI/DLP policy.",
        },
        {
            "severity": "HIGH",
            "id": "browser-and-accessibility",
            "gap": "Static demos have not been validated on the target hospital managed browser/Citrix/VDI estate with accessibility, keyboard, screen-reader and low-spec performance evidence.",
        },
        {
            "severity": "HIGH",
            "id": "automation-bias",
            "gap": "Verification decay/automation bias is instrumented but has no human evidence yet; speed improvement cannot be treated as success before clinician A/B testing.",
        },
        {
            "severity": "EXTERNAL",
            "id": "regulatory-and-datenschutz",
            "gap": "MDR/MDSW/intended-purpose, AI Act/EHDS applicability, DSFA/DPIA, AVV/DPA and hospital clinical-safety acceptance require qualified external review.",
        },
    ]

    report = {
        "schema_version": "1.0",
        "generated_at": NOW.isoformat(),
        "scope": "whole-platform synthetic/deidentified adversarial stress evidence",
        "production_claim": "not-production-ready",
        "checks": checks,
        "pass": all(item["pass"] for item in checks),
        "known_gaps": known_gaps,
        "rule": "Internal stress PASS proves only the listed deterministic invariants; it never unlocks live patient data or agent use.",
    }

    output = ROOT / "data" / "platform_stress_report.json"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
