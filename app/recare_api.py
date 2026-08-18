from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .recare_capstone import CapstoneRunRequest, capstone_capabilities, run_capstone

app = FastAPI(
    title="CareOS Recare Capstone API",
    version="1.0.0",
    description=(
        "Synthetic-only runnable proof for agent routing, deterministic tool authorization, "
        "grounded drafting, observability and evaluation. Not for clinical use."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mikelninh.github.io", "http://localhost:8000", "http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "careos-recare-capstone",
        "data_mode": "synthetic-only",
        "live_identifiable_phi_allowed": False,
        "production_write_back": False,
    }


@app.get("/api/capabilities")
def capabilities():
    return capstone_capabilities()


@app.post("/api/run")
def run(request: CapstoneRunRequest):
    try:
        return run_capstone(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
