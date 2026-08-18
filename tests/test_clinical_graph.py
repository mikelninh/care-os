from datetime import datetime, timezone

import pytest

from app.clinical_graph import (
    AssertionKind,
    ClinicalContextGraph,
    GraphEdge,
    GraphNode,
    NodeKind,
    RelationKind,
    graph_from_truth,
)
from app.clinical_truth import AssertionStage, ClinicalFact, SourceKind, SourceRef, TruthEnvelope


def fact(fact_id: str, *, value: str, contradiction_group=None, supersedes=None):
    return ClinicalFact(
        fact_id=fact_id,
        patient_ref="p1",
        fact_type="laboratory",
        logical_key="crp",
        value_original=value,
        effective_time=datetime(2026, 8, 18, tzinfo=timezone.utc),
        source=SourceRef(
            kind=SourceKind.FHIR,
            system="lis",
            resource_type="Observation",
            resource_id=fact_id,
            resource_version="1",
        ),
        assertion_stage=AssertionStage.FINAL,
        contradiction_group=contradiction_group,
        supersedes_fact_id=supersedes,
    )


def test_graph_preserves_source_linked_facts_and_supersession():
    old = fact("old", value="10")
    corrected = fact("new", value="12", supersedes="old")
    graph = graph_from_truth(TruthEnvelope(patient_ref="p1", facts=[old, corrected]))
    assert any(edge.relation == RelationKind.SUPERSEDES for edge in graph.edges)
    edge = next(edge for edge in graph.edges if edge.relation == RelationKind.SUPERSEDES)
    assert set(edge.evidence_fact_ids) == {"old", "new"}


def test_contradiction_relation_is_explicit_deterministic_derivation():
    left = fact("a", value="positive", contradiction_group="g1")
    right = fact("b", value="negative", contradiction_group="g1")
    graph = graph_from_truth(TruthEnvelope(patient_ref="p1", facts=[left, right]))
    edge = next(edge for edge in graph.edges if edge.relation == RelationKind.CONTRADICTS)
    assert edge.assertion == AssertionKind.DETERMINISTIC_DERIVATION
    assert set(edge.evidence_fact_ids) == {"a", "b"}


def test_cross_patient_graph_node_is_rejected():
    with pytest.raises(ValueError, match="cross-patient"):
        ClinicalContextGraph(
            patient_ref="p1",
            nodes=[GraphNode(node_id="p", patient_ref="p2", kind=NodeKind.PATIENT, label="wrong")],
            edges=[],
        )


def test_derived_relation_requires_evidence_and_transformer():
    with pytest.raises(ValueError, match="evidence_fact_ids"):
        GraphEdge(
            edge_id="e",
            patient_ref="p1",
            source_node_id="a",
            target_node_id="b",
            relation=RelationKind.DERIVED_FROM,
            assertion=AssertionKind.DETERMINISTIC_DERIVATION,
        )
