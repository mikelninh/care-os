from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path

from pydantic import BaseModel, Field

from .clinical_truth import ClinicalFact, TruthEnvelope
from .connectors.base import ClinicalConnector, ConnectorReadResult
from .connectors.fhir_connector import FHIRConnector
from .deployment_policy import DataMode, DeploymentBlocked
from .fhir_adapter import FhirClient, FhirConfig
from .hospital_install import (
    DeploymentIntent,
    HospitalManifest,
    InterfaceKind,
    PatientIdentityStrategy,
    build_hospital_install_plan,
)
from .source_state import SourceAvailability


class HospitalRuntimeError(RuntimeError):
    pass


class HospitalSourceStatus(BaseModel):
    source_id: str
    availability: str
    last_success_at: str | None = None
    detail: str | None = None


class HospitalContextResult(BaseModel):
    hospital_id: str
    patient_ref: str
    complete: bool
    may_assert_absence: bool
    source_status: list[HospitalSourceStatus]
    truth: TruthEnvelope | None
    warnings: list[str] = Field(default_factory=list)


class BearerFhirClient(FhirClient):
    """FHIR client with a deployment-supplied bearer token.

    Token values are read from the hospital process environment/secret injection and
    are never stored in HospitalManifest or returned by the runtime API.
    """

    def __init__(self, *, config: FhirConfig, data_mode: DataMode, token: str | None, external_deidentified_ack: bool):
        super().__init__(
            config=config,
            data_mode=data_mode,
            external_deidentified_ack=external_deidentified_ack,
        )
        if token:
            # FhirClient owns this httpx client. Authentication belongs to the
            # deployment adapter, never the source manifest or model layer.
            self._client.headers["Authorization"] = f"Bearer {token}"


def load_hospital_manifest(path: str | Path) -> HospitalManifest:
    return HospitalManifest.model_validate_json(Path(path).read_text(encoding="utf-8"))


def _data_mode(intent: DeploymentIntent) -> DataMode:
    if intent == DeploymentIntent.SYNTHETIC:
        return DataMode.SYNTHETIC
    if intent == DeploymentIntent.DEIDENTIFIED:
        return DataMode.DEIDENTIFIED_EVALUATION
    raise DeploymentBlocked("hospital runtime factory is currently limited to synthetic/deidentified evaluation")


def _source_endpoint(source, env: Mapping[str, str]) -> str:
    if not source.endpoint_env:
        raise HospitalRuntimeError(f"{source.source_id}: endpoint_env is required for runnable FHIR adapter")
    endpoint = str(env.get(source.endpoint_env, "")).strip()
    if not endpoint:
        raise HospitalRuntimeError(f"{source.source_id}: environment variable {source.endpoint_env} is not set")
    return endpoint


def _source_token(source, env: Mapping[str, str]) -> str | None:
    mode = source.authentication_mode.strip().lower()
    if mode in {"none", "no-auth", "synthetic-none"}:
        return None
    if mode not in {"bearer-token", "oidc-bearer", "hospital-oidc"}:
        raise HospitalRuntimeError(
            f"{source.source_id}: authentication mode {source.authentication_mode!r} is not implemented by the current self-install runtime"
        )
    if not source.credential_env:
        raise HospitalRuntimeError(f"{source.source_id}: credential_env is required for bearer authentication")
    token = str(env.get(source.credential_env, "")).strip()
    if not token:
        raise HospitalRuntimeError(f"{source.source_id}: credential environment variable {source.credential_env} is not set")
    return token


def build_connectors_from_manifest(
    manifest: HospitalManifest,
    *,
    env: Mapping[str, str] | None = None,
) -> dict[str, ClinicalConnector]:
    """Instantiate only currently implemented adapter runtimes.

    This is intentionally not a plugin magic trick. Contract-only HL7/vendor/UI
    adapters stay blocked until code + conformance evidence exists.
    """

    env = env or os.environ
    plan = build_hospital_install_plan(manifest)
    if manifest.deployment_intent not in {DeploymentIntent.SYNTHETIC, DeploymentIntent.DEIDENTIFIED}:
        raise DeploymentBlocked("self-install runtime is currently synthetic/deidentified only")
    if not plan.installable_for_synthetic_or_deidentified:
        blockers = "; ".join(check.message for check in plan.checks if check.status == "block")
        raise HospitalRuntimeError("hospital preflight is blocked: " + blockers)

    mode = _data_mode(manifest.deployment_intent)
    external_ack = str(env.get("CAREOS_EXTERNAL_DEIDENTIFIED_ACK", "false")).lower() in {"1", "true", "yes", "on"}
    by_source = {source.source_id: source for source in manifest.sources}
    connectors: dict[str, ClinicalConnector] = {}

    for adapter in plan.adapters:
        if adapter.direction != "read":
            continue
        if not adapter.runtime_available:
            raise HospitalRuntimeError(f"{adapter.source_id}: selected adapter is not runnable")
        if adapter.interface not in {InterfaceKind.ISIK_FHIR, InterfaceKind.FHIR_R4}:
            raise HospitalRuntimeError(f"{adapter.source_id}: runtime factory currently supports FHIR-family adapters only")

        source = by_source[adapter.source_id]
        endpoint = _source_endpoint(source, env)
        token = _source_token(source, env)
        client = BearerFhirClient(
            config=FhirConfig(base_url=endpoint),
            data_mode=mode,
            token=token,
            external_deidentified_ack=external_ack,
        )
        connectors[source.source_id] = FHIRConnector(client=client, connector_id=source.source_id)

    if len(connectors) != len(manifest.sources):
        raise HospitalRuntimeError("not every declared clinical source received a runnable connector")
    return connectors


def _namespace_fact(source_id: str, fact: ClinicalFact) -> ClinicalFact:
    clone = fact.model_copy(deep=True)
    clone.fact_id = f"{source_id}:{fact.fact_id}"
    if clone.supersedes_fact_id:
        clone.supersedes_fact_id = f"{source_id}:{clone.supersedes_fact_id}"
    clone.source.system = source_id
    return clone


class HospitalRuntime:
    def __init__(self, manifest: HospitalManifest, connectors: Mapping[str, ClinicalConnector]):
        self.manifest = manifest
        self.connectors = dict(connectors)
        if set(self.connectors) != {source.source_id for source in manifest.sources}:
            raise HospitalRuntimeError("runtime connector set must exactly match manifest sources")
        if len(manifest.sources) > 1 and manifest.patient_identity_strategy != PatientIdentityStrategy.SHARED_ENTERPRISE_ID:
            raise HospitalRuntimeError(
                "current multi-source runtime requires a governed shared-enterprise-id; trusted MPI integration is not implemented yet"
            )

    @classmethod
    def from_environment(cls, manifest: HospitalManifest, *, env: Mapping[str, str] | None = None) -> "HospitalRuntime":
        return cls(manifest, build_connectors_from_manifest(manifest, env=env))

    def read_patient_context(self, patient_ref: str) -> HospitalContextResult:
        source_status: list[HospitalSourceStatus] = []
        facts: list[ClinicalFact] = []
        warnings: list[str] = []
        complete = True

        for source in self.manifest.sources:
            result: ConnectorReadResult = self.connectors[source.source_id].read_patient_truth(patient_ref)
            availability = result.source_state.evaluated_availability()
            source_status.append(
                HospitalSourceStatus(
                    source_id=source.source_id,
                    availability=availability.value,
                    last_success_at=(
                        result.source_state.last_success_at.isoformat()
                        if result.source_state.last_success_at
                        else None
                    ),
                    detail=result.source_state.detail,
                )
            )

            if availability != SourceAvailability.CURRENT or result.truth is None:
                complete = False
                warnings.append(
                    f"{source.source_id} is {availability.value}; missing items from this source must not be interpreted as absent."
                )
                if result.truth is None:
                    continue

            for fact in result.truth.facts:
                if fact.patient_ref != patient_ref:
                    raise HospitalRuntimeError(f"{source.source_id}: connector returned a fact for the wrong patient")
                facts.append(_namespace_fact(source.source_id, fact))

        truth = TruthEnvelope(patient_ref=patient_ref, facts=facts) if facts else None
        return HospitalContextResult(
            hospital_id=self.manifest.hospital_id,
            patient_ref=patient_ref,
            complete=complete,
            may_assert_absence=complete,
            source_status=source_status,
            truth=truth,
            warnings=warnings,
        )
