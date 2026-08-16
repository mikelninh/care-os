from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from .document_pipeline import DocumentInput


class TemporalPrecision(str, Enum):
    DATE = "date"
    DATETIME = "datetime"


@dataclass(frozen=True)
class TemporalResult:
    value: datetime
    source_quote: str
    start: int
    end: int
    precision: TemporalPrecision
    parser_id: str
    parser_version: str


class TemporalNormalizationError(ValueError):
    pass


_PATTERNS = (
    ("iso-date", re.compile(r"\b(20\d{2})-(0[1-9]|1[0-2])-([0-2]\d|3[01])\b")),
    ("de-date", re.compile(r"\b([0-2]?\d|3[01])\.(0?\d|1[0-2])\.(20\d{2})\b")),
    ("iso-datetime", re.compile(r"\b(20\d{2})-(0[1-9]|1[0-2])-([0-2]\d|3[01])[T ]([01]\d|2[0-3]):([0-5]\d)(?::([0-5]\d))?\b")),
)


def _parse_match(parser_id: str, match: re.Match[str]) -> tuple[datetime, TemporalPrecision]:
    try:
        if parser_id == "iso-date":
            year, month, day = map(int, match.groups())
            return datetime(year, month, day, tzinfo=timezone.utc), TemporalPrecision.DATE
        if parser_id == "de-date":
            day, month, year = map(int, match.groups())
            return datetime(year, month, day, tzinfo=timezone.utc), TemporalPrecision.DATE
        if parser_id == "iso-datetime":
            year, month, day, hour, minute, second = match.groups()
            return datetime(
                int(year), int(month), int(day), int(hour), int(minute), int(second or 0),
                tzinfo=timezone.utc,
            ), TemporalPrecision.DATETIME
    except ValueError as exc:
        raise TemporalNormalizationError("invalid explicit calendar date") from exc
    raise TemporalNormalizationError("unsupported temporal parser")


def normalize_explicit_date(document: DocumentInput, evidence_quote: str) -> TemporalResult:
    """Admit only one explicit calendar date contained in one exact source quote.

    This deliberately refuses relative language (`gestern`, `heute`, `seit drei Tagen`),
    ambiguous numeric dates and dates not present in the cited source span. A separate
    governed module may add those semantics later with stronger contextual rules.
    """

    start = document.text.find(evidence_quote)
    if start < 0 or document.text.find(evidence_quote, start + 1) >= 0:
        raise TemporalNormalizationError("temporal evidence quote missing or non-unique")

    found: list[tuple[str, re.Match[str]]] = []
    for parser_id, pattern in _PATTERNS:
        found.extend((parser_id, m) for m in pattern.finditer(evidence_quote))

    # iso-datetime also contains an iso-date prefix; prefer the datetime match and
    # remove its contained date duplicate before enforcing uniqueness.
    datetime_matches = [(pid, m) for pid, m in found if pid == "iso-datetime"]
    if datetime_matches:
        dt = datetime_matches[0][1]
        found = [
            (pid, m) for pid, m in found
            if pid == "iso-datetime" or not (m.start() >= dt.start() and m.end() <= dt.end())
        ]

    if len(found) != 1:
        raise TemporalNormalizationError("temporal evidence must contain exactly one supported explicit date")

    parser_id, match = found[0]
    value, precision = _parse_match(parser_id, match)
    return TemporalResult(
        value=value,
        source_quote=evidence_quote,
        start=start + match.start(),
        end=start + match.end(),
        precision=precision,
        parser_id=parser_id,
        parser_version="1.0.0",
    )
