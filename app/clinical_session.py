from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

from .access_policy import AccessDecision, AccessRequest, UserContext, evaluate_access
from .audit import make_audit_event, validate_event
from .clinical_truth import TruthEnvelope
from .connectors.base import ClinicalConnector, ConnectorReadResult


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

    Expected production ordering:
      1. token authentication happens before UserContext construction;
      2. authorization checks role/scope/treatment context;
      3. connector read must return source state + canonical truth;
      4. patient context must match end-to-end;
      5. required audit must succeed before PHI is returned to the caller.

    No step may silently degrade into a successful empty patient view.
    """

    def __init__(self, audit_sink: AuditSink):
        self.audit_sink = audit_sink

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
                # Denied access stays denied even if audit is degraded; deployment policy
                # must separately alarm on the audit failure.
                pass
            return ClinicalReadOutcome(
                status="denied",
                reason=decision.reason,
                truth=None,
                connector_result=None,
                access_decision=decision,
            )

        result = connector.read_patient_truth(request.patient_ref)
        if result.truth is None:
            try:
                self._audit(user, request, outcome=f"source-{result.source_state.availability.value}")
            except Exception:
                pass
            return ClinicalReadOutcome(
                status="source-unavailable",
                reason=result.source_state.detail or result.source_state.availability.value,
                truth=None,
                connector_result=result,
                access_decision=decision,
            )

        if result.truth.patient_ref != request.patient_ref:
            try:
                self._audit(user, request, outcome="patient-context-mismatch")
            except Exception:
                pass
            return ClinicalReadOutcome(
                status="patient-context-mismatch",
                reason="connector truth patient_ref does not match authorized request",
                truth=None,
                connector_result=result,
                access_decision=decision,
            )

        if not result.source_state.may_assert_absence:
            try:
                self._audit(user, request, outcome=f"source-{result.source_state.evaluated_availability().value}")
            except Exception:
                pass
            return ClinicalReadOutcome(
                status="source-not-current",
                reason="source is not current enough for quiet clinical rendering",
                truth=None,
                connector_result=result,
                access_decision=decision,
            )

        try:
            self._audit(user, request, outcome="success")
        except Exception:
            return ClinicalReadOutcome(
                status="audit-unavailable",
                reason="required audit sink failed; patient truth withheld",
                truth=None,
                connector_result=result,
                access_decision=decision,
            )

        return ClinicalReadOutcome(
            status="ready",
            reason="authorized current source and audit recorded",
            truth=result.truth,
            connector_result=result,
            access_decision=decision,
        )
