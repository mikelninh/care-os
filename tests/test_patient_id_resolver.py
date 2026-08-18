from datetime import datetime, timedelta, timezone

import pytest

from app.patient_id_resolver import (
    PatientResolution,
    ResolutionState,
    SourcePatientMapping,
    StaticPatientIdResolver,
)


def test_static_resolver_returns_exact_source_specific_mappings():
    resolver = StaticPatientIdResolver(
        mappings={"E1": {"kis": "K1", "lis": "L1"}},
        namespace_by_source={"kis": "urn:kis", "lis": "urn:lis"},
    )
    result = resolver.resolve("E1", ("kis", "lis"))
    assert result.state == ResolutionState.RESOLVED
    assert result.mapping_for("kis").source_patient_ref == "K1"
    assert result.mapping_for("lis").source_patient_ref == "L1"


def test_missing_enterprise_patient_is_not_found_without_guessing():
    result = StaticPatientIdResolver(mappings={}).resolve("E404", ("kis",))
    assert result.state == ResolutionState.NOT_FOUND
    assert result.mappings == ()


def test_ambiguous_and_unavailable_states_carry_no_authoritative_mapping():
    for state in (ResolutionState.AMBIGUOUS, ResolutionState.UNAVAILABLE):
        result = PatientResolution(
            enterprise_patient_ref="E1",
            state=state,
            detail=f"synthetic {state.value}",
        )
        with pytest.raises(ValueError, match="patient identity is"):
            result.mapping_for("kis")


def test_expired_mapping_fails_closed_as_stale_at_use_time():
    result = PatientResolution(
        enterprise_patient_ref="E1",
        state=ResolutionState.RESOLVED,
        mappings=(
            SourcePatientMapping(
                source_id="kis",
                source_patient_ref="K1",
                namespace="urn:kis",
                resolver_id="resolver",
                resolver_version="1",
                resolved_at=datetime.now(timezone.utc) - timedelta(hours=2),
                expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
            ),
        ),
    )
    with pytest.raises(ValueError, match="stale/expired"):
        result.mapping_for("kis")


def test_duplicate_source_mappings_are_rejected():
    now = datetime.now(timezone.utc)
    mapping = SourcePatientMapping(
        source_id="kis",
        source_patient_ref="K1",
        namespace="urn:kis",
        resolver_id="resolver",
        resolver_version="1",
        resolved_at=now,
    )
    with pytest.raises(ValueError, match="duplicate source mappings"):
        PatientResolution(
            enterprise_patient_ref="E1",
            state=ResolutionState.RESOLVED,
            mappings=(mapping, mapping),
        )
