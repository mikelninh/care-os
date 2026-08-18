from fastapi.testclient import TestClient

from app.recare_api import app

client = TestClient(app)


def test_health_contract_is_synthetic_only():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["data_mode"] == "synthetic-only"
    assert body["live_identifiable_phi_allowed"] is False
    assert body["production_write_back"] is False


def test_capabilities_expose_model_workers_without_claiming_live_use():
    response = client.get("/api/capabilities")
    assert response.status_code == 200
    body = response.json()
    assert body["deterministic_worker_available"] is True
    assert set(body["worker_modes"]) == {"deterministic", "external_model", "openai_responses"}
    assert body["external_model_contract"]["live_modes_allowed"] is False
    assert body["external_model_contract"]["retention_or_training_allowed"] is False
    assert body["openai_responses_contract"]["live_modes_allowed"] is False
    assert body["openai_responses_contract"]["store"] is False
    assert body["openai_responses_contract"]["model_is_authority"] is False


def test_run_endpoint_returns_trace_grounding_and_evals():
    response = client.post("/api/run", json={"scenario": "happy_path", "worker_mode": "deterministic"})
    assert response.status_code == 200
    body = response.json()
    assert body["execution_status"] == "completed"
    assert body["draft"]["review_required"] is True
    assert body["draft"]["contains_recommendation"] is False
    assert body["evaluation"]["source_citations_valid"] is True
    assert body["evaluation"]["pending_work_retained"] is True
    assert body["metrics"]["trace_events"] >= 6
    assert any(event["phase"] == "tool" for event in body["trace"])
    assert any(event["name"] == "draft_firewall" for event in body["trace"])


def test_eval_suite_contract_reports_all_expected_scenarios():
    response = client.get("/api/eval-suite")
    assert response.status_code == 200
    body = response.json()
    assert body["suite"] == "recare-capstone-containment-v1"
    assert body["total"] == 6
    assert body["all_pass"] is True
    assert {item["scenario"] for item in body["results"]} == {
        "happy_path", "wrong_patient", "prompt_injection", "source_unavailable", "stale_result", "unauthorised_write"
    }


def test_external_model_mode_fails_closed_when_not_configured(monkeypatch):
    for key in ("CAREOS_MODEL_ENDPOINT", "CAREOS_MODEL_ID", "CAREOS_MODEL_VERSION"):
        monkeypatch.delenv(key, raising=False)
    response = client.post("/api/run", json={"scenario": "happy_path", "worker_mode": "external_model"})
    assert response.status_code == 503
    assert "external model worker not configured" in response.json()["detail"]


def test_openai_responses_mode_fails_closed_when_key_not_configured(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post("/api/run", json={"scenario": "happy_path", "worker_mode": "openai_responses"})
    assert response.status_code == 503
    assert "OpenAI Responses worker not configured" in response.json()["detail"]
