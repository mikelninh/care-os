from __future__ import annotations

import os
from typing import Any


def readiness(env: dict[str, str] | None = None) -> dict[str, Any]:
    e = env or os.environ
    cloud = e.get("DEPLOYMENT_MODE", "local-demo") == "cloud"
    checks = [
        {"id":"auth_oidc","required":True,"ok":e.get("AUTH_MODE") == "oidc","detail":"Production requires OIDC/SSO; demo auth is not accepted."},
        {"id":"oidc_issuer","required":True,"ok":str(e.get("OIDC_ISSUER", "")).startswith("https://"),"detail":"HTTPS OIDC issuer configured."},
        {"id":"oidc_audience","required":True,"ok":bool(e.get("OIDC_AUDIENCE")),"detail":"Audience validation configured."},
        {"id":"oidc_jwks","required":True,"ok":str(e.get("OIDC_JWKS_URI", "")).startswith("https://"),"detail":"HTTPS JWKS endpoint configured for asymmetric token verification."},
        {"id":"phi_logging","required":True,"ok":e.get("ALLOW_PHI_IN_LOGS", "false").lower() == "false","detail":"Ordinary telemetry must not contain clinical free text/PHI."},
        {"id":"audit_sink","required":True,"ok":bool(e.get("AUDIT_SINK")),"detail":"Immutable/central audit sink configured."},
        {"id":"audit_pseudonym_key","required":True,"ok":len(e.get("AUDIT_PSEUDONYM_KEY", "")) >= 32,"detail":"Deployment-specific high-entropy audit pseudonymization key configured; demo fallback is forbidden for live PHI."},
        {"id":"data_region","required":cloud,"ok":not cloud or e.get("DATA_REGION") in {"DE","EU","EEA"},"detail":"Cloud data region constrained for German deployment."},
        {"id":"c5_evidence","required":cloud,"ok":not cloud or bool(e.get("C5_ATTESTATION_ID")),"detail":"§393 SGB V cloud deployments need applicable C5/equivalent evidence; legal review required."},
        {"id":"writeback","required":True,"ok":e.get("CLINICAL_WRITEBACK", "disabled") == "disabled","detail":"Current production-read-only programme keeps autonomous clinical write-back disabled."},
        {"id":"fhir_tls","required":cloud,"ok":not cloud or e.get("FHIR_BASE_URL", "").startswith("https://"),"detail":"External FHIR transport uses TLS."},
    ]
    blockers = [c for c in checks if c["required"] and not c["ok"]]
    return {"ready": not blockers, "blockers": len(blockers), "checks": checks, "claim":"Configuration readiness gate only; not certification, legal advice or a compliance attestation."}
