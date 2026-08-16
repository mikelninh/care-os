from pathlib import Path


def test_main_ui_binds_async_focus_and_timeline_responses_to_active_patient():
    js = Path("app/static/app.js").read_text(encoding="utf-8")
    assert "let focusRequestId=0,timelineRequestId=0" in js
    assert "if(requestId!==focusRequestId||patientId!==active)return" in js
    assert "if(requestId!==timelineRequestId||patientId!==active)return" in js
    assert "/api/patients/${encodeURIComponent(patientId)}/focus" in js
    assert "/api/patients/${encodeURIComponent(patientId)}/timeline" in js


def test_main_and_specialty_ui_have_html_escaping_boundary():
    main = Path("app/static/app.js").read_text(encoding="utf-8")
    specialty = Path("app/static/specialty.js").read_text(encoding="utf-8")
    assert "const esc=s=>" in main
    assert "const esc=s=>" in specialty
    for fragment in ["${esc(x.summary)}", "${esc(x.source_ref)}", "${esc(d.handover)}"]:
        assert fragment in main
    for fragment in ["${esc(c.value)}", "${esc(c.source)}", "${esc(x.summary)}", "${esc(x.ref)}"]:
        assert fragment in specialty


def test_demo_fallback_does_not_credit_failed_task_as_saved_time():
    js = Path("app/static/app.js").read_text(encoding="utf-8")
    assert "saved_minutes:payload.success?Math.max(0,payload.baseline_minutes-seconds/60):0" in js
