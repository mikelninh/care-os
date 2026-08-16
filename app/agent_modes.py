from __future__ import annotations

from enum import Enum

from .agent_readiness import agent_gate_manifest
from .readiness_gates import gate_manifest


class AgentOperatingMode(str, Enum):
    SYNTHETIC = "synthetic"
    DEIDENTIFIED_SANDBOX = "deidentified-sandbox"
    SHADOW_LIVE = "shadow-live"
    READ_ONLY_LIVE = "read-only-live"
    CONSEQUENTIAL = "consequential"


def _core_ready() -> bool:
    gates = gate_manifest()["gates"]
    required = {"G0", "G1", "G2", "G3", "G4", "G5"}
    return all(g["status"] == "PASS" for g in gates if g["id"] in required) and required.issubset({g["id"] for g in gates})


def _agents_ready() -> bool:
    return agent_gate_manifest()["all_agent_gates_pass"]


def assert_agent_mode_allowed(mode: AgentOperatingMode) -> AgentOperatingMode:
    if mode in {AgentOperatingMode.SYNTHETIC, AgentOperatingMode.DEIDENTIFIED_SANDBOX}:
        return mode
    if mode in {AgentOperatingMode.SHADOW_LIVE, AgentOperatingMode.READ_ONLY_LIVE}:
        if not _core_ready() or not _agents_ready():
            raise RuntimeError("live agent mode locked until G0-G5 and A0-A9 all PASS")
        return mode
    raise RuntimeError("consequential agent mode is unsupported by current CareOS release policy")
