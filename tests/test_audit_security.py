import pytest

from app.audit import make_audit_event, pseudonymous_ref, using_demo_audit_key, validate_event
from app.security_readiness import readiness


def test_audit_pseudonyms_are_keyed_and_deployment_specific():
    a = pseudonymous_ref("patient-123", secret="a" * 32)
    b = pseudonymous_ref("patient-123", secret="b" * 32)
    assert a != b
    assert "patient-123" not in a
    assert len(a) == 24


def test_demo_fallback_is_explicitly_detectable(monkeypatch):
    monkeypatch.delenv("AUDIT_PSEUDONYM_KEY", raising=False)
    assert using_demo_audit_key() is True
    monkeypatch.setenv("AUDIT_PSEUDONYM_KEY", "x" * 32)
    assert using_demo_audit_key() is False


def test_recursive_forbidden_clinical_text_keys_are_rejected():
    event = make_audit_event(actor_id="doctor", patient_id="patient", action="read", resource_type="PatientContext", resource_id="ctx", pseudonym_key="x" * 32)
    event["metadata"] = {"nested": {"summary": "sensitive clinical summary"}}
    with pytest.raises(ValueError, match="forbidden"):
        validate_event(event)


def test_production_readiness_requires_jwks_and_real_audit_pseudonym_key():
    env = {
        "AUTH_MODE": "oidc",
        "OIDC_ISSUER": "https://id.example",
        "OIDC_AUDIENCE": "careos",
        "ALLOW_PHI_IN_LOGS": "false",
        "AUDIT_SINK": "central-audit",
        "CLINICAL_WRITEBACK": "disabled",
    }
    result = readiness(env)
    blockers = {c["id"] for c in result["checks"] if c["required"] and not c["ok"]}
    assert "oidc_jwks" in blockers
    assert "audit_pseudonym_key" in blockers


def test_security_readiness_can_clear_config_checks_with_required_values():
    env = {
        "AUTH_MODE": "oidc",
        "OIDC_ISSUER": "https://id.example",
        "OIDC_AUDIENCE": "careos",
        "OIDC_JWKS_URI": "https://id.example/jwks.json",
        "ALLOW_PHI_IN_LOGS": "false",
        "AUDIT_SINK": "central-audit",
        "AUDIT_PSEUDONYM_KEY": "k" * 32,
        "CLINICAL_WRITEBACK": "disabled",
    }
    result = readiness(env)
    assert result["ready"] is True
    assert result["claim"].startswith("Configuration readiness gate only")
