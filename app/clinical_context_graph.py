from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class NodeType(str, Enum):
    PATIENT = "patient"
    ENCOUNTER = "encounter"
    FACT = "fact"
    SOURCE = "source"
    DOCUMENT = "document"
    SPECIMEN = "specimen"
    TASK = "task"
    DECISION = "decision"
    HUMAN = "human"
    ORGANISATION = "organisation"
    AGENT_RUN = "agent-run"
    ACCESS_EVENT = "access-event"


class EdgeType(str, Enum):
    HAS_ENCOUNTER = "has-encounter"
    ABOUT_PATIENT = "about-patient"
    ASSERTED_BY = "asserted-by"
    DERIVED_FROM = "derived-from"
    SUPERSEDES = "supersedes"
    CONTRADICTS = "contradicts"
    SUPPORTS = "supports"
    REVIEWED_BY = "reviewed-by"
    AUTHORED_BY = "authored-by"
    ASSIGNED_TO = "assigned-to"
    PRODUCED_BY = "produced-by"
    ACCESSED_BY = "accessed-by"
    ISSUED_BY = "issued-by"
    RELATED_TO = "related-to"


class GraphNode(BaseModel):
    node_id: str = Field(min_length=1)
    node_type: NodeType
    patient_ref: str | None = None
    label: str | None = None
    source_ref: str | None = None
    lifecycle_state: str | None = None
    effective_time: datetime | None = None
    recorded_time: datetime | None = None
    authoritative: bool = False


class GraphEdge(BaseModel):
    edge_id: str = Field(min_length=1)
    edge_type: EdgeType
    from_node: str
    to_node: str
    patient_ref: str | None = None
    evidence_ref: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = "system"


class ClinicalContextGraph(BaseModel):
    patient_ref: str
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_graph_contract(self) -> "ClinicalContextGraph":
        by_id = {node.node_id: node for node in self.nodes}
        if len(by_id) != len(self.nodes):
            raise ValueError("duplicate graph node_id")
        edge_ids = {edge.edge_id for edge in self.edges}
        if len(edge_ids) != len(self.edges):
            raise ValueError("duplicate graph edge_id")

        for node in self.nodes:
            if node.patient_ref and node.patient_ref != self.patient_ref:
                raise ValueError("cross-patient graph node rejected")
            if node.node_type == NodeType.PATIENT and node.node_id != self.patient_ref:
                raise ValueError("patient node must use graph patient_ref as node_id")

        for edge in self.edges:
            if edge.from_node not in by_id or edge.to_node not in by_id:
                raise ValueError("graph edge references unknown node")
            if edge.patient_ref and edge.patient_ref != self.patient_ref:
                raise ValueError("cross-patient graph edge rejected")

        # Consequential authoritative facts/decisions must not float without evidence.
        incoming: dict[str, list[GraphEdge]] = {}
        for edge in self.edges:
            incoming.setdefault(edge.to_node, []).append(edge)

        for node in self.nodes:
            if not node.authoritative:
                continue
            if node.node_type == NodeType.FACT:
                evidence_edges = [
                    edge
                    for edge in self.edges
                    if edge.from_node == node.node_id
                    and edge.edge_type in {EdgeType.ASSERTED_BY, EdgeType.DERIVED_FROM}
                    and edge.evidence_ref
                ]
                if not evidence_edges and not node.source_ref:
                    raise ValueError("authoritative fact requires source/evidence provenance")
            if node.node_type == NodeType.DECISION:
                support = [
                    edge
                    for edge in self.edges
                    if edge.from_node == node.node_id and edge.edge_type in {EdgeType.SUPPORTS, EdgeType.REVIEWED_BY}
                ]
                if not support:
                    raise ValueError("authoritative decision requires support/review relationship")

        # Agent output cannot become authoritative merely by being produced.
        for node in self.nodes:
            if node.authoritative and node.node_type in {NodeType.FACT, NodeType.DECISION}:
                producers = [
                    edge
                    for edge in self.edges
                    if edge.from_node == node.node_id and edge.edge_type == EdgeType.PRODUCED_BY
                ]
                if any(by_id[edge.to_node].node_type == NodeType.AGENT_RUN for edge in producers):
                    human_review = [
                        edge
                        for edge in self.edges
                        if edge.from_node == node.node_id
                        and edge.edge_type == EdgeType.REVIEWED_BY
                        and by_id[edge.to_node].node_type == NodeType.HUMAN
                    ]
                    if not human_review:
                        raise ValueError("agent-produced authoritative node requires explicit human review")

        return self

    def nodes_of_type(self, node_type: NodeType) -> list[GraphNode]:
        return [node for node in self.nodes if node.node_type == node_type]

    def neighbors(self, node_id: str, edge_type: EdgeType | None = None) -> list[GraphNode]:
        by_id = {node.node_id: node for node in self.nodes}
        targets: list[GraphNode] = []
        for edge in self.edges:
            if edge.from_node != node_id:
                continue
            if edge_type and edge.edge_type != edge_type:
                continue
            targets.append(by_id[edge.to_node])
        return targets
