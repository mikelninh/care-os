from __future__ import annotations

import json
from datetime import date
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .hospital_install import ADAPTER_CATALOG, HospitalManifest
from .hospital_upgrade import UpgradePlan


class EvidenceClass(str, Enum):
    SYNTHETIC_ONLY = "synthetic-only"
    REAL_SANDBOX = "real-sandbox"
    REAL_SHADOW = "real-shadow"
    PRODUCTION_OBSERVED = "production-observed"


class VersionMatchPolicy(str, Enum):
    EXACT = "exact"
    EXPLICIT_ALLOWLIST = "explicit-allowlist"


class CompatibilityRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record_id: str = Field(min_length=1)
    adapter_id: str = Field(min_length=1)
    vendor: str = Field(min_length=1)
    product: str = Field(min_length=1)
    tested_version: str = Field(min_length=1)
    version_match_policy: VersionMatchPolicy = VersionMatchPolicy.EXACT
    compatible_versions: tuple[str, ...] = ()
    interface_profile: str = Field(min_length=1)
    supported_resources: tuple[str, ...] = ()
    authentication_pattern: str = Field(min_length=1)
    patient_identity_behavior: str = Field(min_length=1)
    encounter_identity_behavior: str = Field(min_length=1)
    paging_behavior: str = Field(min_length=1)
    versioning_behavior: str = Field(min_length=1)
    lifecycle_behavior: str = Field(min_length=1)
    known_deviations: tuple[str, ...] = ()
    conformance_suite_version: str = Field(min_length=1)
    conformance_result: str = Field(min_length=1)
    evidence_class: EvidenceClass
    tested_on: date
    known_upgrade_regressions: tuple[str, ...] = ()
    synthetic_only: bool

    @model_validator(mode="after")
    def evidence_label_must_be_honest(self) -> "CompatibilityRecord":
        if self.evidence_class == EvidenceClass.SYNTHETIC_ONLY and not self.synthetic_only:
            raise ValueError("synthetic-only evidence class must set synthetic_only=true")
        if self.evidence_class != EvidenceClass.SYNTHETIC_ONLY and self.synthetic_only:
            raise ValueError("real evidence class cannot be labelled synthetic_only=true")
        if self.version_match_policy == VersionMatchPolicy.EXPLICIT_ALLOWLIST and not self.compatible_versions:
            raise ValueError("explicit-allowlist policy requires compatible_versions")
        return self

    def matches(self, *, adapter_id: str, vendor: str, product: str, version: str) -> bool:
        if (self.adapter_id, self.vendor.casefold(), self.product.casefold()) != (
            adapter_id,
            vendor.casefold(),
            product.casefold(),
        ):
            return False
        if self.version_match_policy == VersionMatchPolicy.EXACT:
            return version == self.tested_version
        return version == self.tested_version or version in self.compatible_versions


class CompatibilityLookup(BaseModel):
    source_id: str
    adapter_id: str
    vendor: str
    product: str
    version: str
    matches: tuple[CompatibilityRecord, ...]
    exact_real_evidence: bool
    may_auto_approve_rollout: bool = False


class CompatibilityRegistry:
    def __init__(self, records: list[CompatibilityRecord]):
        ids = [record.record_id for record in records]
        if len(ids) != len(set(ids)):
            raise ValueError("compatibility registry contains duplicate record_id values")
        self.records = tuple(records)

    @classmethod
    def from_directory(cls, directory: str | Path) -> "CompatibilityRegistry":
        path = Path(directory)
        records = [
            CompatibilityRecord.model_validate(json.loads(file.read_text(encoding="utf-8")))
            for file in sorted(path.glob("*.json"))
        ]
        return cls(records)

    def lookup(self, *, source_id: str, adapter_id: str, vendor: str, product: str, version: str) -> CompatibilityLookup:
        matches = tuple(
            record
            for record in self.records
            if record.matches(adapter_id=adapter_id, vendor=vendor, product=product, version=version)
        )
        exact_real = any(
            record.tested_version == version and record.evidence_class != EvidenceClass.SYNTHETIC_ONLY
            for record in matches
        )
        return CompatibilityLookup(
            source_id=source_id,
            adapter_id=adapter_id,
            vendor=vendor,
            product=product,
            version=version,
            matches=matches,
            exact_real_evidence=exact_real,
            may_auto_approve_rollout=False,
        )


def validate_registry_against_adapter_catalog(registry: CompatibilityRegistry) -> None:
    known_ids = {str(item["adapter_id"]) for item in ADAPTER_CATALOG.values()}
    unknown = sorted({record.adapter_id for record in registry.records} - known_ids)
    if unknown:
        raise ValueError("compatibility records reference unknown adapter IDs: " + ", ".join(unknown))


def assess_upgrade_compatibility(
    upgrade: UpgradePlan,
    proposed: HospitalManifest,
    registry: CompatibilityRegistry,
) -> list[CompatibilityLookup]:
    """Attach reusable compatibility evidence to an upgrade without approving it.

    Compatibility evidence may reduce repeated investigation. It never overrides an
    UpgradePlan blocker and never auto-promotes a release.
    """

    plan_adapter_by_source = {}
    from .hospital_install import build_hospital_install_plan

    for selection in build_hospital_install_plan(proposed).adapters:
        if selection.direction == "read":
            plan_adapter_by_source[selection.source_id] = selection.adapter_id

    lookups = []
    for source in proposed.sources:
        adapter_id = plan_adapter_by_source.get(source.source_id)
        if not adapter_id:
            continue
        lookups.append(
            registry.lookup(
                source_id=source.source_id,
                adapter_id=adapter_id,
                vendor=source.vendor,
                product=source.product,
                version=source.version,
            )
        )
    return lookups
