from app.access_policy import AccessAction, AccessRequest, UserContext, evaluate_access


def clinician(**overrides):
    data = {
        "subject": "doctor-1",
        "organisation": "hospital-a",
        "roles": {"doctor"},
        "scopes": {"patient:read"},
        "treatment_patient_refs": {"p1"},
    }
    data.update(overrides)
    return UserContext(**data)


def test_active_treatment_context_allows_scoped_read():
    d = evaluate_access(clinician(), AccessRequest(patient_ref="p1"))
    assert d.allowed is True
    assert d.audit_level == "normal"


def test_other_patient_is_denied_by_default():
    d = evaluate_access(clinician(), AccessRequest(patient_ref="p2"))
    assert d.allowed is False
    assert "treatment context" in d.reason


def test_break_glass_requires_reason_and_elevated_audit():
    denied = evaluate_access(clinician(), AccessRequest(patient_ref="p2", break_glass=True, break_glass_reason="urgent"))
    assert denied.allowed is False
    allowed = evaluate_access(clinician(), AccessRequest(patient_ref="p2", break_glass=True, break_glass_reason="Emergency review for unstable patient"))
    assert allowed.allowed is True
    assert allowed.break_glass is True
    assert allowed.audit_level == "high"


def test_write_is_disabled_even_with_write_scope_until_release_policy_changes():
    user = clinician(scopes={"patient:read", "patient:write"})
    d = evaluate_access(user, AccessRequest(patient_ref="p1", action=AccessAction.WRITE))
    assert d.allowed is False
    assert "write-back disabled" in d.reason


def test_missing_scope_fails_closed():
    d = evaluate_access(clinician(scopes=set()), AccessRequest(patient_ref="p1"))
    assert d.allowed is False
    assert "missing scope" in d.reason
