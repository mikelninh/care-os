from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .hospital_install import HospitalManifest, SourceSystem, build_hospital_install_plan


class UpgradeFinding(BaseModel):
    source_id: str | None = None
    severity: Literal["info", "warn", "block"]
    code: str
    message: str


class UpgradePlan(BaseModel):
    hospital_id: str
    safe_for_automatic_rollout: bool
    requires_shadow_revalidation: bool
    findings: list[UpgradeFinding]
    previous_adapter_ids: list[str]
    proposed_adapter_ids: list[str]


def _sources(manifest: HospitalManifest) -> dict[str, SourceSystem]:
    return {source.source_id: source for source in manifest.sources}


def compare_hospital_manifests(previous: HospitalManifest, proposed: HospitalManifest) -> UpgradePlan:
    if previous.hospital_id != proposed.hospital_id:
        raise ValueError("upgrade comparison requires the same hospital_id")

    findings: list[UpgradeFinding] = []
    before = _sources(previous)
    after = _sources(proposed)

    for source_id in sorted(before.keys() - after.keys()):
        findings.append(
            UpgradeFinding(
                source_id=source_id,
                severity="block",
                code="source-removed",
                message="Previously configured clinical source disappeared. Confirm intentional retirement before rollout.",
            )
        )

    for source_id in sorted(after.keys() - before.keys()):
        findings.append(
            UpgradeFinding(
                source_id=source_id,
                severity="warn",
                code="source-added",
                message="New clinical source requires conformance and shadow validation before clinicians depend on it.",
            )
        )

    for source_id in sorted(before.keys() & after.keys()):
        old = before[source_id]
        new = after[source_id]

        if (old.vendor, old.product) != (new.vendor, new.product):
            findings.append(
                UpgradeFinding(
                    source_id=source_id,
                    severity="block",
                    code="product-changed",
                    message="Vendor/product changed under the same source_id; treat this as a new integration, not an in-place patch.",
                )
            )
        elif old.version != new.version:
            findings.append(
                UpgradeFinding(
                    source_id=source_id,
                    severity="warn",
                    code="version-changed",
                    message=f"Source version changed {old.version} → {new.version}; rerun adapter conformance before rollout.",
                )
            )

        lost_interfaces = set(old.interfaces) - set(new.interfaces)
        if lost_interfaces:
            findings.append(
                UpgradeFinding(
                    source_id=source_id,
                    severity="block",
                    code="interface-lost",
                    message="Previously available interface(s) disappeared: " + ", ".join(sorted(x.value for x in lost_interfaces)),
                )
            )

        gained_interfaces = set(new.interfaces) - set(old.interfaces)
        if gained_interfaces:
            findings.append(
                UpgradeFinding(
                    source_id=source_id,
                    severity="info",
                    code="interface-added",
                    message="New interface(s) available: " + ", ".join(sorted(x.value for x in gained_interfaces)),
                )
            )

        critical_boolean_fields = {
            "patient_identity_available": "authoritative patient identity",
            "source_resource_ids_available": "source/resource provenance IDs",
            "effective_time_available": "clinical effective-time semantics",
            "lifecycle_state_available": "clinical lifecycle state",
        }
        for field_name, description in critical_boolean_fields.items():
            if getattr(old, field_name) and not getattr(new, field_name):
                findings.append(
                    UpgradeFinding(
                        source_id=source_id,
                        severity="block",
                        code=f"capability-lost:{field_name}",
                        message=f"Upgrade lost {description}; do not silently degrade the clinical contract.",
                    )
                )

        if old.source_versions_available and not new.source_versions_available:
            findings.append(
                UpgradeFinding(
                    source_id=source_id,
                    severity="warn",
                    code="resource-versioning-lost",
                    message="Source resource version identifiers are no longer available; replay/supersession evidence is weaker.",
                )
            )

        if not old.write_supported and new.write_supported:
            findings.append(
                UpgradeFinding(
                    source_id=source_id,
                    severity="block",
                    code="write-capability-added",
                    message="New write capability never becomes active through an upgrade; authorize it as a separate product/risk change.",
                )
            )

    old_plan = build_hospital_install_plan(previous)
    new_plan = build_hospital_install_plan(proposed)
    old_adapters = sorted(a.adapter_id for a in old_plan.adapters if a.direction == "read")
    new_adapters = sorted(a.adapter_id for a in new_plan.adapters if a.direction == "read")

    if old_adapters != new_adapters:
        findings.append(
            UpgradeFinding(
                severity="warn",
                code="adapter-plan-changed",
                message="Adapter selection changed; require full connector conformance and shadow comparison before rollout.",
            )
        )

    if any(check.status == "block" for check in new_plan.checks):
        findings.append(
            UpgradeFinding(
                severity="block",
                code="proposed-preflight-blocked",
                message="Proposed hospital manifest no longer passes current CareOS preflight requirements.",
            )
        )

    requires_shadow = any(f.severity in {"warn", "block"} for f in findings)
    blocked = any(f.severity == "block" for f in findings)

    return UpgradePlan(
        hospital_id=previous.hospital_id,
        safe_for_automatic_rollout=not blocked and not requires_shadow,
        requires_shadow_revalidation=requires_shadow,
        findings=findings,
        previous_adapter_ids=old_adapters,
        proposed_adapter_ids=new_adapters,
    )
