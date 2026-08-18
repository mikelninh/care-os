from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ServiceCriticality(str, Enum):
    C0_SOURCE_TRUTH = "c0-source-truth"
    C1_CLINICAL_CONTEXT = "c1-clinical-context"
    C2_AGENT_ASSIST = "c2-agent-assist"
    C3_ADMIN_ANALYTICS = "c3-admin-analytics"


class CommitmentState(str, Enum):
    NOT_OFFERED = "not-offered"
    DRAFT = "draft"
    CONTRACTED = "contracted"


class IncidentSeverity(str, Enum):
    SEV0 = "sev0-systemic-safety"
    SEV1 = "sev1-critical-clinical-workflow"
    SEV2 = "sev2-degraded-workflow"
    SEV3 = "sev3-noncritical"


class KillScope(str, Enum):
    MODEL = "model"
    AGENT_VERSION = "agent-version"
    TOOL = "tool"
    ADAPTER = "adapter"
    WORKFLOW = "workflow"
    SITE = "site"
    RELEASE = "release"


class ServiceCapability(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_id: str = Field(min_length=1)
    criticality: ServiceCriticality
    routine_phi_control_plane_dependency: bool = False
    hospital_local_fallback_required: bool = True
    local_kill_scope: tuple[KillScope, ...] = ()
    description: str

    @model_validator(mode="after")
    def core_truth_cannot_require_shared_control_plane(self) -> "ServiceCapability":
        if self.criticality in {ServiceCriticality.C0_SOURCE_TRUTH, ServiceCriticality.C1_CLINICAL_CONTEXT}:
            if self.routine_phi_control_plane_dependency:
                raise ValueError("core bedside truth/context may not require routine PHI in a shared control plane")
            if not self.hospital_local_fallback_required:
                raise ValueError("core bedside truth/context requires a hospital-local fallback path")
        return self


class ServiceCommitment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_id: str = Field(min_length=1)
    state: CommitmentState = CommitmentState.NOT_OFFERED
    target: str | None = None
    evidence_refs: tuple[str, ...] = ()
    staffed_on_call: bool = False
    target_environment_exercised: bool = False

    @model_validator(mode="after")
    def contracted_sla_requires_real_operational_evidence(self) -> "ServiceCommitment":
        if self.state == CommitmentState.CONTRACTED:
            if not self.target:
                raise ValueError("contracted service commitment requires a target")
            if not self.staffed_on_call:
                raise ValueError("contracted critical service requires staffed on-call coverage")
            if not self.target_environment_exercised:
                raise ValueError("contracted service commitment requires target-environment exercise evidence")
            if not self.evidence_refs:
                raise ValueError("contracted service commitment requires evidence refs")
        return self


class IncidentClassification(BaseModel):
    severity: IncidentSeverity
    reasons: tuple[str, ...]
    recommended_kill_scopes: tuple[KillScope, ...]
    hospital_notification_required: bool


def classify_incident(
    *,
    wrong_patient_risk: bool = False,
    unauthorized_action_risk: bool = False,
    corrupted_source_state: bool = False,
    multiple_sites_affected: bool = False,
    clinical_context_unavailable: bool = False,
    agent_only_unavailable: bool = False,
) -> IncidentClassification:
    reasons: list[str] = []
    kill: list[KillScope] = []

    if wrong_patient_risk:
        reasons.append("wrong-patient isolation may be compromised")
        kill.extend([KillScope.WORKFLOW, KillScope.SITE])
    if unauthorized_action_risk:
        reasons.append("unauthorized action capability may be exposed")
        kill.extend([KillScope.AGENT_VERSION, KillScope.TOOL])
    if corrupted_source_state:
        reasons.append("source lifecycle/freshness semantics may be corrupted")
        kill.extend([KillScope.ADAPTER, KillScope.WORKFLOW])
    if multiple_sites_affected:
        reasons.append("incident spans multiple provider sites")
        kill.append(KillScope.RELEASE)

    if reasons:
        return IncidentClassification(
            severity=IncidentSeverity.SEV0,
            reasons=tuple(dict.fromkeys(reasons)),
            recommended_kill_scopes=tuple(dict.fromkeys(kill)),
            hospital_notification_required=True,
        )

    if clinical_context_unavailable:
        return IncidentClassification(
            severity=IncidentSeverity.SEV1,
            reasons=("clinical context unavailable; legacy path required",),
            recommended_kill_scopes=(KillScope.SITE,),
            hospital_notification_required=True,
        )

    if agent_only_unavailable:
        return IncidentClassification(
            severity=IncidentSeverity.SEV2,
            reasons=("agent assistance unavailable while source-linked context remains available",),
            recommended_kill_scopes=(KillScope.MODEL, KillScope.AGENT_VERSION),
            hospital_notification_required=False,
        )

    return IncidentClassification(
        severity=IncidentSeverity.SEV3,
        reasons=("noncritical service degradation",),
        recommended_kill_scopes=(),
        hospital_notification_required=False,
    )


DEFAULT_SERVICE_CATALOG: tuple[ServiceCapability, ...] = (
    ServiceCapability(
        service_id="provider-source-access",
        criticality=ServiceCriticality.C0_SOURCE_TRUTH,
        routine_phi_control_plane_dependency=False,
        hospital_local_fallback_required=True,
        local_kill_scope=(KillScope.ADAPTER, KillScope.SITE),
        description="Provider-local source access and verification path. Legacy source remains authoritative fallback.",
    ),
    ServiceCapability(
        service_id="careos-context",
        criticality=ServiceCriticality.C1_CLINICAL_CONTEXT,
        routine_phi_control_plane_dependency=False,
        hospital_local_fallback_required=True,
        local_kill_scope=(KillScope.WORKFLOW, KillScope.SITE),
        description="Source-linked clinical context and lifecycle/provenance composition.",
    ),
    ServiceCapability(
        service_id="careos-agent-assist",
        criticality=ServiceCriticality.C2_AGENT_ASSIST,
        routine_phi_control_plane_dependency=False,
        hospital_local_fallback_required=True,
        local_kill_scope=(KillScope.MODEL, KillScope.AGENT_VERSION, KillScope.TOOL),
        description="Optional bounded model/agent assistance. Its failure must not remove source-linked context.",
    ),
)
