from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from app.access_policy import UserContext
from app.auth_oidc import AuthenticatedIdentity
from app.context_launch import ClinicalLaunchContext, ContextBindingError, bind_context


def identity(subject="doctor-1"):
    return AuthenticatedIdentity(subject=subject, issuer="https://id.hospital/", audience="careos", claims={})


def user(subject="doctor-1", organisation="hospital-a", patients={"p1"}):
    return UserContext(subject=subject, organisation=organisation, roles={"doctor"}, scopes={"patient:read"}, treatment_patient_refs=set(patients))


def context(**overrides):
    now = datetime.now(timezone.utc)
    data = {
        "context_id": "ctx-1",
        "subject": "doctor-1",
        "organisation": "hospital-a",
        "patient_ref": "p1",
        "encounter_ref": "enc-1",
        "launcher": "hospital-kis",
        "issued_at": now - timedelta(seconds=5),
        "expires_at": now + timedelta(minutes=5),
    }
    data.update(overrides)
    return ClinicalLaunchContext(**data)


def test_valid_launch_binds_same_authenticated_patient_context():
    request = bind_context(identity(), user(), context())
    assert request.patient_ref == "p1"


def test_subject_mismatch_is_rejected():
    with pytest.raises(ContextBindingError, match="subject"):
        bind_context(identity("doctor-2"), user(), context())


def test_organisation_mismatch_is_rejected():
    with pytest.raises(ContextBindingError, match="organisation"):
        bind_context(identity(), user(organisation="hospital-b"), context())


def test_patient_outside_treatment_context_is_rejected():
    with pytest.raises(ContextBindingError, match="treatment context"):
        bind_context(identity(), user(patients={"p2"}), context())


def test_expired_context_is_rejected():
    now = datetime.now(timezone.utc)
    expired = context(issued_at=now - timedelta(minutes=10), expires_at=now - timedelta(minutes=5))
    with pytest.raises(ContextBindingError, match="expired"):
        bind_context(identity(), user(), expired)


def test_excessively_long_context_lifetime_is_invalid():
    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError):
        context(issued_at=now, expires_at=now + timedelta(hours=1))
