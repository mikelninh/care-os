from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .agent_policy import AgentRequest
from .agent_runtime import AgentGateway


@dataclass(frozen=True)
class ToolResult:
    tool_id: str
    payload: Any
    external_call: bool = False


class AgentToolProxy:
    """Only execution path from an agent worker to registered CareOS tools.

    Handlers are registered by trusted application configuration. The reasoning
    worker can request a tool but never receives handler objects, source-system
    credentials, or a bypass around AgentGateway authorization.
    """

    def __init__(self, gateway: AgentGateway, handlers: dict[str, Callable[[AgentRequest], Any]]):
        self.gateway = gateway
        self.handlers = handlers

    def call(self, request: AgentRequest, *, now=None) -> ToolResult:
        decision = self.gateway.authorize(request, now=now)
        if not decision.allowed or decision.tool is None:
            raise PermissionError(decision.reason)
        handler = self.handlers.get(decision.tool.tool_id)
        if handler is None:
            self.gateway.abort("registered tool has no trusted handler")
            raise RuntimeError("registered tool has no trusted handler")
        try:
            payload = handler(request)
        except Exception as exc:
            # Once a request has been admitted, a trusted handler failure is terminal
            # for that execution. Do not leave runtime state ACTIVE after a source,
            # identity, parser or integration boundary has failed.
            self.gateway.abort(f"trusted tool handler failed: {type(exc).__name__}")
            raise
        external = bool(request.egress_host)
        self.gateway.record_tool_result(request, external_call=external)
        return ToolResult(tool_id=request.tool_id, payload=payload, external_call=external)
