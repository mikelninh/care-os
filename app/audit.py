from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FORBIDDEN_KEYS = {"note", "text", "summary", "clinical_text", "transcript"}


def pseudonymous_ref(value: str) -> str:
    return hashlib.sha256(("careos-audit:" + value).encode()).hexdigest()[:20]


def make_audit_event(*, actor_id: str, patient_id: str, action: str, resource_type: str, resource_id: str, outcome: str = "success") -> dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor_ref": pseudonymous_ref(actor_id),
        "patient_ref": pseudonymous_ref(patient_id),
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "outcome": outcome,
    }


def validate_event(event: dict[str, Any]) -> None:
    if FORBIDDEN_KEYS.intersection(event):
        raise ValueError("audit event contains forbidden clinical-text keys")


def append_jsonl(event: dict[str, Any], path: Path) -> None:
    validate_event(event)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
