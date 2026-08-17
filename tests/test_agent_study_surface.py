from pathlib import Path


def test_ab_study_surface_is_local_structured_and_has_no_free_text_answer_capture():
    html = Path("share/sjk-infectiology/ab.html").read_text(encoding="utf-8")
    lower = html.lower()
    assert "keine serverübertragung" in lower
    assert "keine freitextantworten" in lower
    assert "textarea" not in lower
    assert "fetch(" not in lower
    assert "xmlhttprequest" not in lower
    assert "crypto.subtle.digest('sha-256'" in lower
    assert "accepted_without_source_check" in html
    assert "pending_as_negative" in html
    assert "recommendation_misread" in html
    assert "agent_truth_confusion" in html


def test_ab_study_surface_has_two_cases_and_four_counterbalanced_sequences():
    html = Path("share/sjk-infectiology/ab.html").read_text(encoding="utf-8")
    assert "'case-a'" in html and "'case-b'" in html
    assert "[['case-a','careos'],['case-b','careos-agent']]" in html
    assert "[['case-b','careos-agent'],['case-a','careos']]" in html
    assert "[['case-b','careos'],['case-a','careos-agent']]" in html
    assert "[['case-a','careos-agent'],['case-b','careos']]" in html


def test_ab_study_surface_never_frames_speed_as_automatic_success():
    html = Path("share/sjk-infectiology/ab.html").read_text(encoding="utf-8")
    assert "Geschwindigkeit allein kann den Test nicht bestehen" in html
    assert "Ein Safety-Stop schlägt jeden Zeitgewinn" in html
