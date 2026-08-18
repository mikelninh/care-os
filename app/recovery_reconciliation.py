from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from .artifact_invalidation import DerivedArtifact, InvalidationResult, invalidate_downstream_artifacts
from .clinical_graph import ClinicalContextGraph
from .resilience_mode import DependencyState, OperatingMode, ResilienceDecision, decide_resilience


class RecoveryReconciliationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    patient_ref: str
    before: ResilienceDecision
    invalidation: InvalidationResult
    after: ResilienceDecision
    reconciled_fact_ids: tuple[str, ...]


def reconcile_after_outage(
    *,
    graph: ClinicalContextGraph,
    artifacts: list[DerivedArtifact],
    changed_fact_ids: set[str],
    model_available: bool = True,
) -> RecoveryReconciliationResult:
    before = decide_resilience(
        DependencyState(
            source_truth_available=True,
            source_current=True,
            identity_available=True,
            audit_available=True,
            model_available=model_available,
            network_available=True,
            legacy_fallback_available=True,
            recovery_reconciled=False,
        )
    )
    if before.mode != OperatingMode.RECOVERY:
        raise RuntimeError("recovery reconciliation must start in recovery mode")

    invalidation = invalidate_downstream_artifacts(
        graph=graph,
        artifacts=artifacts,
        changed_fact_ids=changed_fact_ids,
        actor_id="careos-recovery-reconciler",
    )

    after = decide_resilience(
        DependencyState(
            source_truth_available=True,
            source_current=True,
            identity_available=True,
            audit_available=True,
            model_available=model_available,
            network_available=True,
            legacy_fallback_available=True,
            recovery_reconciled=True,
        )
    )
    return RecoveryReconciliationResult(
        patient_ref=graph.patient_ref,
        before=before,
        invalidation=invalidation,
        after=after,
        reconciled_fact_ids=tuple(sorted(changed_fact_ids)),
    )
