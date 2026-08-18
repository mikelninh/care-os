from __future__ import annotations

from pydantic import BaseModel, Field


class ResourceCapability(BaseModel):
    resource_type: str
    interactions: list[str] = Field(default_factory=list)
    versioning: str | None = None
    search_params: list[str] = Field(default_factory=list)


class FhirCapabilityDiscovery(BaseModel):
    fhir_version: str | None = None
    software_name: str | None = None
    software_version: str | None = None
    formats: list[str] = Field(default_factory=list)
    resources: list[ResourceCapability] = Field(default_factory=list)

    @property
    def resource_types(self) -> list[str]:
        return sorted({resource.resource_type for resource in self.resources})

    @property
    def supports_patient_read(self) -> bool:
        return any(
            resource.resource_type == "Patient" and "read" in resource.interactions
            for resource in self.resources
        )

    @property
    def versioned_resource_types(self) -> list[str]:
        return sorted(
            resource.resource_type
            for resource in self.resources
            if resource.versioning in {"versioned", "versioned-update"}
        )


def parse_capability_statement(statement: dict) -> FhirCapabilityDiscovery:
    if statement.get("resourceType") != "CapabilityStatement":
        raise ValueError("FHIR discovery requires a CapabilityStatement")

    resources: list[ResourceCapability] = []
    for rest in statement.get("rest", []):
        if not isinstance(rest, dict):
            continue
        for resource in rest.get("resource", []):
            if not isinstance(resource, dict) or not resource.get("type"):
                continue
            interactions = [
                str(item.get("code"))
                for item in resource.get("interaction", [])
                if isinstance(item, dict) and item.get("code")
            ]
            search_params = [
                str(item.get("name"))
                for item in resource.get("searchParam", [])
                if isinstance(item, dict) and item.get("name")
            ]
            resources.append(
                ResourceCapability(
                    resource_type=str(resource["type"]),
                    interactions=sorted(set(interactions)),
                    versioning=(str(resource["versioning"]) if resource.get("versioning") else None),
                    search_params=sorted(set(search_params)),
                )
            )

    software = statement.get("software") if isinstance(statement.get("software"), dict) else {}
    return FhirCapabilityDiscovery(
        fhir_version=(str(statement["fhirVersion"]) if statement.get("fhirVersion") else None),
        software_name=(str(software["name"]) if software.get("name") else None),
        software_version=(str(software["version"]) if software.get("version") else None),
        formats=sorted(str(value) for value in statement.get("format", []) if value),
        resources=resources,
    )


class ManifestCapabilityComparison(BaseModel):
    source_id: str
    discovered_resource_types: list[str]
    declared_resource_types: list[str]
    undeclared_but_discovered: list[str]
    declared_but_not_advertised: list[str]
    patient_read_advertised: bool
    versioned_resource_types: list[str]
    notes: list[str] = Field(default_factory=list)


def compare_manifest_resources(source_id: str, declared: list[str], discovery: FhirCapabilityDiscovery) -> ManifestCapabilityComparison:
    declared_set = set(declared)
    discovered_set = set(discovery.resource_types)
    notes: list[str] = []
    if not discovery.supports_patient_read:
        notes.append("CapabilityStatement does not advertise Patient read; patient-scoped connector assumptions require review.")
    if not discovery.fhir_version:
        notes.append("FHIR version was not advertised.")
    return ManifestCapabilityComparison(
        source_id=source_id,
        discovered_resource_types=sorted(discovered_set),
        declared_resource_types=sorted(declared_set),
        undeclared_but_discovered=sorted(discovered_set - declared_set),
        declared_but_not_advertised=sorted(declared_set - discovered_set),
        patient_read_advertised=discovery.supports_patient_read,
        versioned_resource_types=discovery.versioned_resource_types,
        notes=notes,
    )
