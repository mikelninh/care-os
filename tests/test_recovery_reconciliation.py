from app.artifact_invalidation import ArtifactDependency, ArtifactKind, ArtifactState, DerivedArtifact
from app.clinical_graph import AssertionKind, ClinicalContextGraph, GraphEdge, GraphNode, NodeKind, RelationKind
from app.recovery_reconciliation import reconcile_after_outage
from app.resilience_mode import OperatingMode


def test_corrected_result_during_outage_reopens_dependent_draft_before_normal_mode():
    patient = "synthetic-patient-001"
    graph = ClinicalContextGraph(
        patient_ref=patient,
        nodes=[
            GraphNode(node_id=f"patient:{patient}", patient_ref=patient, kind=NodeKind.PATIENT, label=patient),
            GraphNode(node_id="fact:result-v1", patient_ref=patient, kind=NodeKind.FACT, label="lab"),
            GraphNode(node_id="fact:result-v2", patient_ref=patient, kind=NodeKind.FACT, label="lab"),
        ],
        edges=[
            GraphEdge(
                edge_id="supersedes:result-v2:result-v1",
                patient_ref=patient,
                source_node_id="fact:result-v2",
                target_node_id="fact:result-v1",
                relation=RelationKind.SUPERSEDES,
                assertion=AssertionKind.SOURCE,
                evidence_fact_ids=("result-v2", "result-v1"),
            )
        ],
    )
    draft = DerivedArtifact(
        artifact_id="draft-before-outage",
        patient_ref=patient,
        kind=ArtifactKind.AI_DRAFT,
        state=ArtifactState.CURRENT,
        dependencies=(ArtifactDependency(fact_id="result-v1", transformer="draft-builder", transformer_version="1"),),
    )

    result = reconcile_after_outage(graph=graph, artifacts=[draft], changed_fact_ids={"result-v2"})

    assert result.before.mode == OperatingMode.RECOVERY
    assert result.invalidation.artifacts[0].state == ArtifactState.REVIEW_REQUIRED
    assert result.invalidation.invalidations[0].audit_event["action"] == "artifact-invalidated"
    assert result.after.mode == OperatingMode.NORMAL
    assert result.reconciled_fact_ids == ("result-v2",)
