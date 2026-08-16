from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class SandboxProfile(BaseModel):
    profile_id: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    identifiable_phi: bool = False
    read_only: bool = True
    external_egress: bool = False
    production_credentials: bool = False
    connector_shapes: set[str] = Field(default_factory=set)
    identity_shape: str = Field(min_length=1)
    audit_shape: str = Field(min_length=1)

    @model_validator(mode="after")
    def safe_sandbox(self) -> "SandboxProfile":
        if self.identifiable_phi:
            raise ValueError("deidentified sandbox must not contain identifiable PHI")
        if not self.read_only:
            raise ValueError("sandbox agent integration must remain read-only")
        if self.external_egress:
            raise ValueError("sandbox defaults to no external egress")
        if self.production_credentials:
            raise ValueError("sandbox must not use production credentials")
        return self


def sjk_deidentified_target_profile() -> SandboxProfile:
    """Target contract to fill with actual SJK IT discovery; not a claim of integration."""
    return SandboxProfile(
        profile_id="sjk-infectiology-deidentified-target",
        provider="St. Joseph Krankenhaus Berlin-Tempelhof reference target",
        connector_shapes={"patient-encounter", "microbiology", "selected-labs", "documented-antimicrobials", "pending-work"},
        identity_shape="synthetic/deidentified patient+encounter context; actual IdP/KIS launcher TBD",
        audit_shape="CareOS agent audit schema mapped to provider test sink; actual SIEM TBD",
    )
