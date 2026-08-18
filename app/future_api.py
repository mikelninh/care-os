from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

from .care_coordination import CareRequestState, synthetic_coordination_request, transition_request
from .patient_view import default_teach_back, synthetic_patient_view
from .resilience_drills import standard_recovery_drill
from .service_operating_model import DEFAULT_SERVICE_CATALOG, CommitmentState
from .time_returned_to_care import ROLE_TARGETS, WorkflowObservation, build_time_back_report


app = FastAPI(
    title="CareOS Healthcare Future Foundation",
    version="0.2.0",
    description="Synthetic/pre-hospital API for stakeholder, resilience, coordination and workflow-evidence contracts. Not for clinical use.",
)


class TimeBackRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    observations: list[WorkflowObservation]
    minimum_pairs: int = 5


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "mode": "synthetic-pre-hospital",
        "clinical_use": False,
        "production_phi": False,
    }


@app.get("/api/patient/synthetic")
def patient_synthetic() -> dict:
    view = synthetic_patient_view()
    return {
        "view": view.model_dump(mode="json"),
        "teach_back": [check.model_dump(mode="json") for check in default_teach_back(view)],
        "boundary": "synthetic only; plain-language presentation does not replace source truth",
    }


@app.get("/api/resilience/standard-recovery-drill")
def resilience_standard() -> dict:
    return standard_recovery_drill().model_dump(mode="json")


@app.get("/api/coordination/synthetic-lifecycle")
def coordination_synthetic() -> dict:
    request = synthetic_coordination_request()
    states = [request.model_dump(mode="json")]
    for actor, state, confirmed in (
        ("sender-user", CareRequestState.REQUESTED, True),
        ("receiver-system", CareRequestState.RECEIVED, False),
        ("receiver-user", CareRequestState.ACCEPTED, False),
        ("receiver-user", CareRequestState.SCHEDULED, False),
        ("receiver-user", CareRequestState.PERFORMED, False),
        ("receiver-system", CareRequestState.RESULT_AVAILABLE, False),
        ("sender-user", CareRequestState.FOLLOW_UP_COMPLETE, False),
    ):
        transition = transition_request(request, state, actor_id=actor, human_confirmed=confirmed)
        request = transition.request
        states.append(request.model_dump(mode="json"))
    return {
        "states": states,
        "boundary": "synthetic lifecycle only; transport and authority must be bound to approved real infrastructure before use",
    }


@app.get("/api/time-back/targets")
def time_back_targets() -> dict:
    return {
        "targets": [target.model_dump(mode="json") for target in ROLE_TARGETS],
        "claim": "product targets to test; not measured CareOS outcomes",
    }


@app.post("/api/time-back/report")
def time_back_report(request: TimeBackRequest) -> dict:
    report = build_time_back_report(request.observations, minimum_pairs=request.minimum_pairs)
    return report.model_dump(mode="json")


@app.get("/api/service/catalog")
def service_catalog() -> dict:
    return {
        "services": [service.model_dump(mode="json") for service in DEFAULT_SERVICE_CATALOG],
        "sla_state": CommitmentState.NOT_OFFERED.value,
        "note": "24/7 contractual commitments require staffing and target-environment evidence before they may be offered.",
    }
