from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_infectiology_morning_review_has_sources_pending_and_no_treatment_claim():
    response = client.get("/api/specialties/infectiology")
    assert response.status_code == 200
    demo = response.json()["demo"]
    assert demo["cards"] and demo["pending"] and demo["timeline"]
    assert any("Mikrobiologie" in card["label"] for card in demo["cards"])
    clinical_story = " ".join(
        [*demo["pending"]]
        + [str(card.get("detail", "")) for card in demo["cards"]]
        + [str(item.get("summary", "")) for item in demo["timeline"]]
    ).lower()
    assert "aussteh" in clinical_story
    assert all(item["ref"] for item in demo["timeline"])
    anti = next(card for card in demo["cards"] if card["label"] == "Antiinfektiva")
    assert "Keine automatische Therapieempfehlung" in anti["detail"]


def test_oncology_handover_preserves_pathology_therapy_toxicity_and_open_work():
    response = client.get("/api/specialties/oncology")
    assert response.status_code == 200
    demo = response.json()["demo"]
    labels = {card["label"] for card in demo["cards"]}
    assert {"Diagnose / Stadium", "Molekular", "Therapie", "Toxizität", "Offen"} <= labels
    assert len(demo["timeline"]) >= 3
    assert "Tumorboard" in demo["handover"]


def test_neurology_change_review_distinguishes_baseline_new_change_and_followup():
    response = client.get("/api/specialties/neurology")
    assert response.status_code == 200
    demo = response.json()["demo"]
    labels = {card["label"] for card in demo["cards"]}
    assert {"Baseline", "Neu seit heute", "Bildgebung", "Offen"} <= labels
    assert any("Reassessment" in pending for pending in demo["pending"])
    assert all(item["source"] and item["ref"] for item in demo["timeline"])


def test_legacy_inbox_ambiguous_patient_match_is_blocked_for_human_review():
    inbox = client.get("/api/inbox")
    assert inbox.status_code == 200
    ambiguous = next(item for item in inbox.json() if item["status"] == "ambiguous")
    policy = client.get(f"/api/inbox/{ambiguous['id']}/match-policy")
    assert policy.status_code == 200
    assert "block" in policy.json()["decision"]


def test_documentation_reuse_is_prepare_and_review_not_writeback():
    response = client.get("/api/patients/farid/documentation")
    assert response.status_code == 200
    document = response.json()
    assert document["note"]
    assert document["handover"]
    assert document["tasks"]
    health = client.get("/api/health").json()
    assert "no production write-back" in health["claims"]


def test_pilot_measurement_never_rewards_fast_failed_task():
    response = client.post(
        "/api/pilot/score",
        json={
            "task_id": "wrong-fast",
            "baseline_minutes": 10,
            "actual_seconds": 5,
            "success": False,
            "corrections": 1,
        },
    )
    assert response.status_code == 200
    score = response.json()
    assert score["gross_saved_minutes"] > 9
    assert score["saved_minutes"] == 0
    assert score["reduction_percent"] == 0


def test_agent_and_core_readiness_surfaces_remain_explicitly_locked():
    core = client.get("/api/readiness/gates")
    agents = client.get("/api/readiness/agents")
    tools = client.get("/api/agents/synthetic-tools")
    assert core.status_code == agents.status_code == tools.status_code == 200
    assert core.json()["live_patient_data_allowed"] is False
    assert agents.json()["agent_live_identifiable_phi_allowed"] is False
    assert agents.json()["autonomous_consequential_actions_allowed"] is False
    assert tools.json()["mode"] == "synthetic-only"
    assert tools.json()["tools"]


def test_unknown_patient_specialty_and_inbox_resources_fail_cleanly():
    assert client.get("/api/patients/not-real/focus").status_code == 404
    assert client.get("/api/specialties/not-real").status_code == 404
    assert client.get("/api/inbox/not-real/match-policy").status_code == 404
