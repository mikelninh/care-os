from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

from .clinical_truth import ClinicalFact, SourceKind, SourceRef, TruthEnvelope


@dataclass
class FhirConfig:
    base_url: str = os.getenv("FHIR_BASE_URL", "http://localhost:8080/fhir")
    timeout_seconds: float = float(os.getenv("FHIR_TIMEOUT_SECONDS", "8"))


class FhirUnavailable(RuntimeError):
    pass


class FhirClient:
    """Small FHIR R4 adapter used by CareOS.

    It intentionally uses standard REST/search resources only. ISiK-specific profiles,
    authorization and terminology validation sit above/beside this transport layer and
    are not claimed here.
    """

    def __init__(self, config: FhirConfig | None = None, transport: httpx.BaseTransport | None = None):
        self.config = config or FhirConfig()
        self._client = httpx.Client(
            base_url=self.config.base_url.rstrip("/"),
            timeout=self.config.timeout_seconds,
            headers={"Accept": "application/fhir+json"},
            transport=transport,
        )

    def _get(self, path: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        try:
            r = self._client.get(path, params=params)
            r.raise_for_status()
            return r.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise FhirUnavailable(str(exc)) from exc

    def capability(self) -> dict[str, Any]:
        return self._get("/metadata")

    def patient(self, patient_id: str) -> dict[str, Any]:
        return self._get(f"/Patient/{patient_id}")

    def search(self, resource: str, **params: str) -> list[dict[str, Any]]:
        bundle = self._get(f"/{resource}", params=params)
        return [e["resource"] for e in bundle.get("entry", []) if e.get("resource")]

    def patient_snapshot(self, patient_id: str) -> dict[str, Any]:
        patient = self.patient(patient_id)
        allergies = self.search("AllergyIntolerance", patient=patient_id)
        conditions = self.search("Condition", patient=patient_id)
        observations = self.search("Observation", patient=patient_id, _sort="-date")
        medications = self.search("MedicationStatement", patient=patient_id, status="active")
        tasks = self.search("Task", patient=patient_id)
        documents = self.search("DocumentReference", patient=patient_id)
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
    """Convert source-native FHIR resources into the canonical CareOS fact contract.

    This is intentionally conservative: no LLM inference and no silent merging. The
    original source identity/version and clinical effective time are preserved before
    anything reaches a clinician-facing view.
    """

    patient_id = snapshot["patient"].get("id")
    if not patient_id:
        raise ValueError("FHIR Patient requires id before CareOS truth ingestion")

    facts: list[ClinicalFact] = []

    for r in snapshot.get("allergies", []):
        code, system = _coding(r.get("code"))
        facts.append(ClinicalFact(
            fact_id=_fact_id(r),
            patient_ref=patient_id,
            fact_type="allergy",
            value_original=_concept_text(r.get("code")),
            code=code,
            code_system=system,
            effective_time=r.get("recordedDate"),
            recorded_time=r.get("recordedDate"),
            source=_source(r),
            transformer="fhir-source-native",
            transformer_version="1",
        ))

    for r in snapshot.get("conditions", []):
        code, system = _coding(r.get("code"))
        facts.append(ClinicalFact(
            fact_id=_fact_id(r),
            patient_ref=patient_id,
            fact_type="diagnosis",
            value_original=_concept_text(r.get("code")),
            code=code,
            code_system=system,
            effective_time=r.get("onsetDateTime") or r.get("recordedDate"),
            recorded_time=r.get("recordedDate"),
            source=_source(r),
            transformer="fhir-source-native",
            transformer_version="1",
        ))

    for r in snapshot.get("observations", []):
        concept = _concept_text(r.get("code"))
        code, system = _coding(r.get("code"))
        quantity = r.get("valueQuantity") or {}
        value = quantity.get("value")
        if value is None:
            value = _concept_text(r.get("valueCodeableConcept")) if r.get("valueCodeableConcept") else r.get("valueString", "Unbenannt")
        facts.append(ClinicalFact(
            fact_id=_fact_id(r),
            patient_ref=patient_id,
            fact_type=f"observation:{concept}",
            value_original=value,
            code=code,
            code_system=system,
            unit_original=quantity.get("unit") or quantity.get("code"),
            effective_time=r.get("effectiveDateTime") or r.get("issued"),
            recorded_time=r.get("issued"),
            source=_source(r),
            transformer="fhir-source-native",
            transformer_version="1",
        ))

    for r in snapshot.get("medications", []):
        med = _concept_text(r.get("medicationCodeableConcept"))
        code, system = _coding(r.get("medicationCodeableConcept"))
        facts.append(ClinicalFact(
            fact_id=_fact_id(r),
            patient_ref=patient_id,
            fact_type="medication.current",
            value_original=med,
            code=code,
            code_system=system,
            effective_time=r.get("effectiveDateTime") or r.get("dateAsserted"),
            recorded_time=r.get("dateAsserted"),
            source=_source(r),
            transformer="fhir-source-native",
            transformer_version="1",
        ))

    for r in snapshot.get("tasks", []):
        facts.append(ClinicalFact(
            fact_id=_fact_id(r),
            patient_ref=patient_id,
            fact_type="task.open" if r.get("status") not in {"completed", "cancelled"} else "task.closed",
            value_original=r.get("description") or _concept_text(r.get("code")),
            effective_time=r.get("authoredOn"),
            recorded_time=r.get("authoredOn"),
            source=_source(r),
            transformer="fhir-source-native",
            transformer_version="1",
        ))

    for r in snapshot.get("documents", []):
        code, system = _coding(r.get("type"))
        facts.append(ClinicalFact(
            fact_id=_fact_id(r),
            patient_ref=patient_id,
            fact_type="document.reference",
            value_original=_concept_text(r.get("type")),
            code=code,
            code_system=system,
            effective_time=r.get("date") or (r.get("context") or {}).get("period", {}).get("start"),
            recorded_time=r.get("date"),
            source=_source(r),
            transformer="fhir-source-native",
            transformer_version="1",
        ))

    return TruthEnvelope(patient_ref=patient_id, facts=facts)


def _summary(fact: ClinicalFact) -> str:
    value = str(fact.value_original)
    if fact.fact_type.startswith("observation:"):
        concept = fact.fact_type.split(":", 1)[1]
        unit = f" {fact.unit_original}" if fact.unit_original else ""
        return f"{concept}: {value}{unit}"
    return value


def snapshot_to_timeline(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Render a compatibility timeline *from* the truth layer, not directly from FHIR."""

    truth = snapshot_to_truth(snapshot)
    title_map = {
        "allergy": "Allergie / Unverträglichkeit",
        "diagnosis": "Diagnose",
        "medication.current": "Aktuelle Medikation",
        "task.open": "Offene Aufgabe",
        "task.closed": "Aufgabe",
        "document.reference": "Dokument",
    }
    items: list[dict[str, Any]] = []
    for fact in truth.facts:
        source = fact.source
        title = "Messwert" if fact.fact_type.startswith("observation:") else title_map.get(fact.fact_type, "Klinischer Fakt")
        severity = "attention" if fact.fact_type in {"allergy", "task.open"} else "info"
        items.append({
            "fact_id": fact.fact_id,
            "resource_type": source.resource_type,
            "resource_id": source.resource_id,
            "resource_version": source.resource_version,
            "source": source.system,
            "title": title,
            "summary": _summary(fact),
            "date": fact.effective_time.isoformat() if fact.effective_time else "",
            "severity": severity,
            "fact_status": fact.status.value,
            "provenance_complete": fact.provenance_complete,
        })
    items.sort(key=lambda x: x.get("date") or "", reverse=True)
    return {
        "patient": {"id": snapshot["patient"].get("id"), "name": _display_name(snapshot["patient"]), "birthDate": snapshot["patient"].get("birthDate")},
        "items": items,
        "count": len(items),
        "provenance_coverage": truth.provenance_coverage(),
        "review_queue_count": len(truth.review_queue()),
        "provenance_policy": "Every surfaced fact passes through ClinicalFact and retains source resource identity/version; document extraction additionally requires exact evidence spans.",
    }
