from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel, Field

from ..clinical_truth import TruthEnvelope
from ..source_state import SourceState


class ConnectorCapabilities(BaseModel):
    connector_id: str = Field(min_length=1)
    vendor: str = Field(min_length=1)
    standard: str = Field(min_length=1)
    read_only: bool = True
    supports_resource_versions: bool = False
    supports_paging: bool = False
    supports_incremental_refresh: bool = False
    authentication_mode: str = "not-configured"
    resources: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ConnectorReadResult(BaseModel):
    connector_id: str
    source_state: SourceState
    truth: TruthEnvelope | None = None

    @property
    def safe_to_render(self) -> bool:
        return self.truth is not None and self.source_state.may_assert_absence


class ClinicalConnector(Protocol):
    connector_id: str

    def capabilities(self) -> ConnectorCapabilities: ...

    def read_patient_truth(self, patient_ref: str) -> ConnectorReadResult: ...
