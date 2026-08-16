from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from threading import Lock


class DelegationState(str, Enum):
    UNUSED = "unused"
    ACTIVE = "active"
    CONSUMED = "consumed"
    REVOKED = "revoked"


@dataclass(frozen=True)
class DelegationRecord:
    delegation_id: str
    state: DelegationState
    execution_id: str | None = None
    updated_at: datetime | None = None


class InMemoryDelegationStore:
    """Atomic single-process replay/revocation reference implementation.

    Production must replace this with a durable, shared, strongly consistent store.
    The interface exists so replay prevention is not left to the reasoning worker.
    """

    def __init__(self):
        self._records: dict[str, DelegationRecord] = {}
        self._lock = Lock()

    def activate_once(self, delegation_id: str, execution_id: str, *, now: datetime | None = None) -> DelegationRecord:
        timestamp = now or datetime.now(timezone.utc)
        with self._lock:
            current = self._records.get(delegation_id)
            if current is not None:
                if current.state == DelegationState.REVOKED:
                    raise PermissionError("delegation revoked")
                raise PermissionError("delegation replay or duplicate activation denied")
            record = DelegationRecord(delegation_id, DelegationState.ACTIVE, execution_id, timestamp)
            self._records[delegation_id] = record
            return record

    def consume(self, delegation_id: str, execution_id: str, *, now: datetime | None = None) -> DelegationRecord:
        timestamp = now or datetime.now(timezone.utc)
        with self._lock:
            current = self._records.get(delegation_id)
            if current is None or current.state != DelegationState.ACTIVE or current.execution_id != execution_id:
                raise PermissionError("delegation is not active for this execution")
            record = DelegationRecord(delegation_id, DelegationState.CONSUMED, execution_id, timestamp)
            self._records[delegation_id] = record
            return record

    def revoke(self, delegation_id: str, *, now: datetime | None = None) -> DelegationRecord:
        timestamp = now or datetime.now(timezone.utc)
        with self._lock:
            current = self._records.get(delegation_id)
            execution_id = current.execution_id if current else None
            record = DelegationRecord(delegation_id, DelegationState.REVOKED, execution_id, timestamp)
            self._records[delegation_id] = record
            return record

    def get(self, delegation_id: str) -> DelegationRecord:
        return self._records.get(delegation_id, DelegationRecord(delegation_id, DelegationState.UNUSED))
