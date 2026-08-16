import pytest

from app.deployment_policy import (
    DataMode,
    DeploymentBlocked,
    assert_data_mode_allowed,
    assert_fhir_source_allowed,
    core_gate_blockers,
)


def test_synthetic_and_deidentified_modes_are_allowed():
    assert assert_data_mode_allowed("synthetic") == DataMode.SYNTHETIC
    assert assert_data_mode_allowed("deidentified-evaluation") == DataMode.DEIDENTIFIED_EVALUATION


def test_live_readonly_is_locked_while_core_gates_not_passed():
    assert core_gate_blockers()
    with pytest.raises(DeploymentBlocked, match="G0-G5"):
        assert_data_mode_allowed("live-readonly")


def test_transactional_mode_is_explicitly_unsupported():
    with pytest.raises(DeploymentBlocked, match="transactional"):
        assert_data_mode_allowed("live-transactional")


def test_unknown_mode_fails_closed():
    with pytest.raises(DeploymentBlocked, match="unknown"):
        assert_data_mode_allowed("just-use-real-data")


def test_synthetic_mode_only_allows_loopback_fhir():
    assert_fhir_source_allowed(DataMode.SYNTHETIC, "http://localhost:8080/fhir")
    assert_fhir_source_allowed(DataMode.SYNTHETIC, "http://127.0.0.1:8080/fhir")
    with pytest.raises(DeploymentBlocked, match="loopback"):
        assert_fhir_source_allowed(DataMode.SYNTHETIC, "https://hospital.example/fhir")


def test_external_deidentified_source_requires_explicit_ack_and_https():
    with pytest.raises(DeploymentBlocked, match="ack"):
        assert_fhir_source_allowed(DataMode.DEIDENTIFIED_EVALUATION, "https://research.example/fhir")
    with pytest.raises(DeploymentBlocked, match="HTTPS"):
        assert_fhir_source_allowed(DataMode.DEIDENTIFIED_EVALUATION, "http://research.example/fhir", external_deidentified_ack=True)
    assert_fhir_source_allowed(DataMode.DEIDENTIFIED_EVALUATION, "https://research.example/fhir", external_deidentified_ack=True)
