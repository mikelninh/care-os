import pytest

from app.document_pipeline import DocumentInput
from app.temporal_normalization import TemporalNormalizationError, TemporalPrecision, normalize_explicit_date


def _doc(text):
    return DocumentInput(patient_ref="p1", document_id="d1", source_system="test", text=text)


def test_parses_explicit_german_date_from_exact_source_quote():
    doc = _doc("Blutkultur abgenommen am 16.08.2026. Befund folgt.")
    result = normalize_explicit_date(doc, "abgenommen am 16.08.2026")
    assert result.value.date().isoformat() == "2026-08-16"
    assert result.precision == TemporalPrecision.DATE
    assert doc.text[result.start:result.end] == "16.08.2026"


def test_parses_iso_datetime():
    doc = _doc("Probenzeit 2026-08-16T07:42 dokumentiert.")
    result = normalize_explicit_date(doc, "Probenzeit 2026-08-16T07:42")
    assert result.value.isoformat().startswith("2026-08-16T07:42")
    assert result.precision == TemporalPrecision.DATETIME


def test_refuses_relative_time_language():
    doc = _doc("Blutkultur gestern abgenommen.")
    with pytest.raises(TemporalNormalizationError):
        normalize_explicit_date(doc, "gestern")


def test_refuses_ambiguous_multiple_dates_in_one_evidence_quote():
    doc = _doc("Vergleich 15.08.2026 mit 16.08.2026.")
    with pytest.raises(TemporalNormalizationError):
        normalize_explicit_date(doc, "15.08.2026 mit 16.08.2026")


def test_refuses_invalid_calendar_date():
    doc = _doc("Datum 31.02.2026")
    with pytest.raises(TemporalNormalizationError):
        normalize_explicit_date(doc, "31.02.2026")


def test_refuses_non_unique_evidence_quote():
    doc = _doc("Datum 16.08.2026; Kopie Datum 16.08.2026")
    with pytest.raises(TemporalNormalizationError):
        normalize_explicit_date(doc, "Datum 16.08.2026")
