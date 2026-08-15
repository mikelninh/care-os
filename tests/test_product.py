from app.demo_data import TIMELINES, FOCUS, INBOX_ITEMS, DOCUMENTATION_CASES, PILOT_TASKS
from app.safety import patient_match_decision


def test_focus_keeps_sources_visible():
    for focus in FOCUS.values():
        assert focus["facts"]
        assert all(f["source"] for f in focus["facts"])


def test_farid_history_unifies_fragmented_sources():
    sources = {x["source"] for x in TIMELINES["farid"]}
    assert {"KIS", "Arztbrief", "Labor", "ePA", "Fax", "Anrufnotiz", "Pflege", "Externer Scan"}.issubset(sources)


def test_historical_allergy_remains_searchable_and_provenanced():
    item = next(x for x in TIMELINES["farid"] if "Amoxicillin" in x["summary"])
    assert "Exanthem" in item["summary"]
    assert item["source_ref"]


def test_ambiguous_patient_match_blocks_auto_attachment():
    item = next(x for x in INBOX_ITEMS if x["status"] == "ambiguous")
    d = patient_match_decision(item["match_confidence"], False, len(item["candidates"]))
    assert d["decision"] == "block_and_confirm"
    assert d["human_confirmation"] is True


def test_exact_high_confidence_match_can_enter_review_path():
    item = next(x for x in INBOX_ITEMS if x["status"] == "matched")
    d = patient_match_decision(item["match_confidence"], True, 1)
    assert d["decision"] == "auto_attach_allowed"


def test_documentation_reuses_one_note_for_multiple_admin_outputs():
    d = DOCUMENTATION_CASES["farid"]
    assert d["note"] and len(d["structured"]) >= 4 and d["tasks"] and d["handover"] and d["discharge"]


def test_pilot_measures_multiple_real_work_patterns():
    assert len(PILOT_TASKS) >= 5
    assert {t["id"] for t in PILOT_TASKS} >= {"allergy", "renal", "orthostasis", "document", "fax"}
