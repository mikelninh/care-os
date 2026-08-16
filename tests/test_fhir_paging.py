import httpx
import pytest

from app.fhir_adapter import FhirClient, FhirConfig, FhirUnavailable


def test_search_reads_all_bundle_pages():
    def handler(request: httpx.Request):
        if request.url.path == "/fhir/Observation" and request.url.params.get("page") == "2":
            return httpx.Response(200, json={
                "resourceType": "Bundle",
                "type": "searchset",
                "entry": [{"resource": {"resourceType": "Observation", "id": "o2"}}],
            })
        return httpx.Response(200, json={
            "resourceType": "Bundle",
            "type": "searchset",
            "entry": [{"resource": {"resourceType": "Observation", "id": "o1"}}],
            "link": [{"relation": "next", "url": "http://localhost:8080/fhir/Observation?page=2"}],
        })

    client = FhirClient(transport=httpx.MockTransport(handler))
    resources = client.search("Observation", patient="p1")
    assert [r["id"] for r in resources] == ["o1", "o2"]


def test_cross_origin_next_link_is_rejected():
    def handler(request: httpx.Request):
        return httpx.Response(200, json={
            "resourceType": "Bundle",
            "type": "searchset",
            "entry": [],
            "link": [{"relation": "next", "url": "https://attacker.example/steal"}],
        })

    client = FhirClient(transport=httpx.MockTransport(handler))
    with pytest.raises(FhirUnavailable, match="changed origin"):
        client.search("Observation", patient="p1")


def test_pagination_loop_is_rejected_instead_of_returning_partial_data():
    next_url = "http://localhost:8080/fhir/Observation?page=2"

    def handler(request: httpx.Request):
        return httpx.Response(200, json={
            "resourceType": "Bundle",
            "type": "searchset",
            "entry": [{"resource": {"resourceType": "Observation", "id": "o1"}}],
            "link": [{"relation": "next", "url": next_url}],
        })

    client = FhirClient(transport=httpx.MockTransport(handler))
    with pytest.raises(FhirUnavailable, match="loop detected"):
        client.search("Observation", patient="p1")


def test_max_pages_rejects_silent_truncation():
    config = FhirConfig(max_pages=1)

    def handler(request: httpx.Request):
        return httpx.Response(200, json={
            "resourceType": "Bundle",
            "type": "searchset",
            "entry": [],
            "link": [{"relation": "next", "url": "http://localhost:8080/fhir/Observation?page=2"}],
        })

    client = FhirClient(config=config, transport=httpx.MockTransport(handler))
    with pytest.raises(FhirUnavailable, match="partial results rejected"):
        client.search("Observation")


def test_non_bundle_search_response_is_rejected():
    client = FhirClient(transport=httpx.MockTransport(lambda _: httpx.Response(200, json={"resourceType": "Observation", "id": "oops"})))
    with pytest.raises(FhirUnavailable, match="not a Bundle"):
        client.search("Observation")
