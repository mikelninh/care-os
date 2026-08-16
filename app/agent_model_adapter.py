from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

import httpx
from pydantic import BaseModel, ConfigDict, Field

from .agent_models import WorkerInput
from .agent_modes import AgentOperatingMode
from .agent_worker import AgentDraft, AgentToolProposal


class ModelEndpointPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    endpoint: str = Field(min_length=1)
    model_id: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
    allowed_host: str = Field(min_length=1)
    timeout_seconds: float = Field(default=15.0, gt=0, le=60)
    retain_or_train: bool = False

    def assert_allowed(self, mode: AgentOperatingMode) -> None:
        if mode not in {AgentOperatingMode.SYNTHETIC, AgentOperatingMode.DEIDENTIFIED_SANDBOX}:
            raise PermissionError("external/model adapter is disabled for live agent modes until separate approval")
        parsed = urlparse(self.endpoint)
        if parsed.scheme != "https":
            raise PermissionError("model endpoint must use HTTPS")
        if parsed.hostname != self.allowed_host:
            raise PermissionError("model endpoint host is outside policy")
        if self.retain_or_train:
            raise PermissionError("first CareOS model adapter does not permit retention/training on supplied context")


@dataclass
class HttpJsonReasoningWorker:
    """Provider-neutral JSON worker for synthetic/deidentified evaluation only.

    This adapter is not a hospital credential holder and never calls CareOS tools.
    It only proposes schema-constrained tool requests/drafts. The Agent Gateway still
    authorizes every tool call.
    """

    policy: ModelEndpointPolicy
    mode: AgentOperatingMode
    client: httpx.Client

    @property
    def model_id(self) -> str:
        return self.policy.model_id

    @property
    def model_version(self) -> str:
        return self.policy.model_version

    def _post(self, kind: str, payload: dict) -> dict:
        self.policy.assert_allowed(self.mode)
        response = self.client.post(
            self.policy.endpoint,
            json={"kind": kind, "model": self.policy.model_id, "input": payload},
            timeout=self.policy.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("model response must be a JSON object")
        return data

    def propose(self, item: WorkerInput) -> list[AgentToolProposal]:
        data = self._post(
            "tool_proposal",
            {
                "task": item.task,
                "source_text": item.source_text,
                "allowed_tool_ids": list(item.allowed_tool_ids),
                "allowed_data_categories": list(item.allowed_data_categories),
            },
        )
        proposals = data.get("proposals")
        if not isinstance(proposals, list):
            raise ValueError("model response missing proposals list")
        return [AgentToolProposal.model_validate(item) for item in proposals]

    def draft(self, *, facts: list[dict], task: str) -> AgentDraft:
        data = self._post("draft", {"task": task, "facts": facts})
        return AgentDraft.model_validate(data.get("draft"))
