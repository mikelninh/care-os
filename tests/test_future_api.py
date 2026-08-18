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


def test_service_catalog_does_not_claim_current_sla():
    response = client.get("/api/service/catalog")
    assert response.status_code == 200
    assert response.json()["sla_state"] == "not-offered"


def test_time_back_targets_are_labeled_as_targets_not_outcomes():
    response = client.get("/api/time-back/targets")
    assert response.status_code == 200
    assert response.json()["targets"]
    assert "not measured" in response.json()["claim"]
