from pathlib import Path

from fastapi.testclient import TestClient

from app.hospital_api import app
from app.hospital_install import (
    DeploymentIntent,
    HospitalManifest,
    InterfaceKind,
    SourceSystem,
    SystemRole,
)


def _manifest(path: Path):
    manifest = HospitalManifest(
        hospital_id="API-DEMO",
        site_name="API Synthetic Hospital",
        deployment_intent=DeploymentIntent.SYNTHETIC,
        sources=[
            SourceSystem(
                source_id="kis",
                role=SystemRole.KIS,
                vendor="Vendor",
                product="KIS",
                version="1",
                interfaces=[InterfaceKind.FHIR_R4],
                authentication_mode="synthetic-none",
                endpoint_env="KIS_FHIR_BASE_URL",
                patient_identity_available=True,
                source_resource_ids_available=True,
                effective_time_available=True,
                lifecycle_state_available=True,
            )
        ],
        oidc_or_sso_available=True,
        trusted_patient_context_launch=True,
        audit_destination_available=True,
        rollback_owner_named=True,
        security_owner_named=True,
        privacy_owner_named=True,
        clinical_owner_named=True,
    )
    path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")


def test_hospital_health_and_preflight_are_non_live(monkeypatch, tmp_path):
    manifest_path = tmp_path / "hospital.json"
    _manifest(manifest_path)
    monkeypatch.setenv("CAREOS_HOSPITAL_MANIFEST", str(manifest_path))
    client = TestClient(app)

    health = client.get("/health")
    assert health.status_code == 200
    body = health.json()
    assert body["hospital_id"] == "API-DEMO"
    assert body["live_identifiable_phi_allowed"] is False
    assert body["production_write_back"] is False

    preflight = client.get("/api/hospital/preflight")
    assert preflight.status_code == 200
    assert preflight.json()["installable_for_synthetic_or_deidentified"] is True
