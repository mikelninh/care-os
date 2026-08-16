from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

import httpx

from .clinical_truth import ClinicalFact, SourceKind, SourceRef, TruthEnvelope
from .deployment_policy import DataMode, assert_data_mode_allowed, assert_fhir_source_allowed

FHIR_ID_PATTERN = re.compile(r"^[A-Za-z0-9\-.]{1,64}$")


@dataclass
class FhirConfig:
    base_url: str = os.getenv("FHIR_BASE_URL", "http://localhost:8080/fhir")
    timeout_seconds: float = float(os.getenv("FHIR_TIMEOUT_SECONDS", "8"))
    max_pages: int = int(os.getenv("FHIR_MAX_PAGES", "50"))


class FhirUnavailable(RuntimeError):
    pass


def _env_true(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _validate_fhir_id(value: str) -> str:
    if not FHIR_ID_PATTERN.fullmatch(value or ""):
        raise FhirUnavailable("invalid FHIR id")
    return value


def _reference_targets_patient(reference: str | None, patient_id: str) -> bool:
    if not reference:
        return False
    parsed = urlparse(reference)
    path = parsed.path if parsed.scheme or parsed.netloc else reference.split("?", 1)[0].split("#", 1)[0]
    normalized = path.strip("/")
    return normalized == f"Patient/{patient_id}" or normalized.endswith(f"/Patient/{patient_id}")


def _assert_resource_patient_scope(resource: dict[str, Any], patient_id: str) -> None:
    resource_type = resource.get("resourceType")
    reference_field = {
        "AllergyIntolerance": "patient",
        "Condition": "subject",
        "Observation": "subject",
        "MedicationStatement": "subject",
        "Task": "for",
        "DocumentReference": "subject",
    }.get(resource_type)
    if not reference_field:
        raise FhirUnavailable(f"unexpected resource type in patient snapshot: {resource_type}")
    reference = (resource.get(reference_field) or {}).get("reference")
    if not _reference_targets_patient(reference, patient_id):
        raise FhirUnavailable(f"FHIR {resource_type} patient reference mismatch")


class FhirClient:
    """FHIR R4 read adapter with fail-visible bounded pagination and patient binding.

    Standard REST/search transport only. ISiK-specific profiles, production auth and
    terminology validation remain separate gates and are not implied by this adapter.
    The adapter itself enforces the current CareOS data-mode/source policy so callers
    cannot silently bypass deployment restrictions.
    """

    def __init__(
        self,
        config: FhirConfig | None = None,
        transport: httpx.BaseTransport | None = None,
        *,
        data_mode: DataMode | str | None = None,
        external_deidentified_ack: bool | None = None,
    ):
        self.config = config or FhirConfig()
        if self.config.max_pages < 1 or self.config.max_pages > 1000:
            raise ValueError("FHIR max_pages must be between 1 and 1000")
        if self.config.timeout_seconds <= 0 or self.config.timeout_seconds > 60:
            raise ValueError("FHIR timeout_seconds must be >0 and <=60")
        mode = assert_data_mode_allowed(data_mode or os.getenv("CAREOS_DATA_MODE", "synthetic"))
        acknowledgement = (
            _env_true(os.getenv("CAREOS_EXTERNAL_DEIDENTIFIED_ACK"))
            if external_deidentified_ack is None
            else external_deidentified_ack
        )
        assert_fhir_source_allowed(mode, self.config.base_url, external_deidentified_ack=acknowledgement)
        self.data_mode = mode
        self._client = httpx.Client(
            base_url=self.config.base_url.rstrip("/"),
            timeout=self.config.timeout_seconds,
            headers={"Accept": "application/fhir+json"},
            transport=transport,
            follow_redirects=False,
        )

    def _decode_response(self, response: httpx.Response) -> dict[str, Any]:
        try:
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                raise ValueError("FHIR response must be a JSON object")
            return data
        except (httpx.HTTPError, ValueError) as exc:
            raise FhirUnavailable(str(exc)) from exc

    def _get(self, path: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        try:
            return self._decode_response(self._client.get(path, params=params))
        except httpx.HTTPError as exc:
            raise FhirUnavailable(str(exc)) from exc

    def _validate_next_url(self, url: str) -> str:
        """Reject cross-origin pagination links instead of turning a FHIR server into SSRF."""
        base = urlparse(self.config.base_url)
        candidate = urlparse(url)
        if not candidate.scheme or not candidate.netloc:
            raise FhirUnavailable("FHIR next link must be an absolute same-origin URL")
        if candidate.username or candidate.password:
            raise FhirUnavailable("FHIR next link must not embed credentials")
        base_port = base.port or (443 if base.scheme == "https" else 80)
        candidate_port = candidate.port or (443 if candidate.scheme == "https" else 80)
        if (candidate.scheme, candidate.hostname, candidate_port) != (base.scheme, base.hostname, base_port):
            raise FhirUnavailable("FHIR next link changed origin")
        base_path = base.path.rstrip("/")
        if base_path and not (candidate.path == base_path or candidate.path.startswith(base_path + "/")):
            raise FhirUnavailable("FHIR next link escaped configured base path")
        return url

    def _get_absolute(self, url: str) -> dict[str, Any]:
        safe_url = self._validate_next_url(url)
        try:
            return self._decode_response(self._client.get(safe_url))
        except httpx.HTTPError as exc:
            raise FhirUnavailable(str(exc)) from exc

    @staticmethod
    def _next_link(bundle: dict[str, Any]) -> str | None:
        for link in bundle.get("link") or []:
            if link.get("relation") == "next" and link.get("url"):
                return str(link["url"])
        return None

    @staticmethod
    def _bundle_resources(bundle: dict[str, Any]) -> list[dict[str, Any]]:
        if bundle.get("resourceType") != "Bundle":
            raise FhirUnavailable("FHIR search response was not a Bundle")
        resources: list[dict[str, Any]] = []
        for entry in bundle.get("entry", []) or []:
            resource = entry.get("resource") if isinstance(entry, dict) else None
            if resource is not None:
                if not isinstance(resource, dict):
                    raise FhirUnavailable("FHIR Bundle contained a non-object resource")
                resources.append(resource)
        return resources

    def capability(self) -> dict[str, Any]:
        return self._get("/metadata")

    def patient(self, patient_id: str) -> dict[str, Any]:
        safe_id = _validate_fhir_id(patient_id)
        patient = self._get(f"/Patient/{safe_id}")
        if patient.get("resourceType") != "Patient" or patient.get("id") != safe_id:
            raise FhirUnavailable("FHIR Patient identity mismatch")
        return patient

    def search(self, resource: str, **params: str) -> list[dict[str, Any]]:
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]{0,63}", resource or ""):
            raise FhirUnavailable("invalid FHIR resource type")
        bundle = self._get(f"/{resource}", params=params)
        resources = self._bundle_resources(bundle)
        next_url = self._next_link(bundle)
        seen: set[str] = set()
        pages = 1

        while next_url:
            if pages >= self.config.max_pages:
                raise FhirUnavailable("FHIR pagination exceeded configured max_pages; partial results rejected")
            safe_url = self._validate_next_url(next_url)
            if safe_url in seen:
                raise FhirUnavailable("FHIR pagination loop detected; partial results rejected")
            seen.add(safe_url)
            bundle = self._get_absolute(safe_url)
            resources.extend(self._bundle_resources(bundle))
            next_url = self._next_link(bundle)
            pages += 1

        return resources

    def patient_snapshot(self, patient_id: str) -> dict[str, Any]:
        safe_id = _validate_fhir_id(patient_id)
        patient = self.patient(safe_id)
        allergies = self.search("AllergyIntolerance", patient=safe_id)
        conditions = self.search("Condition", patient=safe_id)
        observations = self.search("Observation", patient=safe_id, _sort="-date")
        medications = self.search("MedicationStatement", patient=safe_id, status="active")
        tasks = self.search("Task", patient=safe_id)
        documents = self.search("DocumentReference", patient=safe_id)
        for resource in [*allergies, *conditions, *observations, *medications, *tasks, *documents]:
            _assert_resource_patient_scope(resource, safe_id)
        return {
            "patient": patient,
            "allergies": allergies,
            "conditions": conditions,
            "observations": observations,
            "medications": medications,
            "tasks": tasks,
            "documents": documents,
        }


def _display_name(patient: dict[str, Any]) -> str:
    names = patient.get("name") or []
    if not names:
        return patient.get("id", "Patient")
    n = names[0]
    return " ".join([*(n.get("given") or []), n.get("family", "")]).strip()


def _concept_text(cc: dict[str, Any] | None) -> str:
    if not cc:
        return "Unbenannt"
    if cc.get("text"):
        return cc["text"]
    codings = cc.get("coding") or []
    return next((c.get("display") for c in codings if c.get("display")), "Unbenannt")


def _coding(cc: dict[str, Any] | None) -> tuple[str | None, str | None]:
    codings = (cc or {}).get("coding") or []
    if not codings:
        return None, None
    c = codings[0]
    return c.get("code"), c.get("system")


def _source(resource: dict[str, Any]) -> SourceRef:
    return SourceRef(
        kind=SourceKind.FHIR,
        system="FHIR",
        resource_type=resource.get("resourceType"),
        resource_id=resource.get("id"),
        resource_version=(resource.get("meta") or {}).get("versionId"),
    )


def _fact_id(resource: dict[str, Any], suffix: str = "") -> str:
    base = f"{resource.get('resourceType','Resource')}:{resource.get('id','missing')}"
    return f"{base}:{suffix}" if suffix else base


def snapshot_to_truth(snapshot: dict[str, Any]) -> TruthEnvelope:
    """Convert source-native FHIR resources into the canonical CareOS fact contract."""
    patient_id = snapshot["patient"].get("id")
    if not patient_id:
        raise ValueError("FHIR Patient requires id before CareOS truth ingestion")
    facts: list[ClinicalFact] = []

    for r in snapshot.get("allergies", []):
        code, system = _coding(r.get("code"))
        facts.append(ClinicalFact(fact_id=_fact_id(r), patient_ref=patient_id, fact_type="allergy", value_original=_concept_text(r.get("code")), code=code, code_system=system, effective_time=r.get("recordedDate"), recorded_time=r.get("recordedDate"), source=_source(r), transformer="fhir-source-native", transformer_version="1"))

    for r in snapshot.get("conditions", []):
        code, system = _coding(r.get("code"))
        facts.append(ClinicalFact(fact_id=_fact_id(r), patient_ref=patient_id, fact_type="diagnosis", value_original=_concept_text(r.get("code")), code=code, code_system=system, effective_time=r.get("onsetDateTime") or r.get("recordedDate"), recorded_time=r.get("recordedDate"), source=_source(r), transformer="fhir-source-native", transformer_version="1"))

    for r in snapshot.get("observations", []):
        concept = _concept_text(r.get("code")); code, system = _coding(r.get("code")); quantity = r.get("valueQuantity") or {}; value = quantity.get("value")
        if value is None:
            value = _concept_text(r.get("valueCodeableConcept")) if r.get("valueCodeableConcept") else r.get("valueString", "Unbenannt")
        facts.append(ClinicalFact(fact_id=_fact_id(r), patient_ref=patient_id, fact_type=f"observation:{concept}", value_original=value, code=code, code_system=system, unit_original=quantity.get("unit") or quantity.get("code"), effective_time=r.get("effectiveDateTime") or r.get("issued"), recorded_time=r.get("issued"), source=_source(r), transformer="fhir-source-native", transformer_version="1"))

    for r in snapshot.get("medications", []):
        med = _concept_text(r.get("medicationCodeableConcept")); code, system = _coding(r.get("medicationCodeableConcept"))
        facts.append(ClinicalFact(fact_id=_fact_id(r), patient_ref=patient_id, fact_type="medication.current", value_original=med, code=code, code_system=system, effective_time=r.get("effectiveDateTime") or r.get("dateAsserted"), recorded_time=r.get("dateAsserted"), source=_source(r), transformer="fhir-source-native", transformer_version="1"))

    for r in snapshot.get("tasks", []):
        facts.append(ClinicalFact(fact_id=_fact_id(r), patient_ref=patient_id, fact_type="task.open" if r.get("status") not in {"completed", "cancelled"} else "task.closed", value_original=r.get("description") or _concept_text(r.get("code")), effective_time=r.get("authoredOn"), recorded_time=r.get("authoredOn"), source=_source(r), transformer="fhir-source-native", transformer_version="1"))

    for r in snapshot.get("documents", []):
        code, system = _coding(r.get("type"))
        facts.append(ClinicalFact(fact_id=_fact_id(r), patient_ref=patient_id, fact_type="document.reference", value_original=_concept_text(r.get("type")), code=code, code_system=system, effective_time=r.get("date") or (r.get("context") or {}).get("period", {}).get("start"), recorded_time=r.get("date"), source=_source(r), transformer="fhir-source-native", transformer_version="1"))

    return TruthEnvelope(patient_ref=patient_id, facts=facts)


def _summary(fact: ClinicalFact) -> str:
    value = str(fact.value_original)
    if fact.fact_type.startswith("observation:"):
        concept = fact.fact_type.split(":", 1)[1]; unit = f" {fact.unit_original}" if fact.unit_original else ""
        return f"{concept}: {value}{unit}"
    return value


def snapshot_to_timeline(snapshot: dict[str, Any]) -> dict[str, Any]:
    truth = snapshot_to_truth(snapshot)
    title_map = {"allergy": "Allergie / Unverträglichkeit", "diagnosis": "Diagnose", "medication.current": "Aktuelle Medikation", "task.open": "Offene Aufgabe", "task.closed": "Aufgabe", "document.reference": "Dokument"}
    items: list[dict[str, Any]] = []
    for fact in truth.facts:
        source = fact.source; title = "Messwert" if fact.fact_type.startswith("observation:") else title_map.get(fact.fact_type, "Klinischer Fakt"); severity = "attention" if fact.fact_type in {"allergy", "task.open"} else "info"
        items.append({"fact_id": fact.fact_id, "resource_type": source.resource_type, "resource_id": source.resource_id, "resource_version": source.resource_version, "source": source.system, "title": title, "summary": _summary(fact), "date": fact.effective_time.isoformat() if fact.effective_time else "", "severity": severity, "fact_status": fact.status.value, "provenance_complete": fact.provenance_complete})
    items.sort(key=lambda x: x.get("date") or "", reverse=True)
    return {"patient": {"id": snapshot["patient"].get("id"), "name": _display_name(snapshot["patient"]), "birthDate": snapshot["patient"].get("birthDate")}, "items": items, "count": len(items), "provenance_coverage": truth.provenance_coverage(), "review_queue_count": len(truth.review_queue()), "provenance_policy": "Every surfaced fact passes through ClinicalFact and retains source resource identity/version; document extraction additionally requires exact evidence spans."}
