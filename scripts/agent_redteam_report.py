from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.agent_policy import AgentDelegation, AgentOperation
from app.agent_redteam import run_containment_suite

NOW = datetime.now(timezone.utc)

delegation = AgentDelegation(
    agent_id="careos-rounds-agent",
    agent_version="1.0.0",
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
    max_tool_calls=5,
    max_records=50,
    max_pages=5,
    max_runtime_seconds=120,
)

report = run_containment_suite(delegation, now=NOW)
report["generated_at"] = NOW.isoformat()
report["data_mode"] = "synthetic-only"

out = Path("artifacts/agent-redteam-report.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0 if report["pass"] else 1)
