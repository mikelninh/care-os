from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .clinical_truth import ClinicalFact, TruthEnvelope


class NodeKind(str, Enum):
    PATIENT = "patient"
    FACT = "fact"
    ENCOUNTER = "encounter"
    TASK = "task"
    ARTIFACT = "artifact"
    ACTOR = "actor"


class RelationKind(str, Enum):
    BELONGS_TO = "belongs-to"
    SUPPORTS = "supports"
    SUPERSEDES = "supersedes"
    CONTRADICTS = "contradicts"
    DERIVED_FROM = "derived-from"
    AFFECTS = "affects"
    CREATED_BY = "created-by"
    REVIEWED_BY = "reviewed-by"


class AssertionKind(str, Enum):
    SOURCE = "source"
    DETERMINISTIC_DERIVATION = "deterministic-derivation"
    HUMAN = "human"
    AGENT_PROPOSAL = "agent-proposal"


class GraphNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    node_id: str = Field(min_length=1)
    patient_ref: str = Field(min_length=1)
    kind: NodeKind
    label: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    edge_id: str = Field(min_length=1)
    patient_ref: str = Field(min_length=1)
    source_node_id: str = Field(min_length=1)
    target_node_id: str = Field(min_length=1)
    relation: RelationKind
    assertion: AssertionKind
    evidence_fact_ids: tuple[str, ...] = ()
    transformer: str | None = None
    transformer_version: str | None = None

    @model_validator(mode="after")
    def derivation_requires_lineage(self) -> "GraphEdge":
        if self.assertion == AssertionKind.DETERMINISTIC_DERIVATION:
            if not self.evidence_fact_ids:
                raise ValueError("derived graph relations require evidence_fact_ids")
            if not self.transformer or not self.transformer_version:
                raise ValueError("derived graph relations require transformer + version")
        if self.assertion == AssertionKind.AGENT_PROPOSAL and not self.transformer:
            raise ValueError("agent-proposal relation requires the proposing agent/model identity")
        return self


class ClinicalContextGraph(BaseModel):
    """Patient-local, reconstructable graph over source-linked clinical facts.

    This is a derived navigation/reasoning surface, never a replacement source of
    clinical authority. Consequential nodes/relations must trace to source facts,
    deterministic transformations or explicit human/agent artifacts.
    """

    model_config = ConfigDict(extra="forbid")

    patient_ref: str = Field(min_length=1)
    nodes: list[GraphNode]
    edges: list[GraphEdge]

    @model_validator(mode="after")
    def enforce_patient_partition_and_references(self) -> "ClinicalContextGraph":
        node_ids = [node.node_id for node in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError("duplicate graph node_id")
        edge_ids = [edge.edge_id for edge in self.edges]
        if len(edge_ids) != len(set(edge_ids)):
            raise ValueError("duplicate graph edge_id")

        wrong_nodes = [node.node_id for node in self.nodes if node.patient_ref != self.patient_ref]
        wrong_edges = [edge.edge_id for edge in self.edges if edge.patient_ref != self.patient_ref]
        if wrong_nodes or wrong_edges:
            raise ValueError(f"cross-patient graph content rejected: nodes={wrong_nodes}, edges={wrong_edges}")

        known = set(node_ids)
        dangling = [
            edge.edge_id
            for edge in self.edges
            if edge.source_node_id not in known or edge.target_node_id not in known
        ]
        if dangling:
            raise ValueError(f"graph contains dangling edges: {dangling}")
        return self

    def downstream(self, node_id: str, relation: RelationKind | None = None) -> list[GraphNode]:
        node_map = {node.node_id: node for node in self.nodes}
        target_ids = {
            edge.target_node_id
            for edge in self.edges
            if edge.source_node_id == node_id and (relation is None or edge.relation == relation)
        }
        return [node_map[node_id] for node_id in target_ids]

    def evidence_for_edge(self, edge_id: str) -> tuple[str, ...]:
        for edge in self.edges:
            if edge.edge_id == edge_id:
                return edge.evidence_fact_ids
        raise KeyError(edge_id)


def _fact_payload(fact: ClinicalFact) -> dict[str, Any]:
    return {
        "fact_type": fact.fact_type,
        "logical_key": fact.logical_key,
        "value_original": fact.value_original,
        "value_normalized": fact.value_normalized,
        "code": fact.code,
        "code_system": fact.code_system,
        "effective_time": fact.effective_time.isoformat() if fact.effective_time else None,
        "recorded_time": fact.recorded_time.isoformat() if fact.recorded_time else None,
        "status": fact.status.value,
        "assertion_stage": fact.assertion_stage.value,
        "source_system": fact.source.system,
        "source_resource_type": fact.source.resource_type,
        "source_resource_id": fact.source.resource_id,
        "source_resource_version": fact.source.resource_version,
        "document_id": fact.source.document_id,
        "evidence_span": fact.source.evidence_span,
        "transformer": fact.transformer,
        "transformer_version": fact.transformer_version,
    }


def graph_from_truth(envelope: TruthEnvelope) -> ClinicalContextGraph:
    patient_node_id = f"patient:{envelope.patient_ref}"
    nodes = [
        GraphNode(
            node_id=patient_node_id,
            patient_ref=envelope.patient_ref,
            kind=NodeKind.PATIENT,
            label=envelope.patient_ref,
        )
    ]
    edges: list[GraphEdge] = []

    facts_by_id = {fact.fact_id: fact for fact in envelope.facts}
    contradiction_groups: dict[str, list[ClinicalFact]] = {}

    for fact in envelope.facts:
        fact_node_id = f"fact:{fact.fact_id}"
        nodes.append(
            GraphNode(
                node_id=fact_node_id,
                patient_ref=envelope.patient_ref,
                kind=NodeKind.FACT,
                label=fact.fact_type,
                payload=_fact_payload(fact),
            )
        )
        edges.append(
            GraphEdge(
                edge_id=f"belongs:{fact.fact_id}",
                patient_ref=envelope.patient_ref,
                source_node_id=fact_node_id,
                target_node_id=patient_node_id,
                relation=RelationKind.BELONGS_TO,
                assertion=AssertionKind.SOURCE,
                evidence_fact_ids=(fact.fact_id,),
            )
        )
        if fact.supersedes_fact_id and fact.supersedes_fact_id in facts_by_id:
            edges.append(
                GraphEdge(
                    edge_id=f"supersedes:{fact.fact_id}:{fact.supersedes_fact_id}",
                    patient_ref=envelope.patient_ref,
                    source_node_id=fact_node_id,
                    target_node_id=f"fact:{fact.supersedes_fact_id}",
                    relation=RelationKind.SUPERSEDES,
                    assertion=AssertionKind.SOURCE,
                    evidence_fact_ids=(fact.fact_id, fact.supersedes_fact_id),
                )
            )
        if fact.contradiction_group:
            contradiction_groups.setdefault(fact.contradiction_group, []).append(fact)

    for group, facts in contradiction_groups.items():
        for i, left in enumerate(facts):
            for right in facts[i + 1 :]:
                edges.append(
                    GraphEdge(
                        edge_id=f"contradicts:{group}:{left.fact_id}:{right.fact_id}",
                        patient_ref=envelope.patient_ref,
                        source_node_id=f"fact:{left.fact_id}",
                        target_node_id=f"fact:{right.fact_id}",
                        relation=RelationKind.CONTRADICTS,
                        assertion=AssertionKind.DETERMINISTIC_DERIVATION,
                        evidence_fact_ids=(left.fact_id, right.fact_id),
                        transformer="contradiction-group",
                        transformer_version="1",
                    )
                )

    return ClinicalContextGraph(patient_ref=envelope.patient_ref, nodes=nodes, edges=edges)
