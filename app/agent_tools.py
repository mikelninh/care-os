from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, model_validator

from .agent_policy import AgentOperation


class ToolTrustTier(str, Enum):
    INTERNAL = "internal"
    PROVIDER_MANAGED = "provider_managed"
    EXTERNAL = "external"


class ToolSpec(BaseModel):
    tool_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    owner: str = Field(min_length=1)
    trust_tier: ToolTrustTier
    operation: AgentOperation
    target_system: str = Field(min_length=1)
    data_categories: set[str] = Field(default_factory=set)
    patient_scoped: bool = True
    allowed_egress_hosts: set[str] = Field(default_factory=set)
    max_records_per_call: int = Field(default=100, ge=1, le=10_000)
    max_pages_per_call: int = Field(default=10, ge=1, le=100)
    timeout_seconds: int = Field(default=20, ge=1, le=300)
    idempotent: bool = True
    requires_audit: bool = True
    requires_human_confirmation: bool = False
    enabled: bool = True

    @model_validator(mode="after")
    def validate_effect(self) -> "ToolSpec":
        if self.operation in {AgentOperation.WRITE, AgentOperation.EXTERNAL_SEND}:
            if not self.requires_human_confirmation:
                raise ValueError("consequential tools require explicit human confirmation")
            if self.idempotent and self.operation == AgentOperation.WRITE:
                # Writes may be idempotent in some APIs, but forcing an explicit choice
                # avoids accidentally labeling an unknown write behavior as safe.
                raise ValueError("write tools must explicitly declare non-default replay semantics")
        return self


class ToolRegistry:
    def __init__(self, tools: list[ToolSpec] | None = None):
        self._tools: dict[str, ToolSpec] = {}
        for tool in tools or []:
            self.register(tool)

    def register(self, tool: ToolSpec) -> None:
        existing = self._tools.get(tool.tool_id)
        if existing is not None and existing.version != tool.version:
            raise ValueError("tool id already registered with a different version")
        if existing is not None:
            raise ValueError("tool already registered")
        self._tools[tool.tool_id] = tool

    def get(self, tool_id: str) -> ToolSpec | None:
        return self._tools.get(tool_id)

    def require(self, tool_id: str) -> ToolSpec:
        tool = self.get(tool_id)
        if tool is None:
            raise KeyError(f"unknown tool: {tool_id}")
        return tool

    def manifest(self) -> list[dict]:
        return [tool.model_dump(mode="json") for tool in sorted(self._tools.values(), key=lambda item: item.tool_id)]


def synthetic_sjk_registry() -> ToolRegistry:
    """Safe synthetic-only tool catalog for the first SJK agent experiments."""

    return ToolRegistry(
        [
            ToolSpec(
                tool_id="read-clinical-context",
                version="1.0.0",
                owner="careos",
                trust_tier=ToolTrustTier.INTERNAL,
                operation=AgentOperation.READ,
                target_system="careos-truth-layer",
                data_categories={"microbiology", "medication", "tasks", "hygiene", "trends"},
                max_records_per_call=50,
                max_pages_per_call=5,
                timeout_seconds=5,
            ),
            ToolSpec(
                tool_id="prepare-handover",
                version="1.0.0",
                owner="careos",
                trust_tier=ToolTrustTier.INTERNAL,
                operation=AgentOperation.PREPARE,
                target_system="careos-draft-boundary",
                data_categories={"microbiology", "medication", "tasks", "hygiene", "trends"},
                max_records_per_call=50,
                max_pages_per_call=1,
                timeout_seconds=5,
            ),
        ]
    )
