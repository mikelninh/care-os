from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SafetyControls:
    """Runtime pilot controls independent of the underlying clinical source systems."""

    patient_reads_enabled: bool = True
    disabled_connectors: frozenset[str] = field(default_factory=frozenset)
    prepared_outputs_enabled: bool = False
    reason: str = ""

    def read_allowed(self, connector_id: str) -> tuple[bool, str]:
        if not self.patient_reads_enabled:
            return False, self.reason or "CareOS patient reads disabled by runtime safety control"
        if connector_id in self.disabled_connectors:
            return False, self.reason or f"connector {connector_id} disabled by runtime safety control"
        return True, "enabled"

    def output_allowed(self) -> tuple[bool, str]:
        if not self.prepared_outputs_enabled:
            return False, self.reason or "prepared outputs disabled by runtime safety control"
        return True, "enabled"
