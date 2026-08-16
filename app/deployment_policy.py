from __future__ import annotations

from enum import Enum
from urllib.parse import urlparse

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


def _is_loopback_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.hostname in {"localhost", "127.0.0.1", "::1"}


def _assert_clean_service_url(base_url: str) -> None:
    parsed = urlparse(base_url)
    if parsed.username or parsed.password:
        raise DeploymentBlocked("clinical source URL must not embed credentials")
    if parsed.query or parsed.fragment:
        raise DeploymentBlocked("clinical source base URL must not contain query or fragment")


def assert_fhir_source_allowed(mode: DataMode, base_url: str, *, external_deidentified_ack: bool = False) -> None:
    """Prevent FHIR adapters from bypassing the patient-data deployment gate.

    This check belongs in the adapter construction path, not only in documentation or
    the public API. Synthetic mode is local-only. De-identified evaluation may use an
    external source only after explicit acknowledgement. Live sources remain governed
    by live-readonly mode and must additionally flow through authenticated clinical
    orchestration rather than the public integration-lab endpoints.
    """

    _assert_clean_service_url(base_url)

    if mode == DataMode.SYNTHETIC:
        if not _is_loopback_url(base_url):
            raise DeploymentBlocked("synthetic mode may only use a loopback/local FHIR source")
        return

    if mode == DataMode.DEIDENTIFIED_EVALUATION:
        if _is_loopback_url(base_url):
            return
        if not external_deidentified_ack:
            raise DeploymentBlocked("external de-identified FHIR source requires explicit acknowledgement via CAREOS_EXTERNAL_DEIDENTIFIED_ACK=true")
        if not base_url.startswith("https://"):
            raise DeploymentBlocked("external de-identified FHIR source must use HTTPS")
        return

    if mode == DataMode.LIVE_READONLY:
        if not base_url.startswith("https://"):
            raise DeploymentBlocked("live FHIR source must use HTTPS")
        return

    raise DeploymentBlocked("FHIR source is not allowed in transactional mode")


def assert_public_fhir_integration_route_allowed(mode: DataMode) -> None:
    """Keep lab/demo FHIR routes from becoming an accidental live-PHI API.

    A future live-readonly deployment must use authenticated identity, treatment-context
    authorization, source-state checks and required audit through ClinicalReadCoordinator.
    The current public integration routes are deliberately never that production path.
    """

    if mode in {DataMode.SYNTHETIC, DataMode.DEIDENTIFIED_EVALUATION}:
        return
    raise DeploymentBlocked(
        "public FHIR integration routes are disabled for live patient data; use authenticated clinical orchestration"
    )
