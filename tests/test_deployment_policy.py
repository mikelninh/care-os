import pytest

from app.deployment_policy import DataMode, DeploymentBlocked, assert_data_mode_allowed, core_gate_blockers


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
