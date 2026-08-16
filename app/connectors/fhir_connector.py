from __future__ import annotations

from datetime import datetime, timezone

from ..fhir_adapter import FhirClient, FhirUnavailable, snapshot_to_truth
from ..source_state import SourceAvailability, SourceState
from .base import ConnectorCapabilities, ConnectorReadResult


class FHIRConnector:
    def __init__(self, client: FhirClient | None = None, *, connector_id: str = "fhir-r4", max_age_seconds: int = 300):
        self.client = client or FhirClient()
        self.connector_id = connector_id
        self.max_age_seconds = max_age_seconds

    def capabilities(self) -> ConnectorCapabilities:
        return ConnectorCapabilities(
            connector_id=self.connector_id,
            vendor="generic",
            standard="FHIR R4",
            read_only=True,
            supports_resource_versions=False,
            supports_paging=False,
            supports_incremental_refresh=False,
            authentication_mode="transport-specific / not implemented in generic demo adapter",
            resources=["Patient", "AllergyIntolerance", "Condition", "Observation", "MedicationStatement", "Task", "DocumentReference"],
            notes=[
                "meta.versionId is preserved when supplied, but version reconciliation/history is not implemented",
                "generic FHIR R4 does not imply ISiK conformance",
                "paging and incremental synchronization remain release blockers",
            ],
        )

    def read_patient_truth(self, patient_ref: str) -> ConnectorReadResult:
        now = datetime.now(timezone.utc)
        try:
            snapshot = self.client.patient_snapshot(patient_ref)
            truth = snapshot_to_truth(snapshot)
            state = SourceState(
                source_id=self.connector_id,
                availability=SourceAvailability.CURRENT,
                last_success_at=now,
                observed_at=now,
                max_age_seconds=self.max_age_seconds,
            )
            return ConnectorReadResult(connector_id=self.connector_id, source_state=state, truth=truth)
        except (FhirUnavailable, ValueError) as exc:
            state = SourceState(
                source_id=self.connector_id,
                availability=SourceAvailability.UNAVAILABLE,
                observed_at=now,
                max_age_seconds=self.max_age_seconds,
                detail=type(exc).__name__,
            )
            return ConnectorReadResult(connector_id=self.connector_id, source_state=state, truth=None)
