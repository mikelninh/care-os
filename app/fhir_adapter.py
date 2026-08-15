from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class FhirConfig:
    base_url: str = os.getenv("FHIR_BASE_URL", "http://localhost:8080/fhir")
    timeout_seconds: float = float(os.getenv("FHIR_TIMEOUT_SECONDS", "8"))


class FhirUnavailable(RuntimeError):
    pass


class FhirClient:
    """Small FHIR R4 adapter used by CareOS.

    It intentionally uses standard REST/search resources only. ISiK-specific profiles
    and validation sit above this transport layer and are not claimed here.
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


def snapshot_to_timeline(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Normalize FHIR resources to the clinician timeline while retaining source identity."""
    items: list[dict[str, Any]] = []
    for r in snapshot.get("allergies", []):
        items.append({"resource_type": "AllergyIntolerance", "resource_id": r.get("id"), "source": "FHIR", "title": "Allergie / Unverträglichkeit", "summary": _concept_text(r.get("code")), "date": r.get("recordedDate") or "", "severity": "attention"})
    for r in snapshot.get("conditions", []):
        items.append({"resource_type": "Condition", "resource_id": r.get("id"), "source": "FHIR", "title": "Diagnose", "summary": _concept_text(r.get("code")), "date": r.get("recordedDate") or r.get("onsetDateTime") or "", "severity": "info"})
    for r in snapshot.get("observations", []):
        value = r.get("valueQuantity") or {}
        summary = _concept_text(r.get("code"))
        if value.get("value") is not None:
            summary += f": {value['value']} {value.get('unit','') or value.get('code','')}".rstrip()
        items.append({"resource_type": "Observation", "resource_id": r.get("id"), "source": "FHIR", "title": "Messwert", "summary": summary, "date": r.get("effectiveDateTime") or r.get("issued") or "", "severity": "info"})
    for r in snapshot.get("medications", []):
        med = _concept_text(r.get("medicationCodeableConcept"))
        items.append({"resource_type": "MedicationStatement", "resource_id": r.get("id"), "source": "FHIR", "title": "Aktuelle Medikation", "summary": med, "date": r.get("dateAsserted") or "", "severity": "info"})
    for r in snapshot.get("tasks", []):
        items.append({"resource_type": "Task", "resource_id": r.get("id"), "source": "FHIR", "title": "Offene Aufgabe", "summary": r.get("description") or _concept_text(r.get("code")), "date": (r.get("authoredOn") or ""), "severity": "attention" if r.get("status") not in {"completed", "cancelled"} else "info"})
    for r in snapshot.get("documents", []):
        items.append({"resource_type": "DocumentReference", "resource_id": r.get("id"), "source": "FHIR", "title": "Dokument", "summary": _concept_text(r.get("type")), "date": r.get("date") or (r.get("context") or {}).get("period", {}).get("start") or "", "severity": "info"})
    items.sort(key=lambda x: x.get("date") or "", reverse=True)
    return {
        "patient": {"id": snapshot["patient"].get("id"), "name": _display_name(snapshot["patient"]), "birthDate": snapshot["patient"].get("birthDate")},
        "items": items,
        "count": len(items),
        "provenance_policy": "Every timeline item keeps its FHIR resource type + id; no silent source removal.",
    }
