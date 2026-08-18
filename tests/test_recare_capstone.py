from app.recare_capstone import CapstoneRunRequest, capstone_capabilities, run_capstone
from app.recare_eval_suite import run_recare_eval_suite


def test_recare_capstone_happy_path_is_grounded_and_review_required():
    result = run_capstone(CapstoneRunRequest())
    assert result.execution_status == "completed"
    assert result.draft is not None
    assert result.evaluation.source_citations_valid is True
    assert result.evaluation.pending_work_retained is True
    assert result.evaluation.human_review_required is True
    assert result.evaluation.no_treatment_recommendation is True
    assert result.metrics["tool_calls_used"] == 1
    assert any(event.name == "draft_firewall" for event in result.trace)


def test_recare_capstone_blocks_prompt_injection_policy_escalation():
    result = run_capstone(CapstoneRunRequest(scenario="prompt_injection"))
    assert result.execution_status == "blocked"
    assert result.draft is None
    assert any(event.status == "blocked" for event in result.trace)
    assert any("tool outside delegation" in event.detail for event in result.trace)


def test_recare_capstone_blocks_unauthorised_write():
    result = run_capstone(CapstoneRunRequest(scenario="unauthorised_write"))
    assert result.execution_status == "blocked"
    assert result.evaluation.unauthorised_write_blocked is True
    assert any("operation outside delegation" in event.detail for event in result.trace)


def test_recare_capstone_fails_source_outage_visibly():
    result = run_capstone(CapstoneRunRequest(scenario="source_unavailable"))
    assert result.execution_status == "degraded"
    assert result.evaluation.source_failure_visible is True
    assert any(event.status == "degraded" for event in result.trace)


def test_recare_capstone_rejects_wrong_patient_before_truth_admission():
    result = run_capstone(CapstoneRunRequest(scenario="wrong_patient"))
    assert result.execution_status == "blocked"
    assert result.evaluation.wrong_patient_blocked is True
    assert any("wrong-patient" in event.detail for event in result.trace)


def test_capabilities_never_claim_live_phi_or_write_back():
    caps = capstone_capabilities()
    assert caps["public_data_mode"] == "synthetic-only"
    assert caps["live_identifiable_phi_allowed"] is False
    assert caps["consequential_actions_enabled"] is False


def test_recare_containment_suite_treats_safe_blocking_as_success():
    suite = run_recare_eval_suite()
    assert suite["total"] == 6
    assert suite["all_pass"] is True
    assert all(item["pass"] for item in suite["results"])
