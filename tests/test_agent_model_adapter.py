import json

import httpx
import pytest

from app.agent_model_adapter import HttpJsonReasoningWorker, ModelEndpointPolicy
from app.agent_models import WorkerInput
from app.agent_modes import AgentOperatingMode


def client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def policy():
    return ModelEndpointPolicy(
        endpoint="https://model.internal/v1/agent",
        model_id="approved-model",
        model_version="1",
        allowed_host="model.internal",
    )


def test_model_adapter_accepts_schema_constrained_synthetic_proposal():
    def handler(request):
        body = json.loads(request.content)
        assert body["input"]["allowed_tool_ids"] == ["read-clinical-context"]
        return httpx.Response(200, json={"proposals": [{"tool_id":"read-clinical-context","operation":"read","data_categories":["microbiology"],"requested_records":2,"requested_pages":1}]})

    worker = HttpJsonReasoningWorker(policy(), AgentOperatingMode.SYNTHETIC, client(handler))
    proposals = worker.propose(WorkerInput(task="morning-review", source_text="synthetic", allowed_tool_ids=("read-clinical-context",), allowed_data_categories=("microbiology",)))
    assert proposals[0].tool_id == "read-clinical-context"


def test_model_adapter_rejects_policy_smuggling_fields_from_provider():
    def handler(request):
        return httpx.Response(200, json={"proposals": [{"tool_id":"read-clinical-context","operation":"read","data_categories":["microbiology"],"patient_ref":"other-patient"}]})
    worker = HttpJsonReasoningWorker(policy(), AgentOperatingMode.SYNTHETIC, client(handler))
    with pytest.raises(Exception):
        worker.propose(WorkerInput(task="x", source_text="synthetic", allowed_tool_ids=("read-clinical-context",), allowed_data_categories=("microbiology",)))


def test_model_adapter_is_locked_for_live_modes():
    worker = HttpJsonReasoningWorker(policy(), AgentOperatingMode.READ_ONLY_LIVE, client(lambda r: httpx.Response(500)))
    with pytest.raises(PermissionError):
        worker.propose(WorkerInput(task="x", source_text="x", allowed_tool_ids=(), allowed_data_categories=()))


def test_model_policy_rejects_host_mismatch_and_retention():
    bad_host = policy().model_copy(update={"allowed_host":"other.internal"})
    with pytest.raises(PermissionError):
        bad_host.assert_allowed(AgentOperatingMode.SYNTHETIC)
    retention = policy().model_copy(update={"retain_or_train":True})
    with pytest.raises(PermissionError):
        retention.assert_allowed(AgentOperatingMode.DEIDENTIFIED_SANDBOX)
