import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .demo_data import PATIENTS, TIMELINES, FOCUS, DOCUMENTATION_CASES, INBOX_ITEMS, PILOT_TASKS
from .impact import score_pilot_task, aggregate_results
from .safety import patient_match_decision
from .fhir_adapter import FhirClient, FhirUnavailable, snapshot_to_timeline, snapshot_to_truth
from .guidelines import list_sources, select_guidance
from .security_readiness import readiness as security_readiness
from .specialties import list_specialty_packs, specialty_demo
from .reference_environments import list_reference_environments, reference_environment
from .global_packs import architecture_manifest
from .monetization_agent import monetization_manifest
from .portability import ips_preview
from .readiness_gates import gate_manifest
from .deployment_policy import (
    DeploymentBlocked,
    assert_data_mode_allowed,
    assert_public_fhir_integration_route_allowed,
)
from .agent_readiness import agent_gate_manifest
from .agent_tools import synthetic_sjk_registry

BASE = Path(__file__).parent
STATIC = BASE / "static"
DATA_MODE = assert_data_mode_allowed(os.getenv("CAREOS_DATA_MODE", "synthetic"))

app = FastAPI(title="CareOS", version="9.1.0", description="Clinician-first, source-grounded healthcare workflow prototype")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


class PilotScoreRequest(BaseModel):
    task_id: str = Field(min_length=1, max_length=100)
    baseline_minutes: float = Field(gt=0, le=240)
    actual_seconds: float = Field(ge=0, le=14400)
    clicks: int = Field(default=0, ge=0, le=10000)
    searches: int = Field(default=0, ge=0, le=10000)
    calls: int = Field(default=0, ge=0, le=10000)
    corrections: int = Field(default=0, ge=0, le=10000)
    effort: int | None = Field(default=None, ge=1, le=5)
    success: bool = True


class PilotAggregateRequest(BaseModel):
    results: list[dict] = Field(default_factory=list, max_length=500)


def _assert_public_fhir_lab_route() -> None:
    try:
        assert_public_fhir_integration_route_allowed(DATA_MODE)
    except DeploymentBlocked as exc:
        raise HTTPException(403, str(exc)) from exc


@app.get("/")
def home():
    return FileResponse(STATIC / "index.html")


@app.get("/platform")
def platform_lab():
    return FileResponse(STATIC / "platform.html")


@app.get("/specialty")
def specialty_lab():
    return FileResponse(STATIC / "specialty.html")


@app.get("/api/specialties")
def specialties():
    return {"packs": list_specialty_packs()}


@app.get("/api/specialties/{pack_id}")
def specialty_pack(pack_id: str):
    pack = specialty_demo(pack_id)
    if not pack:
        raise HTTPException(404, "Specialty pack not found")
    return pack


@app.get("/api/reference-environments")
def reference_environments():
    return {"environments": list_reference_environments(), "mode": "synthetic-product-research"}


@app.get("/api/reference-environments/{env_id}")
def reference_environment_detail(env_id: str):
    env = reference_environment(env_id)
    if not env:
        raise HTTPException(404, "Reference environment not found")
    return env


@app.get("/api/architecture/packs")
def packs_manifest():
    return architecture_manifest()


@app.get("/api/readiness/gates")
def readiness_gates():
    return gate_manifest()


@app.get("/api/readiness/agents")
def agent_readiness_gates():
    return agent_gate_manifest()


@app.get("/api/agents/synthetic-tools")
def synthetic_agent_tools():
    return {
        "mode": "synthetic-only",
        "live_identifiable_phi_allowed": False,
        "tools": synthetic_sjk_registry().manifest(),
    }


@app.get("/api/readiness/data-mode")
def data_mode():
    return {"data_mode": DATA_MODE.value, "live_patient_data_allowed": gate_manifest()["live_patient_data_allowed"]}


@app.get("/api/global/ips-preview/{patient_id}")
def global_ips_preview(patient_id: str, language: str = Query(default="en", max_length=20)):
    result = ips_preview(patient_id, language)
    if not result:
        raise HTTPException(404, "Synthetic patient not found")
    return result


@app.get("/api/monetization/ethical-agent")
def ethical_monetization_agent():
    return monetization_manifest()


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "version": "9.1.0",
        "data_mode": DATA_MODE.value,
        "mode": "specialty-packs+reference-environments+integration-lab+evidence-backed-readiness-gates",
        "claims": [
            "live patient data mode refuses startup until G0-G5 pass",
            "agent identifiable-PHI use remains separately gated by A0-A9",
            "reference environments are synthetic product-research configurations, not endorsements or integrations",
            "no autonomous clinical decisions",
            "no production write-back",
            "ambiguous patient matching blocks automatic attachment",
            "utility metrics require measured task completion",
        ],
    }


@app.get("/api/patients")
def patients():
    return PATIENTS


@app.get("/api/patients/{patient_id}/focus")
def focus(patient_id: str):
    if patient_id not in FOCUS:
        raise HTTPException(404, "Synthetic patient not found")
    return FOCUS[patient_id]


@app.get("/api/patients/{patient_id}/timeline")
def timeline(
    patient_id: str,
    q: str = Query(default="", max_length=200),
    source: str = Query(default="all", max_length=100),
):
    if patient_id not in TIMELINES:
        raise HTTPException(404, "Synthetic patient not found")
    items = TIMELINES[patient_id]
    if source != "all":
        items = [x for x in items if x["source"].lower() == source.lower()]
    if q.strip():
        needle = q.strip().lower()
        items = [x for x in items if needle in " ".join([x["title"], x["summary"], x["source"], x.get("source_ref", "")]).lower()]
    return {"patient_id": patient_id, "items": items, "count": len(items)}


@app.get("/api/patients/{patient_id}/documentation")
def documentation(patient_id: str):
    if patient_id not in DOCUMENTATION_CASES:
        raise HTTPException(404, "No synthetic documentation case")
    return DOCUMENTATION_CASES[patient_id]


@app.get("/api/inbox")
def inbox():
    return INBOX_ITEMS


@app.get("/api/inbox/{item_id}/match-policy")
def match_policy(item_id: str):
    item = next((x for x in INBOX_ITEMS if x["id"] == item_id), None)
    if not item:
        raise HTTPException(404, "Synthetic inbox item not found")
    candidates = item.get("candidates", [])
    exact = item["status"] == "matched"
    count = 1 if exact else max(2, len(candidates))
    return patient_match_decision(item["match_confidence"], exact, count)


@app.get("/api/pilot/tasks")
def pilot_tasks():
    return PILOT_TASKS


@app.post("/api/pilot/score")
def pilot_score(p: PilotScoreRequest):
    return score_pilot_task(
        p.task_id,
        p.baseline_minutes,
        p.actual_seconds,
        clicks=p.clicks,
        searches=p.searches,
        calls=p.calls,
        corrections=p.corrections,
        effort=p.effort,
        success=p.success,
    )


@app.post("/api/pilot/aggregate")
def pilot_aggregate(p: PilotAggregateRequest):
    return aggregate_results(p.results)


@app.get("/api/fhir/capability")
def fhir_capability():
    _assert_public_fhir_lab_route()
    try:
        c = FhirClient().capability()
        return {"resourceType": c.get("resourceType"), "fhirVersion": c.get("fhirVersion"), "software": c.get("software"), "status": "connected"}
    except FhirUnavailable as exc:
        raise HTTPException(503, f"FHIR source unavailable: {exc}")


@app.get("/api/fhir/patients/{patient_id}/truth")
def fhir_patient_truth(patient_id: str):
    _assert_public_fhir_lab_route()
    try:
        truth = snapshot_to_truth(FhirClient().patient_snapshot(patient_id))
        return truth.model_dump(mode="json")
    except FhirUnavailable as exc:
        raise HTTPException(503, f"FHIR source unavailable: {exc}")


@app.get("/api/fhir/patients/{patient_id}/timeline")
def fhir_patient_timeline(patient_id: str):
    _assert_public_fhir_lab_route()
    try:
        return snapshot_to_timeline(FhirClient().patient_snapshot(patient_id))
    except FhirUnavailable as exc:
        raise HTTPException(503, f"FHIR source unavailable: {exc}")


@app.get("/api/guidelines/sources")
def guideline_sources():
    return {"sources": list_sources(), "mode": "reference-context-only"}


@app.get("/api/guidelines/select")
def guideline_select(
    topic: str = Query(default="chronic kidney disease", max_length=200),
    country: str = Query(default="DE", max_length=10),
):
    return select_guidance(topic, country)


@app.get("/api/security/readiness")
def security_gate():
    return security_readiness()


@app.get("/api/stress/latest")
def stress_latest():
    import json

    root = BASE.parent / "data"
    names = ["stress_report.json", "redteam_before_hardening.json", "redteam_after_hardening.json", "redteam_unseen_after_hardening.json", "platform_stress_report.json"]
    out = {}
    for name in names:
        path = root / name
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            data.pop("sample_failures", None)
            out[name] = data
    return out
