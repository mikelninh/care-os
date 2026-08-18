from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Protocol

from ..clinical_truth import AssertionStage, ClinicalFact, SourceKind, SourceRef, TruthEnvelope
from ..source_state import SourceAvailability, SourceState
from .base import ConnectorCapabilities, ConnectorReadResult


class HL7V2ParseError(ValueError):
    pass


class HL7MessageFeed(Protocol):
    def messages_for_patient(self, patient_ref: str) -> list[str]: ...


def _segments(message: str) -> list[list[str]]:
    raw_segments = [segment.strip() for segment in re.split(r"[\r\n]+", message.strip()) if segment.strip()]
    if not raw_segments or not raw_segments[0].startswith("MSH|"):
        raise HL7V2ParseError("HL7 v2 message must start with MSH segment")
    return [segment.split("|") for segment in raw_segments]


def _field(segment: list[str], number: int) -> str:
    # MSH is special because the field separator is encoded between MSH and field 2.
    index = number - 1 if segment[0] == "MSH" else number
    return segment[index].strip() if index < len(segment) else ""


def _first(segments: list[list[str]], name: str) -> list[str] | None:
    return next((segment for segment in segments if segment[0] == name), None)


def _parse_hl7_datetime(value: str) -> datetime | None:
    if not value:
        return None
    cleaned = value.split("+")[0].split("-")[0]
    for fmt in ("%Y%m%d%H%M%S", "%Y%m%d%H%M", "%Y%m%d"):
        try:
            return datetime.strptime(cleaned[: len(datetime.now().strftime(fmt))], fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def _assertion_stage(obx_status: str) -> AssertionStage:
    return {
        "P": AssertionStage.PRELIMINARY,
        "F": AssertionStage.FINAL,
        "C": AssertionStage.CORRECTED,
        "D": AssertionStage.CANCELLED,
        "X": AssertionStage.CANCELLED,
    }.get(obx_status.upper(), AssertionStage.UNKNOWN)


class ParsedHL7Message:
    def __init__(self, *, message_control_id: str, message_type: str, patient_ref: str, encounter_ref: str | None, segments: list[list[str]]):
        self.message_control_id = message_control_id
        self.message_type = message_type
        self.patient_ref = patient_ref
        self.encounter_ref = encounter_ref
        self.segments = segments


def parse_message(message: str) -> ParsedHL7Message:
    segments = _segments(message)
    msh = segments[0]
    pid = _first(segments, "PID")
    if pid is None:
        raise HL7V2ParseError("HL7 v2 message has no PID segment")
    message_type = _field(msh, 9).split("^")[0]
    message_control_id = _field(msh, 10)
    patient_ref = _field(pid, 3).split("~")[0].split("^")[0]
    pv1 = _first(segments, "PV1")
    encounter_ref = _field(pv1, 19).split("^")[0] if pv1 else None
    if not message_control_id:
        raise HL7V2ParseError("HL7 v2 message has no MSH-10 message control ID")
    if not patient_ref:
        raise HL7V2ParseError("HL7 v2 message has no PID-3 patient identifier")
    return ParsedHL7Message(
        message_control_id=message_control_id,
        message_type=message_type,
        patient_ref=patient_ref,
        encounter_ref=encounter_ref or None,
        segments=segments,
    )


def facts_from_oru(parsed: ParsedHL7Message, *, connector_id: str) -> list[ClinicalFact]:
    if parsed.message_type != "ORU":
        return []
    facts: list[ClinicalFact] = []
    for obx in (segment for segment in parsed.segments if segment[0] == "OBX"):
        set_id = _field(obx, 1) or str(len(facts) + 1)
        identifier = _field(obx, 3)
        value = _field(obx, 5)
        units = _field(obx, 6)
        status = _field(obx, 11)
        observed_at = _parse_hl7_datetime(_field(obx, 14))
        if not identifier:
            raise HL7V2ParseError(f"ORU {parsed.message_control_id} OBX-{set_id} has no OBX-3 identifier")
        fact_id = f"HL7:{parsed.message_control_id}:OBX:{set_id}"
        facts.append(
            ClinicalFact(
                fact_id=fact_id,
                patient_ref=parsed.patient_ref,
                fact_type=f"observation:{identifier}",
                logical_key=identifier,
                value_original=value,
                unit_original=units or None,
                effective_time=observed_at,
                recorded_time=observed_at,
                source=SourceRef(
                    kind=SourceKind.STRUCTURED_VENDOR,
                    system=connector_id,
                    resource_type="HL7v2:OBX",
                    resource_id=f"{parsed.message_control_id}:{set_id}",
                ),
                transformer="hl7v2-obx",
                transformer_version="1",
                assertion_stage=_assertion_stage(status),
            )
        )
    return facts


class HL7V2Connector:
    """Narrow read-only HL7 v2 connector for synthetic/deidentified ADT/ORU feeds.

    The connector understands patient/encounter context and ORU OBX observations. It
    intentionally does not claim universal HL7 v2 or MLLP/interface-engine support.
    """

    def __init__(self, *, feed: HL7MessageFeed, connector_id: str = "hl7v2"):
        self.feed = feed
        self.connector_id = connector_id

    def capabilities(self) -> ConnectorCapabilities:
        return ConnectorCapabilities(
            connector_id=self.connector_id,
            vendor="generic",
            standard="HL7 v2 narrow ADT/ORU read",
            read_only=True,
            supports_resource_versions=False,
            supports_paging=False,
            supports_incremental_refresh=False,
            authentication_mode="transport-owned",
            resources=["ADT patient/encounter context", "ORU/OBX observations"],
            notes=["synthetic/deidentified connector contract; real interface-engine compatibility is external evidence"],
        )

    def read_patient_truth(self, patient_ref: str) -> ConnectorReadResult:
        messages = self.feed.messages_for_patient(patient_ref)
        facts: list[ClinicalFact] = []
        seen_controls: set[str] = set()
        errors: list[str] = []
        now = datetime.now(timezone.utc)

        for raw in messages:
            try:
                parsed = parse_message(raw)
                if parsed.patient_ref != patient_ref:
                    raise HL7V2ParseError(
                        f"wrong patient: expected {patient_ref!r}, message contains {parsed.patient_ref!r}"
                    )
                if parsed.message_control_id in seen_controls:
                    continue
                seen_controls.add(parsed.message_control_id)
                facts.extend(facts_from_oru(parsed, connector_id=self.connector_id))
            except HL7V2ParseError as exc:
                errors.append(str(exc))

        if errors:
            state = SourceState(
                source_id=self.connector_id,
                availability=SourceAvailability.UNKNOWN,
                observed_at=now,
                detail="partial/malformed HL7 v2 feed: " + " | ".join(errors[:3]),
            )
            truth = TruthEnvelope(patient_ref=patient_ref, facts=facts) if facts else None
            return ConnectorReadResult(connector_id=self.connector_id, source_state=state, truth=truth)

        return ConnectorReadResult(
            connector_id=self.connector_id,
            source_state=SourceState(
                source_id=self.connector_id,
                availability=SourceAvailability.CURRENT,
                last_success_at=now,
                observed_at=now,
            ),
            truth=TruthEnvelope(patient_ref=patient_ref, facts=facts),
        )
