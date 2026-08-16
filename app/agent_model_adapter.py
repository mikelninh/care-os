from __future__ import annotations

import json
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
    allowed_port: int = Field(default=443, ge=1, le=65535)
    timeout_seconds: float = Field(default=15.0, gt=0, le=60)
    retain_or_train: bool = False
    max_request_bytes: int = Field(default=131_072, ge=1_024, le=2_000_000)
    max_response_bytes: int = Field(default=262_144, ge=1_024, le=4_000_000)
    max_proposals: int = Field(default=8, ge=1, le=32)

    def assert_allowed(self, mode: AgentOperatingMode) -> None:
        if mode not in {AgentOperatingMode.SYNTHETIC, AgentOperatingMode.DEIDENTIFIED_SANDBOX}:
            raise PermissionError("external/model adapter is disabled for live agent modes until separate approval")
        parsed = urlparse(self.endpoint)
        if parsed.scheme != "https":
            raise PermissionError("model endpoint must use HTTPS")
        if parsed.username or parsed.password:
            raise PermissionError("model endpoint must not embed credentials")
        if parsed.fragment:
            raise PermissionError("model endpoint must not contain a URL fragment")
        if parsed.hostname != self.allowed_host:
            raise PermissionError("model endpoint host is outside policy")
        endpoint_port = parsed.port or 443
        if endpoint_port != self.allowed_port:
            raise PermissionError("model endpoint port is outside policy")
        if self.retain_or_train:
            raise PermissionError("first CareOS model adapter does not permit retention/training on supplied context")


@dataclass
class HttpJsonReasoningWorker:
    """Provider-neutral JSON worker for synthetic/deidentified evaluation only.

    This adapter is not a hospital credential holder and never calls CareOS tools.
    It only proposes schema-constrained tool requests/drafts. The Agent Gateway still
    authorizes every tool call. Redirects, oversized requests/responses and proposal
    floods are rejected before model output can influence the gateway.
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
        body = {"kind": kind, "model": self.policy.model_id, "input": payload}
        encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        if len(encoded) > self.policy.max_request_bytes:
            raise ValueError("model request exceeds configured size limit")

        response = self.client.post(
            self.policy.endpoint,
            content=encoded,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=self.policy.timeout_seconds,
            follow_redirects=False,
        )
        if 300 <= response.status_code < 400:
            raise PermissionError("model endpoint redirects are forbidden")

        content_length = response.headers.get("content-length")
        if content_length:
            try:
                if int(content_length) > self.policy.max_response_bytes:
                    raise ValueError("model response exceeds configured size limit")
            except ValueError as exc:
                if "exceeds" in str(exc):
                    raise
                raise ValueError("invalid model response Content-Length") from exc

        response.raise_for_status()
        raw = response.content
        if len(raw) > self.policy.max_response_bytes:
            raise ValueError("model response exceeds configured size limit")
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("model response must be valid JSON") from exc
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
        if len(proposals) > self.policy.max_proposals:
            raise ValueError("model returned too many tool proposals")
        return [AgentToolProposal.model_validate(item) for item in proposals]

    def draft(self, *, facts: list[dict], task: str) -> AgentDraft:
        data = self._post("draft", {"task": task, "facts": facts})
        return AgentDraft.model_validate(data.get("draft"))
