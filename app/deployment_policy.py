from __future__ import annotations

from enum import Enum

from .readiness_gates import GATES, GateStatus


class DataMode(str, Enum):
    SYNTHETIC = "synthetic"
    DEIDENTIFIED_EVALUATION = "deidentified-evaluation"
    LIVE_READONLY = "live-readonly"
    LIVE_TRANSACTIONAL = "live-transactional"


class DeploymentBlocked(RuntimeError):
    pass


def core_gate_blockers() -> list[str]:
    return [f"{g.id}:{g.status.value}" for g in GATES[:6] if g.status != GateStatus.PASS]


def assert_data_mode_allowed(mode: str | DataMode) -> DataMode:
    try:
        parsed = mode if isinstance(mode, DataMode) else DataMode(mode)
    except ValueError as exc:
        raise DeploymentBlocked(f"unknown CAREOS_DATA_MODE: {mode}") from exc

    if parsed in {DataMode.SYNTHETIC, DataMode.DEIDENTIFIED_EVALUATION}:
        return parsed

    if parsed == DataMode.LIVE_TRANSACTIONAL:
        raise DeploymentBlocked("live transactional/write-back mode is not supported by the current CareOS release policy")

    blockers = core_gate_blockers()
    if blockers:
        raise DeploymentBlocked("live patient data locked until G0-G5 pass: " + ", ".join(blockers))
    return parsed
