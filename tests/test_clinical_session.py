from datetime import datetime, timedelta, timezone

from app.access_policy import AccessRequest, UserContext
from app.clinical_session import CallbackAuditSink, ClinicalReadCoordinator
from app.clinical_truth import TruthEnvelope
from app.connectors.base import ConnectorReadResult
from app.source_state import SourceAvailability, SourceState


class FakeConnector:
    def __init__(self, result):
        self.result = result
        self.called = False

    def capabilities(self):
        raise NotImplementedError

    def read_patient_truth(self, patient_ref):
        self.called = True
        return self.result


def user(patients={"p1"}):
    return UserContext(
        subject="doctor-1",
        organisation="hospital-a",
        roles={"doctor"},
        scopes={"patient:read"},
        treatment_patient_refs=set(patients),
    )


def current_result(patient="p1"):
    now = datetime.now(timezone.utc)
    return ConnectorReadResult(
        connector_id="fake",
        source_state=SourceState(source_id="fake", availability=SourceAvailability.CURRENT, last_success_at=now, observed_at=now),
        truth=TruthEnvelope(patient_ref=patient, facts=[]),
    )


def test_authorized_current_audited_read_returns_truth():
    events = []
    connector = FakeConnector(current_result())
    outcome = ClinicalReadCoordinator(CallbackAuditSink(events.append)).read(user(), AccessRequest(patient_ref="p1"), connector)
    assert outcome.status == "ready"
    assert outcome.allowed_to_render is True
    assert len(events) == 1
    assert events[0]["outcome"] == "success"
    assert "p1" not in str(events[0])


def test_unauthorized_patient_is_denied_before_connector_call():
    events = []
    connector = FakeConnector(current_result("p2"))
    outcome = ClinicalReadCoordinator(CallbackAuditSink(events.append)).read(user(), AccessRequest(patient_ref="p2"), connector)
    assert outcome.status == "denied"
    assert outcome.truth is None
    assert connector.called is False


def test_source_unavailable_never_becomes_empty_success():
    now = datetime.now(timezone.utc)
    connector = FakeConnector(ConnectorReadResult(
        connector_id="fake",
        source_state=SourceState(source_id="fake", availability=SourceAvailability.UNAVAILABLE, observed_at=now, detail="timeout"),
        truth=None,
    ))
    outcome = ClinicalReadCoordinator(CallbackAuditSink(lambda _: None)).read(user(), AccessRequest(patient_ref="p1"), connector)
    assert outcome.status == "source-unavailable"
    assert outcome.truth is None


def test_cross_patient_truth_is_withheld_even_after_authorized_request():
    connector = FakeConnector(current_result("p2"))
    outcome = ClinicalReadCoordinator(CallbackAuditSink(lambda _: None)).read(user(), AccessRequest(patient_ref="p1"), connector)
    assert outcome.status == "patient-context-mismatch"
    assert outcome.truth is None


def test_stale_source_truth_is_withheld_from_quiet_rendering():
    now = datetime.now(timezone.utc)
    result = ConnectorReadResult(
        connector_id="fake",
        source_state=SourceState(
            source_id="fake",
            availability=SourceAvailability.CURRENT,
            last_success_at=now - timedelta(hours=1),
            observed_at=now,
            max_age_seconds=60,
        ),
        truth=TruthEnvelope(patient_ref="p1", facts=[]),
    )
    outcome = ClinicalReadCoordinator(CallbackAuditSink(lambda _: None)).read(user(), AccessRequest(patient_ref="p1"), FakeConnector(result))
    assert outcome.status == "source-not-current"
    assert outcome.truth is None


def test_audit_failure_withholds_patient_truth():
    def broken_audit(_):
        raise RuntimeError("audit unavailable")

    outcome = ClinicalReadCoordinator(CallbackAuditSink(broken_audit)).read(user(), AccessRequest(patient_ref="p1"), FakeConnector(current_result()))
    assert outcome.status == "audit-unavailable"
    assert outcome.truth is None
