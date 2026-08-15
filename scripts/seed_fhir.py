from __future__ import annotations

import json
import os
from pathlib import Path
import httpx

base = os.getenv("FHIR_BASE_URL", "http://localhost:8080/fhir").rstrip("/")
bundle = json.loads(Path("integration/fhir_seed_bundle.json").read_text(encoding="utf-8"))
r = httpx.post(base, json=bundle, headers={"Content-Type":"application/fhir+json","Accept":"application/fhir+json"}, timeout=30)
r.raise_for_status()
print(json.dumps({"status":r.status_code,"base":base,"resourceType":r.json().get("resourceType")}, indent=2))
