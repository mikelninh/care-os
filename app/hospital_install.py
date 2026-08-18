from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .deployment_policy import DeploymentBlocked, assert_data_mode_allowed


class SystemRole(str, Enum):
    KIS = "kis"
    LIS = "lis"
    RIS_PACS = "ris-pacs"
    DOCUMENTS = "documents"
    EPA = "epa"
    IDENTITY = "identity"
    OTHER = "other"


class InterfaceKind(str, Enum):
    ISIK_FHIR = "isik-fhir"
    FHIR_R4 = "fhir-r4"
    HL7V2 = "hl7v2"
    DOCUMENT_FEED = "document-feed"
    VENDOR_API = "vendor-api"
    UI_BRIDGE = "ui-bridge"


class DeploymentIntent(str, Enum):
    SYNTHETIC = "synthetic"
    DEIDENTIFIED = "deidentified-evaluation"
    SHADOW_READONLY = "shadow-readonly"
    COPILOT_READONLY = "copilot-readonly"
    CONTROLLED_WRITE = "controlled-write"


class SourceSystem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    role: SystemRole
    vendor: str = Field(min_length=1)
    product: str = Field(min_length=1)
    version: str = Field(min_length=1)
    interfaces: list[InterfaceKind] = Field(default_factory=list)
    authentication_mode: str = "not-configured"
    endpoint_env: str | None = None
    credential_env: str | None = None
    resources: list[str] = Field(default_factory=list)

    patient_identity_available: bool = False
    encounter_identity_available: bool = False
    source_resource_ids_available: bool = False
    source_versions_available: bool = False
    effective_time_available: bool = False
    lifecycle_state_available: bool = False
    incremental_refresh_available: bool = False

    read_supported: bool = True
    write_supported: bool = False
    ui_bridge_allowed: bool = False

    @model_validator(mode="after")
    def no_secrets_or_urls_in_manifest(self) -> "SourceSystem":
        for value, field_name in (
            (self.endpoint_env, "endpoint_env"),
            (self.credential_env, "credential_env"),
        ):
            if value and ("://" in value or "/" in value or "=" in value):
                raise ValueError(f"{field_name} must name an environment variable, not contain an endpoint or secret")
        if self.write_supported and not self.read_supported:
            raise ValueError("write-only clinical source definitions are not supported")
        return self


class HospitalManifest(BaseModel):
    """Non-secret hospital capability manifest.

    Real endpoints, certificates, tokens and passwords stay in the hospital's secret
    store. This file is safe to version and compare across sites.
    """

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1"] = "1"
    hospital_id: str = Field(min_length=1)
    country: str = Field(default="DE", min_length=2, max_length=2)
    site_name: str = Field(min_length=1)
    deployment_intent: DeploymentIntent = DeploymentIntent.SYNTHETIC
    sources: list[SourceSystem] = Field(min_length=1)

    oidc_or_sso_available: bool = False
    trusted_patient_context_launch: bool = False
    audit_destination_available: bool = False
    rollback_owner_named: bool = False
    security_owner_named: bool = False
    privacy_owner_named: bool = False
    clinical_owner_named: bool = False

    allow_ui_bridge_fallback: bool = False
    allow_any_write: bool = False

    @model_validator(mode="after")
    def controlled_write_requires_explicit_opt_in(self) -> "HospitalManifest":
        if self.deployment_intent == DeploymentIntent.CONTROLLED_WRITE and not self.allow_any_write:
            raise ValueError("controlled-write planning requires allow_any_write=true")
        return self


class AdapterSelection(BaseModel):
    source_id: str
    adapter_id: str
    adapter_family: str
    interface: InterfaceKind
    reuse_key: str
    direction: Literal["read", "write"] = "read"
    risk: Literal["green", "amber", "red"]
    rationale: str


class PreflightCheck(BaseModel):
    id: str
    status: Literal["pass", "warn", "block"]
    message: str


class HospitalInstallPlan(BaseModel):
    hospital_id: str
    deployment_intent: DeploymentIntent
    adapters: list[AdapterSelection]
    checks: list[PreflightCheck]
    execution_allowed_by_current_release: bool
    release_blocker: str | None = None
    installable_for_synthetic_or_deidentified: bool
    ready_for_shadow: bool
    ready_for_copilot: bool
    ready_for_controlled_write: bool
    next_steps: list[str]


READ_PRIORITY = (
    InterfaceKind.ISIK_FHIR,
    InterfaceKind.FHIR_R4,
    InterfaceKind.HL7V2,
    InterfaceKind.VENDOR_API,
    InterfaceKind.DOCUMENT_FEED,
)


def _adapter_id(interface: InterfaceKind) -> tuple[str, str, Literal["green", "amber", "red"]]:
    return {
        InterfaceKind.ISIK_FHIR: ("standard-isik-fhir", "fhir", "green"),
        InterfaceKind.FHIR_R4: ("standard-fhir-r4", "fhir", "green"),
        InterfaceKind.HL7V2: ("standard-hl7v2-read", "hl7v2", "green"),
        InterfaceKind.VENDOR_API: ("vendor-api-configured", "vendor-api", "amber"),
        InterfaceKind.DOCUMENT_FEED: ("standard-document-ingest", "documents", "amber"),
        InterfaceKind.UI_BRIDGE: ("controlled-ui-bridge", "computer-use", "amber"),
    }[interface]


def _select_read_adapter(source: SourceSystem) -> AdapterSelection | None:
    if not source.read_supported:
        return None
    for interface in READ_PRIORITY:
        if interface in source.interfaces:
            adapter_id, family, risk = _adapter_id(interface)
            return AdapterSelection(
                source_id=source.source_id,
                adapter_id=adapter_id,
                adapter_family=family,
                interface=interface,
                reuse_key=f"{adapter_id}:{source.vendor.lower()}:{source.product.lower()}:{source.version}",
                risk=risk,
                rationale=f"Prefer {interface.value} before vendor-specific or UI automation paths.",
            )
    return None


def _select_write_adapter(source: SourceSystem, manifest: HospitalManifest) -> AdapterSelection | None:
    if manifest.deployment_intent != DeploymentIntent.CONTROLLED_WRITE:
        return None
    if not (manifest.allow_any_write and source.write_supported):
        return None

    # Typed interfaces beat UI automation. UI bridge is a controlled last-mile fallback.
    for interface in (
        InterfaceKind.ISIK_FHIR,
        InterfaceKind.FHIR_R4,
        InterfaceKind.VENDOR_API,
        InterfaceKind.HL7V2,
        InterfaceKind.UI_BRIDGE,
    ):
        if interface not in source.interfaces:
            continue
        if interface == InterfaceKind.UI_BRIDGE and not (
            manifest.allow_ui_bridge_fallback and source.ui_bridge_allowed
        ):
            continue
        adapter_id, family, risk = _adapter_id(interface)
        return AdapterSelection(
            source_id=source.source_id,
            adapter_id=f"{adapter_id}-write",
            adapter_family=family,
            interface=interface,
            reuse_key=f"{adapter_id}:write:{source.vendor.lower()}:{source.product.lower()}:{source.version}",
            direction="write",
            risk="amber" if risk == "green" else risk,
            rationale="Write path remains separate, explicit, human-approved and independently testable.",
        )
    return None


def _current_release_allows(intent: DeploymentIntent) -> tuple[bool, str | None]:
    mapping = {
        DeploymentIntent.SYNTHETIC: "synthetic",
        DeploymentIntent.DEIDENTIFIED: "deidentified-evaluation",
        DeploymentIntent.SHADOW_READONLY: "live-readonly",
        DeploymentIntent.COPILOT_READONLY: "live-readonly",
        DeploymentIntent.CONTROLLED_WRITE: "live-transactional",
    }
    try:
        assert_data_mode_allowed(mapping[intent])
        return True, None
    except DeploymentBlocked as exc:
        return False, str(exc)


def build_hospital_install_plan(manifest: HospitalManifest) -> HospitalInstallPlan:
    adapters: list[AdapterSelection] = []
    checks: list[PreflightCheck] = []

    for source in manifest.sources:
        selection = _select_read_adapter(source)
        if selection:
            adapters.append(selection)
        else:
            checks.append(
                PreflightCheck(
                    id=f"source:{source.source_id}:read-path",
                    status="block",
                    message="No supported read interface. Do not invent an integration; discover a governed source path.",
                )
            )

        write_selection = _select_write_adapter(source, manifest)
        if write_selection:
            adapters.append(write_selection)

        checks.extend(
            [
                PreflightCheck(
                    id=f"source:{source.source_id}:patient-identity",
                    status="pass" if source.patient_identity_available else "block",
                    message="Authoritative patient identity must survive the adapter boundary.",
                ),
                PreflightCheck(
                    id=f"source:{source.source_id}:source-id",
                    status="pass" if source.source_resource_ids_available else "warn",
                    message="Source/resource identifiers should be preserved for provenance and replay.",
                ),
                PreflightCheck(
                    id=f"source:{source.source_id}:lifecycle",
                    status="pass" if source.lifecycle_state_available else "warn",
                    message="Pending/final/corrected/cancelled semantics should remain explicit where the source exposes them.",
                ),
            ]
        )

    global_checks = (
        ("identity:sso", manifest.oidc_or_sso_available, "Hospital identity/SSO path identified."),
        ("identity:patient-context", manifest.trusted_patient_context_launch, "Trusted same-patient launch/context path identified."),
        ("ops:audit", manifest.audit_destination_available, "Audit destination identified."),
        ("ops:rollback-owner", manifest.rollback_owner_named, "Rollback owner named."),
        ("governance:security-owner", manifest.security_owner_named, "Security owner named."),
        ("governance:privacy-owner", manifest.privacy_owner_named, "Privacy/DPO owner named."),
        ("governance:clinical-owner", manifest.clinical_owner_named, "Clinical owner named."),
    )
    for check_id, ok, message in global_checks:
        checks.append(PreflightCheck(id=check_id, status="pass" if ok else "block", message=message))

    blocking = [check for check in checks if check.status == "block"]
    execution_allowed, release_blocker = _current_release_allows(manifest.deployment_intent)

    standard_read_count = sum(
        1
        for adapter in adapters
        if adapter.direction == "read" and adapter.interface in {InterfaceKind.ISIK_FHIR, InterfaceKind.FHIR_R4, InterfaceKind.HL7V2}
    )
    all_sources_have_read = all(_select_read_adapter(source) is not None for source in manifest.sources)
    base_ready = not blocking and all_sources_have_read and bool(adapters)
    shadow_ready = base_ready and standard_read_count > 0
    copilot_ready = shadow_ready and manifest.trusted_patient_context_launch and manifest.audit_destination_available
    controlled_write_ready = (
        copilot_ready
        and manifest.allow_any_write
        and any(adapter.direction == "write" for adapter in adapters)
    )

    next_steps: list[str] = []
    for check in blocking:
        next_steps.append(f"Resolve {check.id}: {check.message}")
    if not execution_allowed and release_blocker:
        next_steps.append(f"Current CareOS release remains locked: {release_blocker}")
    if base_ready and manifest.deployment_intent in {DeploymentIntent.SYNTHETIC, DeploymentIntent.DEIDENTIFIED}:
        next_steps.append("Run connector conformance suite and start synthetic/deidentified shadow evaluation.")
    if shadow_ready and manifest.deployment_intent in {DeploymentIntent.SHADOW_READONLY, DeploymentIntent.COPILOT_READONLY}:
        next_steps.append("After external gates permit, run read-only shadow mode before clinician dependency.")
    if controlled_write_ready:
        next_steps.append("Write path still requires per-workflow approval, read-after-write verification and rollback rehearsal.")

    return HospitalInstallPlan(
        hospital_id=manifest.hospital_id,
        deployment_intent=manifest.deployment_intent,
        adapters=adapters,
        checks=checks,
        execution_allowed_by_current_release=execution_allowed,
        release_blocker=release_blocker,
        installable_for_synthetic_or_deidentified=(base_ready and manifest.deployment_intent in {DeploymentIntent.SYNTHETIC, DeploymentIntent.DEIDENTIFIED}),
        ready_for_shadow=shadow_ready,
        ready_for_copilot=copilot_ready,
        ready_for_controlled_write=controlled_write_ready,
        next_steps=next_steps,
    )
