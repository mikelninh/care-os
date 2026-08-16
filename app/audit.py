from __future__ import annotations

import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FORBIDDEN_KEYS = {
    "note",
    "notes",
    "text",
    "summary",
    "clinical_text",
    "transcript",
    "diagnosis",
    "medication",
    "allergy",
    "result_text",
    "document_text",
}

# Tests/synthetic mode need deterministic pseudonyms without a secret-management
# dependency. Production readiness explicitly rejects this fallback.
_DEMO_ONLY_KEY = b"careos-demo-audit-pseudonym-key-not-for-live-phi"


def _audit_key(secret: str | bytes | None = None) -> bytes:
    if isinstance(secret, str):
        secret = secret.encode("utf-8")
    if secret:
        return secret
    configured = os.getenv("AUDIT_PSEUDONYM_KEY")
    if configured:
        return configured.encode("utf-8")
    return _DEMO_ONLY_KEY


def using_demo_audit_key(secret: str | bytes | None = None) -> bool:
    if secret:
        return False
    return not bool(os.getenv("AUDIT_PSEUDONYM_KEY"))


def pseudonymous_ref(value: str, *, secret: str | bytes | None = None) -> str:
    """Deployment-scoped keyed pseudonym, never plain-hash the identifier.

    A high-entropy deployment secret must be supplied/configured before live PHI. The
    deterministic demo fallback exists only so synthetic/local tests remain runnable.
    """

    digest = hmac.new(_audit_key(secret), value.encode("utf-8"), hashlib.sha256).hexdigest()
    return digest[:24]


def make_audit_event(
    *,
    actor_id: str,
    patient_id: str,
    action: str,
    resource_type: str,
    resource_id: str,
    outcome: str = "success",
    pseudonym_key: str | bytes | None = None,
) -> dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor_ref": pseudonymous_ref(actor_id, secret=pseudonym_key),
        "patient_ref": pseudonymous_ref(patient_id, secret=pseudonym_key),
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "outcome": outcome,
    }


def _forbidden_path(value: Any, path: str = "$") -> str | None:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key).lower()
            if key_text in FORBIDDEN_KEYS:
                return f"{path}.{key}"
            found = _forbidden_path(nested, f"{path}.{key}")
            if found:
                return found
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            found = _forbidden_path(nested, f"{path}[{index}]")
            if found:
                return found
    return None


def validate_event(event: dict[str, Any]) -> None:
    forbidden = _forbidden_path(event)
    if forbidden:
        raise ValueError(f"audit event contains forbidden clinical-text key at {forbidden}")


def append_jsonl(event: dict[str, Any], path: Path) -> None:
    validate_event(event)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
