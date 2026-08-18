import pytest

from app.care_coordination import CareRequestState, ContextReference, CareRequest, synthetic_coordination_request, transition_request


def test_draft_cannot_be_sent_without_human_or_governed_workflow_confirmation():
    request = synthetic_coordination_request()
    with pytest.raises(ValueError, match="requires governed"):
        transition_request(request, CareRequestState.REQUESTED, actor_id="agent-1", human_confirmed=False)


def test_confirmed_request_has_explicit_acknowledgement_lifecycle():
    request = synthetic_coordination_request()
    sent = transition_request(request, CareRequestState.REQUESTED, actor_id="user-1", human_confirmed=True).request
    received = transition_request(sent, CareRequestState.RECEIVED, actor_id="receiver-system").request
    accepted = transition_request(received, CareRequestState.ACCEPTED, actor_id="receiver-user").request
    scheduled = transition_request(accepted, CareRequestState.SCHEDULED, actor_id="receiver-user").request
    performed = transition_request(scheduled, CareRequestState.PERFORMED, actor_id="receiver-user").request
    result = transition_request(performed, CareRequestState.RESULT_AVAILABLE, actor_id="receiver-system").request
    complete = transition_request(result, CareRequestState.FOLLOW_UP_COMPLETE, actor_id="sender-user").request
    assert complete.state == CareRequestState.FOLLOW_UP_COMPLETE


def test_invalid_state_skip_is_rejected():
    request = synthetic_coordination_request()
    with pytest.raises(ValueError, match="invalid care-request transition"):
        transition_request(request, CareRequestState.RESULT_AVAILABLE, actor_id="x", human_confirmed=True)


def test_non_purpose_relevant_context_is_rejected():
    with pytest.raises(ValueError, match="not declared relevant"):
        CareRequest(
            request_id="r",
            patient_ref="p",
            sender_org="A",
            receiver_org="B",
            purpose="follow-up",
            owner="team",
            transport_profile="rail",
            context_refs=(ContextReference(source_ref="doc:unrelated", category="unrelated", purpose_relevant=False),),
        )


def test_transition_is_audited_without_clinical_free_text():
    transition = transition_request(
        synthetic_coordination_request(),
        CareRequestState.REQUESTED,
        actor_id="user-1",
        human_confirmed=True,
    )
    assert transition.audit_event["resource_type"] == "care-request"
    assert transition.audit_event["outcome"] == "requested"
