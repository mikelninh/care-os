import pytest

from app.agent_data_projection import ProjectionError, project_for_model


def test_projection_keeps_only_allowed_source_linked_fields():
    facts = [
        {"fact_id":"f1","category":"microbiology","value":"E. coli","status":"final","source_ref":"LIS-1","name":"must-not-pass"},
        {"fact_id":"f2","category":"genetics","value":"x","status":"final","source_ref":"LAB-2"},
    ]
    projected = project_for_model(facts, allowed_categories={"microbiology"})
    assert projected == [{"fact_id":"f1","category":"microbiology","value":"E. coli","status":"final","effective_time":None,"source_ref":"LIS-1"}]
    assert "name" not in projected[0]


def test_projection_requires_source_reference():
    with pytest.raises(ProjectionError):
        project_for_model([{"fact_id":"f1","category":"microbiology","value":"x"}], allowed_categories={"microbiology"})


def test_projection_rejects_direct_identifier_if_it_enters_allowed_shape():
    # The fixed output shape prevents arbitrary source keys from crossing the boundary.
    out = project_for_model([{"fact_id":"f1","category":"microbiology","value":"x","source_ref":"src","patient_id":"p1"}], allowed_categories={"microbiology"})
    assert all("patient" not in key for key in out[0])


def test_projection_filters_undelegated_categories_and_bounds_size():
    facts = [{"fact_id":f"f{i}","category":"microbiology","value":i,"source_ref":f"s{i}"} for i in range(5)]
    assert len(project_for_model(facts, allowed_categories={"microbiology"}, max_facts=2)) == 2
    assert project_for_model(facts, allowed_categories={"medication"}) == []


def test_projection_cap_applies_after_category_filtering_not_before():
    facts = [
        *[{"fact_id":f"g{i}","category":"genetics","value":i,"source_ref":f"g{i}"} for i in range(50)],
        *[{"fact_id":f"m{i}","category":"microbiology","value":i,"source_ref":f"m{i}"} for i in range(10)],
    ]
    out = project_for_model(facts, allowed_categories={"microbiology"}, max_facts=5)
    assert [row["fact_id"] for row in out] == ["m0", "m1", "m2", "m3", "m4"]


def test_projection_rejects_oversized_fact_and_input_flood():
    oversized = [{"fact_id":"f1","category":"microbiology","value":"x" * 9000,"source_ref":"src"}]
    with pytest.raises(ProjectionError, match="size limit"):
        project_for_model(oversized, allowed_categories={"microbiology"})

    flooded = [{"fact_id":f"f{i}","category":"microbiology","value":i,"source_ref":f"s{i}"} for i in range(11)]
    with pytest.raises(ProjectionError, match="input exceeds"):
        project_for_model(flooded, allowed_categories={"microbiology"}, max_facts=5, max_input_facts=10)
