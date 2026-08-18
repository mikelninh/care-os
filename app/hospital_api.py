from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException

from .deployment_policy import DeploymentBlocked
from .hospital_install import build_hospital_install_plan
from .hospital_runtime import HospitalRuntime, HospitalRuntimeError, load_hospital_manifest


app = FastAPI(
    title="CareOS Hospital Data Plane",
    version="pre-hospital",
    description=(
        "Hospital-local synthetic/deidentified interoperability data plane. "
        "Current release is not approved for identifiable live patient data or write-back."
    ),
)


def _manifest_path() -> Path:
    return Path(os.getenv("CAREOS_HOSPITAL_MANIFEST", "/etc/careos/hospital.json"))


def _manifest():
    path = _manifest_path()
    if not path.exists():
        raise HospitalRuntimeError(f"hospital manifest not found: {path}")
    return load_hospital_manifest(path)


@app.get("/health")
def health():
    try:
        manifest = _manifest()
        plan = build_hospital_install_plan(manifest)
        blockers = [check.id for check in plan.checks if check.status == "block"]
        return {
            "status": "ok" if not blockers else "preflight-blocked",
            "service": "careos-hospital-data-plane",
            "hospital_id": manifest.hospital_id,
            "country": manifest.country,
            "deployment_intent": manifest.deployment_intent.value,
            "preflight_blockers": blockers,
            "live_identifiable_phi_allowed": False,
            "production_write_back": False,
        }
    except (ValueError, OSError, HospitalRuntimeError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/hospital/preflight")
def preflight():
    try:
        manifest = _manifest()
        return build_hospital_install_plan(manifest).model_dump(mode="json")
    except (ValueError, OSError, HospitalRuntimeError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/hospital/patients/{patient_ref}/context")
def patient_context(patient_ref: str):
    """Read source-linked context from currently implemented local adapters.

    The route intentionally exists only in the synthetic/deidentified self-install
    service. A future live route must additionally require hospital identity,
    treatment-context authorization and production audit through approved orchestration.
    """

    try:
        manifest = _manifest()
        runtime = HospitalRuntime.from_environment(manifest)
        return runtime.read_patient_context(patient_ref).model_dump(mode="json")
    except DeploymentBlocked as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except (ValueError, OSError, HospitalRuntimeError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
