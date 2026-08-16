from __future__ import annotations

from datetime import datetime, timezone
from pydantic import BaseModel, Field


class WorkloadIdentity(BaseModel):
    subject: str = Field(min_length=1)
    organisation: str = Field(min_length=1)
    agent_id: str = Field(min_length=1)
    agent_version: str = Field(min_length=1)
    audience: str = Field(min_length=1)
    issued_at: datetime
    expires_at: datetime
    credential_id: str = Field(min_length=1)

    def validate_for(self, *, organisation: str, agent_id: str, agent_version: str, audience: str, now: datetime | None = None) -> None:
        current = now or datetime.now(timezone.utc)
        if current < self.issued_at or current >= self.expires_at:
            raise PermissionError("workload identity is outside validity window")
        if self.organisation != organisation:
            raise PermissionError("workload identity organisation mismatch")
        if self.agent_id != agent_id or self.agent_version != agent_version:
            raise PermissionError("workload identity agent/version mismatch")
        if self.audience != audience:
            raise PermissionError("workload identity audience mismatch")


class RevocationSet:
    """Reference revocation contract; production source must be provider-controlled/durable."""

    def __init__(self):
        self._revoked: set[str] = set()

    def revoke(self, credential_id: str) -> None:
        self._revoked.add(credential_id)

    def assert_active(self, identity: WorkloadIdentity) -> None:
        if identity.credential_id in self._revoked:
            raise PermissionError("workload identity credential revoked")
