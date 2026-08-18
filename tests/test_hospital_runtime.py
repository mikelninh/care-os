from datetime import datetime, timezone

import pytest

from app.clinical_truth import ClinicalFact, SourceKind, SourceRef, TruthEnvelope
from app.connectors.base import ConnectorCapabilities, ConnectorReadResult
from app.hospital_install import (
    DeploymentIntent,
    HospitalManifest,
    InterfaceKind,
    PatientIdentityStrategy,
    SourceSystem,
    SystemRole,
)
from app.hospital_runtime import HospitalRuntime, HospitalRuntimeError
from app.patient_id_resolver import StaticPatientIdResolver
from app.source_state import SourceAvailability, SourceState


class FakeConnector:
    def __init__(self, connector_id: str, *, available: bool = True, wrong_patient: bool = False):
        self.connector_id = connector_id
        self.available = available
        self.wrong_patient = wrong_patient
        self.last_requested_patient_ref = None

    def capabilities(self):
        return ConnectorCapabilities(connector_id=self.connector_id, vendor="fake", standard="FHIR R4")

    def read_patient_truth(self, patient_ref: str):
        self.last_requested_patient_ref = patient_ref
        now = datetime.now(timezone.utc)
        if not self.available:
            return ConnectorReadResult(
                connector_id=self.connector_id,
                source_state=SourceState(
                    source_id=self.connector_id,
                    availability=SourceAvailability.UNAVAILABLE,
                    observed_at=now,
                    detail="synthetic outage",
                ),
                truth=None,
            )
        fact_patient = "OTHER-PATIENT" if self.wrong_patient else patient_ref
        fact = ClinicalFact(
            fact_id="Observation:1",
            patient_ref=fact_patient,
            fact_type="observation:test",
            value_original="synthetic",
            source=SourceRef(
                kind=SourceKind.FHIR,
                system=self.connector_id,
                resource_type="Observation",
                resource_id="1",
            ),
        )
        return ConnectorReadResult(
            connector_id=self.connector_id,
            source_state=SourceState(
                source_id=self.connector_id,
                availability=SourceAvailability.CURRENT,
                last_success_at=now,
                observed_at=now,
            ),
            truth=TruthEnvelope(patient_ref=fact_patient, facts=[fact]),
        )


def source(source_id: str):
    return SourceSystem(
        source_id=source_id,
        role=SystemRole.KIS,
        vendor="Vendor",
        product=source_id,
        version="1",
        interfaces=[InterfaceKind.FHIR_R4],
        patient_identity_available=True,
        source_resource_ids_available=True,
        effective_time_available=True,
        lifecycle_state_available=True,
    )


def manifest(strategy=PatientIdentityStrategy.SHARED_ENTERPRISE_ID):
    return HospitalManifest(
        hospital_id="H1",
        site_name="Synthetic Hospital",
        deployment_intent=DeploymentIntent.DEIDENTIFIED,
        sources=[source("kis"), source("lis")],
        oidc_or_sso_available=True,
        trusted_patient_context_launch=True,
        patient_identity_strategy=strategy,
        audit_destination_available=True,
        rollback_owner_named=True,
        security_owner_named=True,
        privacy_owner_named=True,
        clinical_owner_named=True,
    )


def test_multi_source_runtime_namespaces_facts_and_is_complete_when_all_current():
    runtime = HospitalRuntime(manifest(), {"kis": FakeConnector("kis"), "lis": FakeConnector("lis")})
    result = runtime.read_patient_context("P1")
    assert result.complete is True
    assert result.may_assert_absence is True
    assert {fact.fact_id for fact in result.truth.facts} == {"kis:Observation:1", "lis:Observation:1"}
    assert {fact.source.system for fact in result.truth.facts} == {"kis", "lis"}
    assert {fact.patient_ref for fact in result.truth.facts} == {"P1"}


def test_one_source_outage_keeps_partial_facts_but_forbids_absence_claims():
    runtime = HospitalRuntime(manifest(), {"kis": FakeConnector("kis"), "lis": FakeConnector("lis", available=False)})
    result = runtime.read_patient_context("P1")
    assert result.complete is False
    assert result.may_assert_absence is False
    assert [fact.fact_id for fact in result.truth.facts] == ["kis:Observation:1"]
    assert any("must not be interpreted as absent" in warning for warning in result.warnings)


def test_wrong_patient_from_any_connector_is_rejected():
    runtime = HospitalRuntime(manifest(), {"kis": FakeConnector("kis"), "lis": FakeConnector("lis", wrong_patient=True)})
    with pytest.raises(HospitalRuntimeError, match="wrong source patient|wrong patient"):
        runtime.read_patient_context("P1")


def test_multi_source_runtime_refuses_unknown_cross_source_identity_strategy():
    with pytest.raises(HospitalRuntimeError, match="explicit governed patient identity strategy"):
        HospitalRuntime(
            manifest(PatientIdentityStrategy.UNKNOWN),
            {"kis": FakeConnector("kis"), "lis": FakeConnector("lis")},
        )


def test_trusted_mpi_strategy_requires_resolver():
    with pytest.raises(HospitalRuntimeError, match="requires a deterministic PatientIdResolver"):
        HospitalRuntime(
            manifest(PatientIdentityStrategy.TRUSTED_MPI),
            {"kis": FakeConnector("kis"), "lis": FakeConnector("lis")},
        )


def test_trusted_mpi_maps_enterprise_patient_to_source_specific_ids_then_normalizes_truth():
    kis = FakeConnector("kis")
    lis = FakeConnector("lis")
    resolver = StaticPatientIdResolver(
        mappings={"ENTERPRISE-1": {"kis": "KIS-123", "lis": "LIS-ABC"}},
        namespace_by_source={"kis": "urn:hospital:kis", "lis": "urn:hospital:lis"},
    )
    runtime = HospitalRuntime(
        manifest(PatientIdentityStrategy.TRUSTED_MPI),
        {"kis": kis, "lis": lis},
        patient_id_resolver=resolver,
    )
    result = runtime.read_patient_context("ENTERPRISE-1")

    assert kis.last_requested_patient_ref == "KIS-123"
    assert lis.last_requested_patient_ref == "LIS-ABC"
    assert result.patient_ref == "ENTERPRISE-1"
    assert {fact.patient_ref for fact in result.truth.facts} == {"ENTERPRISE-1"}


def test_trusted_mpi_missing_mapping_fails_closed_before_connector_read():
    kis = FakeConnector("kis")
    lis = FakeConnector("lis")
    resolver = StaticPatientIdResolver(mappings={"ENTERPRISE-1": {"kis": "KIS-123"}})
    runtime = HospitalRuntime(
        manifest(PatientIdentityStrategy.TRUSTED_MPI),
        {"kis": kis, "lis": lis},
        patient_id_resolver=resolver,
    )
    with pytest.raises(HospitalRuntimeError, match="failed closed"):
        runtime.read_patient_context("ENTERPRISE-1")
    assert kis.last_requested_patient_ref is None
    assert lis.last_requested_patient_ref is None
