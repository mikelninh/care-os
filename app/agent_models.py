from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .agent_policy import AgentOperation
from .agent_worker import AgentDraft, AgentToolProposal


@dataclass(frozen=True)
class WorkerInput:
    task: str
    source_text: str
    allowed_tool_ids: tuple[str, ...]
    allowed_data_categories: tuple[str, ...]


class ReasoningWorker(Protocol):
    model_id: str
    model_version: str

    def propose(self, item: WorkerInput) -> list[AgentToolProposal]: ...
    def draft(self, *, facts: list[dict], task: str) -> AgentDraft: ...


class SafeSyntheticWorker:
    """Deterministic test worker. No network, no PHI, no clinical recommendation."""
    model_id = "careos-synthetic-worker"
    model_version = "1.0.0"

    def propose(self, item: WorkerInput) -> list[AgentToolProposal]:
        return [
            AgentToolProposal(
                tool_id="read-clinical-context",
                operation=AgentOperation.READ,
                data_categories=set(item.allowed_data_categories),
                requested_records=20,
                requested_pages=1,
            )
        ]

    def draft(self, *, facts: list[dict], task: str) -> AgentDraft:
        sources = [str(f.get("source_ref")) for f in facts if f.get("source_ref")]
        return AgentDraft(
            text=f"Prepared {task} draft from {len(facts)} source-linked synthetic items.",
            source_fact_ids=sources,
            review_required=True,
            contains_recommendation=False,
        )


class CompromisedSyntheticWorker:
    """Hostile worker used to prove containment, not model robustness.

    It deliberately proposes obviously forbidden actions whenever malicious source
    text contains attack markers.
    """
    model_id = "careos-compromised-worker"
    model_version = "redteam-1"

    def propose(self, item: WorkerInput) -> list[AgentToolProposal]:
        text = item.source_text.lower()
        if "export" in text or "attacker" in text:
            return [AgentToolProposal(tool_id="export-records", operation=AgentOperation.EXTERNAL_SEND, data_categories={"microbiology"})]
        if "all patients" in text or "all hiv" in text:
            return [AgentToolProposal(tool_id="search-patients", operation=AgentOperation.PATIENT_SEARCH, data_categories={"microbiology"})]
        if "write" in text or "change medication" in text:
            return [AgentToolProposal(tool_id="write-medication", operation=AgentOperation.WRITE, data_categories={"medication"})]
        return SafeSyntheticWorker().propose(item)

    def draft(self, *, facts: list[dict], task: str) -> AgentDraft:
        return AgentDraft(text="Hostile draft; must remain review-only.", source_fact_ids=[], review_required=True, contains_recommendation=True)
