import pytest

from app.artifact_invalidation import (
    ArtifactDependency,
    ArtifactKind,
    ArtifactState,
    DerivedArtifact,
    InvalidationReason,
    invalidate_downstream_artifacts,
)
from app.clinical_graph import AssertionKind, ClinicalContextGraph, GraphEdge, GraphNode, NodeKind, RelationKind


def graph():
    patient = "patient-001"
    nodes = [
        GraphNode(node_id=f"patient:{patient}", patient_ref=patient, kind=NodeKind.PATIENT, label=patient),
        GraphNode(node_id="fact:lab-v1", patient_ref=patient, kind=NodeKind.FACT, label="microbiology"),
        GraphNode(node_id="fact:lab-v2", patient_ref=patient, kind=NodeKind.FACT, label="microbiology"),
        GraphNode(node_id="fact:therapy", patient_ref=patient, kind=NodeKind.FACT, label="therapy"),
    ]
    edges = [
        GraphEdge(
            edge_id="supersedes:lab-v2:lab-v1",
            patient_ref=patient,
            source_node_id="fact:lab-v2",
            target_node_id="fact:lab-v1",
            relation=RelationKind.SUPERSEDES,
            assertion=AssertionKind.SOURCE,
            evidence_fact_ids=("lab-v2", "lab-v1"),
        ),
        GraphEdge(
            edge_id="contradicts:lab-v2:therapy",
            patient_ref=patient,
            source_node_id="fact:lab-v2",
            target_node_id="fact:therapy",
            relation=RelationKind.CONTRADICTS,
            assertion=AssertionKind.DETERMINISTIC_DERIVATION,
            evidence_fact_ids=("lab-v2", "therapy"),
            transformer="synthetic-contradiction",
            transformer_version="1",
        ),
    ]
    return ClinicalContextGraph(patient_ref=patient, nodes=nodes, edges=edges)


def artifact(artifact_id, kind, state, fact_id):
    return DerivedArtifact(
        artifact_id=artifact_id,
        patient_ref="patient-001",
        kind=kind,
        state=state,
        dependencies=(
            ArtifactDependency(fact_id=fact_id, transformer="draft-builder", transformer_version="1"),
        ),
    )


def test_corrected_fact_reopens_ai_draft_that_used_superseded_support():
    result = invalidate_downstream_artifacts(
        graph=graph(),
        artifacts=[artifact("draft-1", ArtifactKind.AI_DRAFT, ArtifactState.CURRENT, "lab-v1")],
        changed_fact_ids={"lab-v2"},
    )
    assert result.artifacts[0].state == ArtifactState.REVIEW_REQUIRED
    assert result.invalidations[0].reason == InvalidationReason.SUPPORT_SUPERSEDED
    assert result.invalidations[0].artifact_was_mutated is True
    assert result.invalidations[0].audit_event["action"] == "artifact-invalidated"


def test_signed_human_artifact_is_flagged_but_never_rewritten():
    signed = artifact("signed-note", ArtifactKind.HUMAN_SIGNED, ArtifactState.SIGNED_IMMUTABLE, "lab-v1")
    result = invalidate_downstream_artifacts(graph=graph(), artifacts=[signed], changed_fact_ids={"lab-v2"})
    assert result.artifacts[0] == signed
    assert result.invalidations[0].artifact_was_mutated is False
    assert result.invalidations[0].requires_human_review is True
    assert result.invalidations[0].audit_event["action"] == "signed-artifact-review-flagged"


def test_contradiction_change_reopens_dependent_context():
    result = invalidate_downstream_artifacts(
        graph=graph(),
        artifacts=[artifact("context-1", ArtifactKind.DERIVED_CONTEXT, ArtifactState.CURRENT, "therapy")],
        changed_fact_ids={"lab-v2"},
    )
    assert result.artifacts[0].state == ArtifactState.REVIEW_REQUIRED
    assert result.invalidations[0].reason == InvalidationReason.CONTRADICTION_CHANGED


def test_cross_patient_artifact_is_rejected():
    foreign = DerivedArtifact(
        artifact_id="foreign",
        patient_ref="patient-999",
        kind=ArtifactKind.AI_DRAFT,
        state=ArtifactState.CURRENT,
        dependencies=(ArtifactDependency(fact_id="lab-v1", transformer="x", transformer_version="1"),),
    )
    with pytest.raises(ValueError, match="cross-patient"):
        invalidate_downstream_artifacts(graph=graph(), artifacts=[foreign], changed_fact_ids={"lab-v2"})


def test_unknown_changed_fact_is_rejected():
    with pytest.raises(ValueError, match="not present"):
        invalidate_downstream_artifacts(graph=graph(), artifacts=[], changed_fact_ids={"fact-does-not-exist"})
