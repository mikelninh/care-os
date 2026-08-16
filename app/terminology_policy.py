from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

# Source: gematik app-referencevalidator-plugins ISiK5 config for
# de.gematik.isik#5.1.3, checked 2026-08-16. Keep version-pinned and update alongside
# .github/workflows/isik5-validation.yml.
ISIK_PACKAGE = "de.gematik.isik#5.1.3"
ISIK_PLUGIN_RELEASE = "isik5-1.0.4"

ISIK_IGNORED_CODE_SYSTEMS = frozenset({
    "http://loinc.org",
    "http://snomed.info/sct",
    "http://fhir.de/CodeSystem/bfarm/icd-10-gm",
    "http://fhir.de/CodeSystem/bfarm/atc",
    "http://fhir.de/CodeSystem/bfarm/ops",
    "http://dvmd.de/fhir/CodeSystem/kdl",
    "urn:iso:std:iso:11073:10101",
})

ISIK_IGNORED_VALUE_SETS = frozenset({
    "https://gematik.de/fhir/isik/ValueSet/ProzedurenCodesSCT",
    "https://gematik.de/fhir/isik/ValueSet/DiagnosesSCT",
    "https://gematik.de/fhir/isik/ValueSet/ProzedurenKategorieSCT",
    "https://gematik.de/fhir/isik/ValueSet/ISiKTerminPriority",
    "http://fhir.de/ValueSet/bfarm/ops",
    "https://gematik.de/fhir/isik/ValueSet/SctRouteOfAdministration",
    "http://dvmd.de/fhir/ValueSet/kdl",
})


class TerminologyEvidenceStatus(str, Enum):
    NOT_APPLICABLE = "not-applicable"
    REQUIRES_EXTERNAL_VALIDATION = "requires-external-validation"
    VALIDATED_EXTERNALLY = "validated-externally"


class CodingEvidence(BaseModel):
    system: str = Field(min_length=1)
    code: str = Field(min_length=1)
    value_set: str | None = None
    external_validator: str | None = None
    external_validator_version: str | None = None
    validated: bool = False

    @property
    def ignored_by_isik_reference_validator(self) -> bool:
        return self.system in ISIK_IGNORED_CODE_SYSTEMS or bool(self.value_set and self.value_set in ISIK_IGNORED_VALUE_SETS)

    @property
    def evidence_status(self) -> TerminologyEvidenceStatus:
        if not self.ignored_by_isik_reference_validator:
            # This class intentionally does not infer that ISiK profile success means
            # terminology success for arbitrary systems. It only identifies the known
            # explicit terminology gap from the pinned plugin configuration.
            return TerminologyEvidenceStatus.NOT_APPLICABLE
        if self.validated and self.external_validator and self.external_validator_version:
            return TerminologyEvidenceStatus.VALIDATED_EXTERNALLY
        return TerminologyEvidenceStatus.REQUIRES_EXTERNAL_VALIDATION

    @property
    def safe_to_claim_terminology_validated(self) -> bool:
        return self.evidence_status == TerminologyEvidenceStatus.VALIDATED_EXTERNALLY
