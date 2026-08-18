import pytest

from app.clinical_context_graph import (
    ClinicalContextGraph,
    EdgeType,
    GraphEdge,
    GraphNode,
    NodeType,
)


def test_authoritative_fact_requires_provenance():
    with pytest.raises(ValueError, match="source/evidence provenance"):
        ClinicalContextGraph(
            patient_ref="P1",
            nodes=[
                GraphNode(node_id="P1", node_type=NodeType.PATIENT, patient_ref="P1"),
                GraphNode(node_id="fact:1", node_type=NodeType.FACT, patient_ref="P1", authoritative=True),
            ],
        )


def test_cross_patient_node_is_rejected():
    with pytest.raises(ValueError, match="cross-patient"):
        ClinicalContextGraph(
            patient_ref="P1",
            nodes=[
                GraphNode(node_id="P1", node_type=NodeType.PATIENT, patient_ref="P1"),
                GraphNode(node_id="fact:2", node_type=NodeType.FACT, patient_ref="P2"),
            ],
        )


def test_agent_produced_authoritative_fact_requires_human_review():
    nodes = [
        GraphNode(node_id="P1", node_type=NodeType.PATIENT, patient_ref="P1"),
        GraphNode(node_id="source:lab", node_type=NodeType.SOURCE, patient_ref="P1"),
        GraphNode(node_id="agent:1", node_type=NodeType.AGENT_RUN, patient_ref="P1"),
        GraphNode(node_id="fact:1", node_type=NodeType.FACT, patient_ref="P1", authoritative=True),
    ]
    edges = [
        GraphEdge(
            edge_id="e1",
            edge_type=EdgeType.ASSERTED_BY,
            from_node="fact:1",
            to_node="source:lab",
            patient_ref="P1",
            evidence_ref="Observation/1",
        ),
        GraphEdge(
            edge_id="e2",
            edge_type=EdgeType.PRODUCED_BY,
            from_node="fact:1",
            to_node="agent:1",
            patient_ref="P1",
        ),
    ]
    with pytest.raises(ValueError, match="human review"):
        ClinicalContextGraph(patient_ref="P1", nodes=nodes, edges=edges)


def test_agent_produced_fact_can_be_authoritative_after_source_evidence_and_human_review():
    nodes = [
        GraphNode(node_id="P1", node_type=NodeType.PATIENT, patient_ref="P1"),
        GraphNode(node_id="source:lab", node_type=NodeType.SOURCE, patient_ref="P1"),
        GraphNode(node_id="agent:1", node_type=NodeType.AGENT_RUN, patient_ref="P1"),
        GraphNode(node_id="human:1", node_type=NodeType.HUMAN, patient_ref="P1"),
        GraphNode(node_id="fact:1", node_type=NodeType.FACT, patient_ref="P1", authoritative=True),
    ]
    edges = [
        GraphEdge(
            edge_id="e1",
            edge_type=EdgeType.ASSERTED_BY,
            from_node="fact:1",
            to_node="source:lab",
            patient_ref="P1",
            evidence_ref="Observation/1",
        ),
        GraphEdge(
            edge_id="e2",
            edge_type=EdgeType.PRODUCED_BY,
            from_node="fact:1",
            to_node="agent:1",
            patient_ref="P1",
        ),
        GraphEdge(
            edge_id="e3",
            edge_type=EdgeType.REVIEWED_BY,
            from_node="fact:1",
            to_node="human:1",
            patient_ref="P1",
        ),
    ]
    graph = ClinicalContextGraph(patient_ref="P1", nodes=nodes, edges=edges)
    assert graph.nodes_of_type(NodeType.FACT)[0].node_id == "fact:1"
