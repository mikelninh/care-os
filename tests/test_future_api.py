from fastapi.testclient import TestClient

from app.future_api import app


client = TestClient(app)


def test_health_is_explicitly_synthetic_and_nonclinical():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "synthetic-pre-hospital"
    assert body["clinical_use"] is False
    assert body["production_phi"] is False


def test_golden_journey_api_runs_the_complete_synthetic_regression_story():
    response = client.get("/api/journey/golden")
    assert response.status_code == 200
    body = response.json()
    assert body["all_passed"] is True
    assert body["journey"]["recovery"]["before"]["mode"] == "recovery"
    assert body["journey"]["recovery"]["after"]["mode"] == "normal"
    assert body["journey"]["sla_state"] == "not-offered"
    assert "not clinical validation" in body["boundary"]


def test_patient_api_returns_source_linked_view_and_teach_back():
    response = client.get("/api/patient/synthetic")
    assert response.status_code == 200
    body = response.json()
    assert body["view"]["pending"]
    assert body["teach_back"]
    assert "source truth" in body["boundary"]


def test_resilience_api_recovers_only_after_reconciliation():
    response = client.get("/api/resilience/standard-recovery-drill")
    assert response.status_code == 200
    body = response.json()
    assert [step["decision"]["mode"] for step in body["steps"]] == ["offline", "recovery", "normal"]
    assert body["hidden_write_ever_allowed"] is False
    assert body["absence_claim_ever_allowed_while_stale_or_offline"] is False


def test_coordination_api_has_acknowledged_lifecycle_not_fire_and_forget():
    response = client.get("/api/coordination/synthetic-lifecycle")
    assert response.status_code == 200
    states = [item["state"] for item in response.json()["states"]]
    assert states == [
        "draft",
        "requested",
        "received",
        "accepted",
        "scheduled",
        "performed",
        "result-available",
        "follow-up-complete",
    ]
    assert "synthetic" in response.json()["boundary"]


def test_service_catalog_does_not_claim_current_sla():
    response = client.get("/api/service/catalog")
    assert response.status_code == 200
    assert response.json()["sla_state"] == "not-offered"


def test_time_back_targets_are_labeled_as_targets_not_outcomes():
    response = client.get("/api/time-back/targets")
    assert response.status_code == 200
    assert response.json()["targets"]
    assert "not measured" in response.json()["claim"]
