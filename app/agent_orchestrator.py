from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .agent_delegation import VerifiedDelegation
from .agent_execution_store import InMemoryDelegationStore
from .agent_identity import RevocationSet, WorkloadIdentity
from .agent_modes import AgentOperatingMode, assert_agent_mode_allowed
from .agent_runtime import AgentExecutionState, AgentGateway
from .agent_tools import ToolRegistry


@dataclass
class ActiveAgentExecution:
    verified: VerifiedDelegation
    workload: WorkloadIdentity
    mode: AgentOperatingMode
    gateway: AgentGateway
    store: InMemoryDelegationStore

    def complete(self, *, now: datetime | None = None) -> None:
        self.gateway.complete()
        self.store.consume(self.verified.delegation_id, self.gateway.execution.execution_id, now=now)

    def abort(self, reason: str) -> None:
        self.gateway.abort(reason)
        self.store.revoke(self.verified.delegation_id)


def begin_agent_execution(
    verified: VerifiedDelegation,
    *,
    workload: WorkloadIdentity,
    registry: ToolRegistry,
    store: InMemoryDelegationStore,
    revocations: RevocationSet,
    mode: AgentOperatingMode,
    expected_workload_audience: str,
    now: datetime,
) -> ActiveAgentExecution:
    assert_agent_mode_allowed(mode)
    delegation = verified.delegation
    revocations.assert_active(workload)
    workload.validate_for(
        organisation=delegation.organisation,
        agent_id=delegation.agent_id,
        agent_version=delegation.agent_version,
        audience=expected_workload_audience,
        now=now,
    )
    execution = AgentExecutionState(started_at=now)
    store.activate_once(verified.delegation_id, execution.execution_id, now=now)
    gateway = AgentGateway(delegation=delegation, registry=registry, execution=execution)
    return ActiveAgentExecution(verified=verified, workload=workload, mode=mode, gateway=gateway, store=store)
