from __future__ import annotations

import json
import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .hospital_install import HospitalInstallPlan, HospitalManifest, build_hospital_install_plan


SECRET_PATTERN = re.compile(
    r"(?i)(bearer\s+[a-z0-9._~+/-]{12,}|password\s*[:=]|secret\s*[:=]|token\s*[:=]\s*[a-z0-9._~+/-]{8,}|-----BEGIN [A-Z ]+PRIVATE KEY-----)"
)


class ReviewSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str
    role: str
    vendor: str
    product: str
    version: str
    adapter_id: str | None
    adapter_status: str | None
    interface: str | None
    direction: str = "read"
    authentication_mode: str
    endpoint_reference: str | None
    credential_reference: str | None
    resources: tuple[str, ...]
    patient_identity_available: bool
    encounter_identity_available: bool
    lifecycle_state_available: bool
    source_versions_available: bool


class HospitalReviewPack(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hospital_id: str
    site_name: str
    country: str
    deployment_intent: str
    patient_identity_strategy: str
    sources: tuple[ReviewSource, ...]
    owners: dict[str, bool]
    controls: dict[str, bool]
    preflight: tuple[dict[str, str], ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    markdown: str
    mermaid: str
    legal_approval_claim: bool = False

    @model_validator(mode="after")
    def no_secret_material_or_approval_claim(self) -> "HospitalReviewPack":
        blob = self.model_dump_json()
        if SECRET_PATTERN.search(blob):
            raise ValueError("review pack contains material resembling a secret")
        if self.legal_approval_claim:
            raise ValueError("generated review pack is support evidence, not DSFA/DPIA/security approval")
        return self


def _source_rows(manifest: HospitalManifest, plan: HospitalInstallPlan) -> tuple[ReviewSource, ...]:
    selections = {item.source_id: item for item in plan.adapters if item.direction == "read"}
    rows = []
    for source in manifest.sources:
        selected = selections.get(source.source_id)
        rows.append(
            ReviewSource(
                source_id=source.source_id,
                role=source.role.value,
                vendor=source.vendor,
                product=source.product,
                version=source.version,
                adapter_id=selected.adapter_id if selected else None,
                adapter_status=selected.implementation_status if selected else None,
                interface=selected.interface.value if selected else None,
                authentication_mode=source.authentication_mode,
                endpoint_reference=source.endpoint_env,
                credential_reference=source.credential_env,
                resources=tuple(source.resources),
                patient_identity_available=source.patient_identity_available,
                encounter_identity_available=source.encounter_identity_available,
                lifecycle_state_available=source.lifecycle_state_available,
                source_versions_available=source.source_versions_available,
            )
        )
    return tuple(rows)


def _mermaid(sources: tuple[ReviewSource, ...]) -> str:
    lines = ["flowchart LR"]
    for index, source in enumerate(sources):
        safe_label = f"{source.source_id}\\n{source.role}\\n{source.interface or 'no-adapter'}"
        lines.append(f'  S{index}["{safe_label}"] --> D["CareOS provider-local data plane"]')
    lines.extend(
        [
            '  D --> C["source-linked clinical context"]',
            '  C --> U["authorized clinician / bounded application"]',
            '  D --> A["provider audit destination"]',
        ]
    )
    return "\n".join(lines)


def _markdown(
    manifest: HospitalManifest,
    sources: tuple[ReviewSource, ...],
    plan: HospitalInstallPlan,
    blockers: tuple[str, ...],
    warnings: tuple[str, ...],
) -> str:
    lines = [
        f"# CareOS hospital review pack — {manifest.site_name}",
        "",
        "> Generated from non-secret capability configuration. This is a technical review/support artifact, not DSFA/DPIA, security, regulatory or clinical approval.",
        "",
        f"- Hospital ID: `{manifest.hospital_id}`",
        f"- Country: `{manifest.country}`",
        f"- Deployment intent: `{manifest.deployment_intent.value}`",
        f"- Patient identity strategy: `{manifest.patient_identity_strategy.value}`",
        "",
        "## Source/interface inventory",
        "",
        "| Source | Role | Vendor/product/version | Interface/adapter | Auth | Endpoint ref | Direction |",
        "|---|---|---|---|---|---|---|",
    ]
    for source in sources:
        lines.append(
            f"| `{source.source_id}` | {source.role} | {source.vendor} / {source.product} / {source.version} | "
            f"{source.interface or 'none'} / {source.adapter_id or 'none'} ({source.adapter_status or 'n/a'}) | "
            f"{source.authentication_mode} | `{source.endpoint_reference or 'not-configured'}` | read |"
        )
    lines.extend(["", "## Read/write boundary", "", "- Read paths are listed above."])
    if manifest.allow_any_write:
        lines.append("- Manifest permits planning for controlled write capability; current release policy and workflow approval gates still apply.")
    else:
        lines.append("- Manifest does not permit write capability.")
    lines.extend(
        [
            "",
            "## Accountable owner lanes",
            "",
            f"- Security owner named: **{manifest.security_owner_named}**",
            f"- Privacy/Datenschutz owner named: **{manifest.privacy_owner_named}**",
            f"- Clinical owner named: **{manifest.clinical_owner_named}**",
            f"- Rollback owner named: **{manifest.rollback_owner_named}**",
            "",
            "## Controls declared by the site",
            "",
            f"- SSO/OIDC available: **{manifest.oidc_or_sso_available}**",
            f"- Trusted patient-context launch: **{manifest.trusted_patient_context_launch}**",
            f"- Audit destination available: **{manifest.audit_destination_available}**",
            "",
            "## Preflight blockers",
            "",
        ]
    )
    lines.extend([f"- {item}" for item in blockers] or ["- none in this non-secret planning pass"])
    lines.extend(["", "## Preflight warnings", ""])
    lines.extend([f"- {item}" for item in warnings] or ["- none"])
    lines.extend(
        [
            "",
            "## Network/data-flow diagram",
            "",
            "```mermaid",
            _mermaid(sources),
            "```",
            "",
            "## Boundary",
            "",
            "Real endpoint values, credentials, certificates, patient data and secret material are intentionally absent. The review pack supports hospital IT/security/privacy discovery; accountable reviewers remain responsible for approvals.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_hospital_review_pack(manifest: HospitalManifest) -> HospitalReviewPack:
    plan = build_hospital_install_plan(manifest)
    sources = _source_rows(manifest, plan)
    blockers = tuple(check.message for check in plan.checks if check.status == "block")
    warnings = tuple(check.message for check in plan.checks if check.status == "warn")
    preflight = tuple({"id": check.id, "status": check.status, "message": check.message} for check in plan.checks)
    pack = HospitalReviewPack(
        hospital_id=manifest.hospital_id,
        site_name=manifest.site_name,
        country=manifest.country,
        deployment_intent=manifest.deployment_intent.value,
        patient_identity_strategy=manifest.patient_identity_strategy.value,
        sources=sources,
        owners={
            "security": manifest.security_owner_named,
            "privacy": manifest.privacy_owner_named,
            "clinical": manifest.clinical_owner_named,
            "rollback": manifest.rollback_owner_named,
        },
        controls={
            "oidc_or_sso_available": manifest.oidc_or_sso_available,
            "trusted_patient_context_launch": manifest.trusted_patient_context_launch,
            "audit_destination_available": manifest.audit_destination_available,
            "allow_any_write": manifest.allow_any_write,
        },
        preflight=preflight,
        blockers=blockers,
        warnings=warnings,
        markdown="",
        mermaid=_mermaid(sources),
    )
    return pack.model_copy(update={"markdown": _markdown(manifest, sources, plan, blockers, warnings)})


def review_pack_json(pack: HospitalReviewPack) -> str:
    payload: dict[str, Any] = pack.model_dump(mode="json")
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
