from app.clinical_truth import AssertionStage
from app.connectors.hl7v2_connector import HL7V2Connector
from app.source_state import SourceAvailability


ADT = "\r".join(
    [
        "MSH|^~\\&|ADT|HOSP|CAREOS|HOSP|20260818100000||ADT^A01|MSG-ADT-1|P|2.5",
        "PID|||P1^^^HOSP^MR||Example^Patient",
        "PV1||I||||||||||||||||ENC-1",
    ]
)

ORU_PRELIM = "\r".join(
    [
        "MSH|^~\\&|LIS|HOSP|CAREOS|HOSP|20260818101000||ORU^R01|MSG-ORU-1|P|2.5",
        "PID|||P1^^^HOSP^MR||Example^Patient",
        "PV1||I||||||||||||||||ENC-1",
        "OBR|1|||CULTURE",
        "OBX|1|ST|CULTURE^Blood culture||growth detected||||||P|||20260818100500",
    ]
)

ORU_FINAL = "\r".join(
    [
        "MSH|^~\\&|LIS|HOSP|CAREOS|HOSP|20260818120000||ORU^R01|MSG-ORU-2|P|2.5",
        "PID|||P1^^^HOSP^MR||Example^Patient",
        "PV1||I||||||||||||||||ENC-1",
        "OBR|1|||CULTURE",
        "OBX|1|ST|CULTURE^Blood culture||final synthetic organism||||||F|||20260818115500",
    ]
)

ORU_CORRECTED = "\r".join(
    [
        "MSH|^~\\&|LIS|HOSP|CAREOS|HOSP|20260818130000||ORU^R01|MSG-ORU-3|P|2.5",
        "PID|||P1^^^HOSP^MR||Example^Patient",
        "OBX|1|ST|CULTURE^Blood culture||corrected synthetic organism||||||C|||20260818125500",
    ]
)


class Feed:
    def __init__(self, messages):
        self.messages = messages

    def messages_for_patient(self, patient_ref):
        return list(self.messages)


def test_oru_obx_values_become_source_linked_read_only_clinical_facts():
    connector = HL7V2Connector(feed=Feed([ADT, ORU_PRELIM, ORU_FINAL]), connector_id="lis-hl7")
    result = connector.read_patient_truth("P1")
    assert result.source_state.availability == SourceAvailability.CURRENT
    assert len(result.truth.facts) == 2
    assert result.truth.facts[0].assertion_stage == AssertionStage.PRELIMINARY
    assert result.truth.facts[1].assertion_stage == AssertionStage.FINAL
    assert all(f.source.resource_type == "HL7v2:OBX" for f in result.truth.facts)
    assert connector.capabilities().read_only is True


def test_corrected_result_state_is_preserved():
    result = HL7V2Connector(feed=Feed([ORU_CORRECTED])).read_patient_truth("P1")
    assert result.truth.facts[0].assertion_stage == AssertionStage.CORRECTED


def test_duplicate_message_control_id_is_idempotently_deduplicated():
    result = HL7V2Connector(feed=Feed([ORU_FINAL, ORU_FINAL])).read_patient_truth("P1")
    assert len(result.truth.facts) == 1


def test_wrong_patient_message_fails_visible_and_returns_no_truth():
    wrong = ORU_FINAL.replace("PID|||P1", "PID|||P2")
    result = HL7V2Connector(feed=Feed([wrong])).read_patient_truth("P1")
    assert result.source_state.availability == SourceAvailability.UNKNOWN
    assert "wrong patient" in result.source_state.detail
    assert result.truth is None


def test_malformed_partial_message_marks_source_unknown_instead_of_looking_empty():
    malformed = "MSH|^~\\&|LIS|HOSP|CAREOS|HOSP|20260818120000||ORU^R01|MSG-BAD|P|2.5\rPID|||P1\rOBX|1|ST|||value"
    result = HL7V2Connector(feed=Feed([ORU_FINAL, malformed])).read_patient_truth("P1")
    assert result.source_state.availability == SourceAvailability.UNKNOWN
    assert result.truth is not None
    assert len(result.truth.facts) == 1
    assert result.source_state.may_assert_absence is False
