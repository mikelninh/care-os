from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

from .access_policy import AccessDecision, AccessRequest, UserContext, evaluate_access
from .audit import make_audit_event, validate_event
from .clinical_truth import TruthEnvelope
from .connectors.base import ClinicalConnector, ConnectorReadResult
from .kill_switch import SafetyControls


class AuditSink(Protocol):
    def emit(self, event: dict) -> None: ...


@dataclass(frozen=True)
class CallbackAuditSink:
    callback: Callable[[dict], None]

    def emit(self, event: dict) -> None:
        validate_event(event)
        self.callback(event)


@dataclass(frozen=True)
class ClinicalReadOutcome:
    status: str
    reason: str
    truth: TruthEnvelope | None
    connector_result: ConnectorReadResult | None
    access_decision: AccessDecision

    @property
    def allowed_to_render(self) -> bool:
        return self.status == "ready" and self.truth is not None


class ClinicalReadCoordinator:
    """Fail-closed orchestration for a read-only CareOS patient-context request.

    Authentication occurs before UserContext construction. Authorization, runtime
    safety controls, source currentness, patient identity and required audit must all
    succeed before patient truth is returned. Connector exceptions are converted into
    an explicit unavailable outcome without leaking provider/internal exception text.
    """

    def __init__(self, audit_sink: AuditSink, safety_controls: SafetyControls | None = None):
        self.audit_sink = audit_sink
        self.safety_controls = safety_controls or SafetyControls()

    def _audit(self, user: UserContext, request: AccessRequest, *, outcome: str, action: str = "read") -> None:
        event = make_audit_event(
            actor_id=user.subject,
            patient_id=request.patient_ref,
            action=action,
            resource_type="PatientContext",
            resource_id="careos-context",
            outcome=outcome,
        )
        self.audit_sink.emit(event)

    def read(self, user: UserContext, request: AccessRequest, connector: ClinicalConnector) -> ClinicalReadOutcome:
        decision = evaluate_access(user, request, writeback_enabled=False)

        if not decision.allowed:
            try:
                self._audit(user, request, outcome="denied", action="read-denied")
            except Exception:
                pass
            return ClinicalReadOutcome(status="denied", reason=decision.reason, truth=None, connector_result=None, access_decision=decision)

        runtime_allowed, runtime_reason = self.safety_controls.read_allowed(connector.connector_id)
        if not runtime_allowed:
            try:
                self._audit(user, request, outcome="runtime-disabled", action="read-disabled")
            except Exception:
                pass
            return ClinicalReadOutcome(status="runtime-disabled", reason=runtime_reason, truth=None, connector_result=None, access_decision=decision)

        try:
            result = connector.read_patient_truth(request.patient_ref)
        except Exception:
            try:
                self._audit(user, request, outcome="source-exception", action="read-source-failed")
            except Exception:
                pass
            return ClinicalReadOutcome(
                status="source-unavailable",
                reason="clinical source read failed",
                truth=None,
                connector_result=None,
                access_decision=decision,
            )

        if result.connector_id != connector.connector_id:
            try:
                self._audit(user, request, outcome="connector-identity-mismatch")
            except Exception:
                pass
            return ClinicalReadOutcome(status="connector-identity-mismatch", reason="connector result identity does not match invoked connector", truth=None, connector_result=result, access_decision=decision)

        if result.truth is None:
            try:
                self._audit(user, request, outcome=f"source-{result.source_state.availability.value}")
            except Exception:
                pass
            return ClinicalReadOutcome(status="source-unavailable", reason=result.source_state.detail or result.source_state.availability.value, truth=None, connector_result=result, access_decision=decision)

        if result.truth.patient_ref != request.patient_ref:
            try:
                self._audit(user, request, outcome="patient-context-mismatch")
            except Exception:
                pass
            return ClinicalReadOutcome(status="patient-context-mismatch", reason="connector truth patient_ref does not match authorized request", truth=None, connector_result=result, access_decision=decision)

        if not result.source_state.may_assert_absence:
            try:
                self._audit(user, request, outcome=f"source-{result.source_state.evaluated_availability().value}")
            except Exception:
                pass
            return ClinicalReadOutcome(status="source-not-current", reason="source is not current enough for quiet clinical rendering", truth=None, connector_result=result, access_decision=decision)

        try:
            self._audit(user, request, outcome="success")
        except Exception:
            return ClinicalReadOutcome(status="audit-unavailable", reason="required audit sink failed; patient truth withheld", truth=None, connector_result=result, access_decision=decision)

        return ClinicalReadOutcome(status="ready", reason="authorized current source and audit recorded", truth=result.truth, connector_result=result, access_decision=decision)
