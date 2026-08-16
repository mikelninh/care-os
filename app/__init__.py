from __future__ import annotations

import os

from .deployment_policy import assert_data_mode_allowed, assert_fhir_source_allowed

# Package-level fail-closed guard: standalone scripts importing CareOS modules should
# not be able to bypass the application startup policy by skipping app.main.
CAREOS_DATA_MODE = assert_data_mode_allowed(os.getenv("CAREOS_DATA_MODE", "synthetic"))
assert_fhir_source_allowed(
    CAREOS_DATA_MODE,
    os.getenv("FHIR_BASE_URL", "http://localhost:8080/fhir"),
    external_deidentified_ack=os.getenv("CAREOS_EXTERNAL_DEIDENTIFIED_ACK", "false").lower() == "true",
)
