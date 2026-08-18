from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .audit import make_audit_event
from .clinical_graph import ClinicalContextGraph, RelationKind


class ArtifactKind(str, Enum):
    AI_DRAFT = "ai-draft"
    DERIVED_CONTEXT = "derived-context"
    HUMAN_SIGNED = "human-signed"


class ArtifactState(str, Enum):
    CURRENT = "current"
    REVIEW_REQUIRED = "review-required"
    SIGNED_IMMUTABLE = "signed-immutable"


class ArtifactDependency(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fact_id: str = Field(min_length=1)
    transformer: str = Field(min_length=1)
    transformer_version: str = Field(min_length=1)


class DerivedArtifact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(min_length=1)
    patient_ref: str = Field(min_length=1)
    kind: ArtifactKind
    state: ArtifactState
    dependencies: tuple[ArtifactDependency, ...]

    @model_validator(mode="after")
    def signed_artifact_must_be_immutable(self) -> "DerivedArtifact":
        if self.kind == ArtifactKind.HUMAN_SIGNED and self.state != ArtifactState.SIGNED_IMMUTABLE:
            raise ValueError("human-signed artifacts must remain signed-immutable")
        if self.kind != ArtifactKind.HUMAN_SIGNED and self.state == ArtifactState.SIGNED_IMMUTABLE:
            raise ValueError("only human-signed artifacts may use signed-immutable state")
        return self


class InvalidationReason(str, Enum):
    SUPPORT_SUPERSEDED = "support-superseded"
    CONTRADICTION_CHANGED = "contradiction-changed"
    SUPPORT_CHANGED = "support-changed"


class ArtifactInvalidation(BaseModel):
    artifact_id: str
    patient_ref: str
    changed_fact_ids: tuple[str, ...]
    affected_fact_ids: tuple[str, ...]
    reason: InvalidationReason
    artifact_was_mutated: bool
    requires_human_review: bool
    audit_event: dict


class InvalidationResult(BaseModel):
    patient_ref: str
    artifacts: list[DerivedArtifact]
    invalidations: list[ArtifactInvalidation]


def _affected_fact_ids(graph: ClinicalContextGraph, changed_fact_ids: set[str]) -> tuple[set[str], dict[str, InvalidationReason]]:
    affected = set(changed_fact_ids)
    reasons: dict[str, InvalidationReason] = {fact_id: InvalidationReason.SUPPORT_CHANGED for fact_id in changed_fact_ids}

    for edge in graph.edges:
        source_fact = edge.source_node_id.removeprefix("fact:") if edge.source_node_id.startswith("fact:") else None
        target_fact = edge.target_node_id.removeprefix("fact:") if edge.target_node_id.startswith("fact:") else None
        if edge.relation == RelationKind.SUPERSEDES and source_fact in changed_fact_ids and target_fact:
            affected.add(target_fact)
            reasons[target_fact] = InvalidationReason.SUPPORT_SUPERSEDED
        if edge.relation == RelationKind.CONTRADICTS and ({source_fact, target_fact} & changed_fact_ids):
            for fact_id in (source_fact, target_fact):
                if fact_id:
                    affected.add(fact_id)
                    reasons[fact_id] = InvalidationReason.CONTRADICTION_CHANGED
    return affected, reasons


def invalidate_downstream_artifacts(
    *,
    graph: ClinicalContextGraph,
    artifacts: list[DerivedArtifact],
    changed_fact_ids: set[str],
    actor_id: str = "careos-artifact-invalidator",
) -> InvalidationResult:
    if not changed_fact_ids:
        return InvalidationResult(patient_ref=graph.patient_ref, artifacts=artifacts, invalidations=[])

    wrong_patient = [artifact.artifact_id for artifact in artifacts if artifact.patient_ref != graph.patient_ref]
    if wrong_patient:
        raise ValueError(f"cross-patient artifact invalidation rejected: {wrong_patient}")

    graph_fact_ids = {
        node.node_id.removeprefix("fact:")
        for node in graph.nodes
        if node.node_id.startswith("fact:")
    }
    unknown = changed_fact_ids - graph_fact_ids
    if unknown:
        raise ValueError(f"changed facts are not present in the patient graph: {sorted(unknown)}")

    affected, reason_by_fact = _affected_fact_ids(graph, changed_fact_ids)
    updated: list[DerivedArtifact] = []
    invalidations: list[ArtifactInvalidation] = []

    for artifact in artifacts:
        dependency_ids = {dependency.fact_id for dependency in artifact.dependencies}
        matched = sorted(dependency_ids & affected)
        if not matched:
            updated.append(artifact)
            continue

        reason = next(
            (reason_by_fact[fact_id] for fact_id in matched if reason_by_fact[fact_id] != InvalidationReason.SUPPORT_CHANGED),
            InvalidationReason.SUPPORT_CHANGED,
        )
        mutable = artifact.kind != ArtifactKind.HUMAN_SIGNED
        replacement = (
            artifact.model_copy(update={"state": ArtifactState.REVIEW_REQUIRED})
            if mutable
            else artifact
        )
        updated.append(replacement)
        audit_event = make_audit_event(
            actor_id=actor_id,
            patient_id=graph.patient_ref,
            action="artifact-invalidated" if mutable else "signed-artifact-review-flagged",
            resource_type="derived-artifact",
            resource_id=artifact.artifact_id,
            outcome="review-required",
            audit_level="safety",
            reason_code=reason.value,
        )
        invalidations.append(
            ArtifactInvalidation(
                artifact_id=artifact.artifact_id,
                patient_ref=graph.patient_ref,
                changed_fact_ids=tuple(sorted(changed_fact_ids)),
                affected_fact_ids=tuple(matched),
                reason=reason,
                artifact_was_mutated=mutable,
                requires_human_review=True,
                audit_event=audit_event,
            )
        )

    return InvalidationResult(patient_ref=graph.patient_ref, artifacts=updated, invalidations=invalidations)
