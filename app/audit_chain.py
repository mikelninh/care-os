from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from .audit import validate_event

GENESIS_HASH = "0" * 64


def _canonical_json(value: dict[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _record_hash(previous_hash: str, event: dict[str, Any]) -> str:
    payload = previous_hash.encode("ascii") + b"\n" + _canonical_json(event)
    return hashlib.sha256(payload).hexdigest()


def make_chained_record(event: dict[str, Any], previous_hash: str = GENESIS_HASH) -> dict[str, Any]:
    validate_event(event)
    if len(previous_hash) != 64:
        raise ValueError("previous_hash must be a 64-character SHA-256 hex digest")
    record_hash = _record_hash(previous_hash, event)
    return {"previous_hash": previous_hash, "event": event, "record_hash": record_hash}


def verify_chain(records: Iterable[dict[str, Any]]) -> tuple[bool, int | None, str]:
    expected_previous = GENESIS_HASH
    for index, record in enumerate(records):
        event = record.get("event")
        previous_hash = record.get("previous_hash")
        record_hash = record.get("record_hash")
        if not isinstance(event, dict):
            return False, index, "missing event"
        try:
            validate_event(event)
        except ValueError:
            return False, index, "forbidden audit content"
        if previous_hash != expected_previous:
            return False, index, "previous hash mismatch"
        expected_hash = _record_hash(previous_hash, event)
        if record_hash != expected_hash:
            return False, index, "record hash mismatch"
        expected_previous = record_hash
    return True, None, "valid"


def read_chain(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_chained_event(event: dict[str, Any], path: Path) -> dict[str, Any]:
    """Append a tamper-evident local record.

    This detects modification/removal/reordering within a retrieved chain but does not
    make a local file immutable. Production G3 still requires a central append-only or
    otherwise independently protected audit sink and monitoring.
    """

    existing = read_chain(path)
    valid, index, reason = verify_chain(existing)
    if not valid:
        raise ValueError(f"existing audit chain invalid at {index}: {reason}")
    previous_hash = existing[-1]["record_hash"] if existing else GENESIS_HASH
    record = make_chained_record(event, previous_hash)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    return record
