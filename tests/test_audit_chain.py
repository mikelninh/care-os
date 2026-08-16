from pathlib import Path

from app.audit import make_audit_event
from app.audit_chain import append_chained_event, read_chain, verify_chain


def event(action="read"):
    return make_audit_event(
        actor_id="doctor-1",
        patient_id="patient-1",
        action=action,
        resource_type="PatientContext",
        resource_id="ctx",
    )


def test_chained_audit_detects_event_tampering(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    append_chained_event(event("read-1"), path)
    append_chained_event(event("read-2"), path)
    records = read_chain(path)
    assert verify_chain(records) == (True, None, "valid")

    records[0]["event"]["action"] = "tampered"
    ok, index, reason = verify_chain(records)
    assert ok is False
    assert index == 0
    assert "hash" in reason


def test_chained_audit_detects_record_removal_or_reordering(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    append_chained_event(event("read-1"), path)
    append_chained_event(event("read-2"), path)
    records = read_chain(path)

    ok, index, reason = verify_chain([records[1]])
    assert ok is False
    assert index == 0
    assert "previous hash" in reason


def test_append_refuses_to_continue_corrupted_existing_chain(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    append_chained_event(event("read-1"), path)
    text = path.read_text(encoding="utf-8").replace("read-1", "edited")
    path.write_text(text, encoding="utf-8")

    try:
        append_chained_event(event("read-2"), path)
        assert False, "corrupted chain should reject append"
    except ValueError as exc:
        assert "invalid" in str(exc)


def test_audit_chain_contains_no_raw_actor_or_patient_id(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    append_chained_event(event(), path)
    raw = path.read_text(encoding="utf-8")
    assert "doctor-1" not in raw
    assert "patient-1" not in raw
