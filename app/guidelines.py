from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class GuidelineSource:
    id: str
    title: str
    publisher: str
    jurisdiction: str
    topic: str
    status: str
    version: str
    published: str | None
    last_reviewed: str | None
    url: str
    authority_tier: str
    notes: str


SOURCES = [
    GuidelineSource(
        id="de-nvl-program",
        title="Nationale VersorgungsLeitlinien (NVL)",
        publisher="AWMF + Zentralinstitut für die kassenärztliche Versorgung (Zi)",
        jurisdiction="DE",
        topic="cross-sector national care guidelines",
        status="active",
        version="program",
        published=None,
        last_reviewed="2026-03-25",
        url="https://www.leitlinien.de/",
        authority_tier="national",
        notes="Only publisher-hosted NVL documents are treated as authoritative; versions and validity are tracked explicitly.",
    ),
    GuidelineSource(
        id="de-awmf-register",
        title="AWMF Leitlinienregister",
        publisher="AWMF",
        jurisdiction="DE",
        topic="specialty guidelines",
        status="active",
        version="registry",
        published=None,
        last_reviewed="2026-08-15",
        url="https://register.awmf.org/de/leitlinien/aktuelle-leitlinien",
        authority_tier="national-specialty",
        notes="Source registry for current, updated and in-development German specialty guidelines.",
    ),
    GuidelineSource(
        id="intl-kdigo-ckd-2024",
        title="KDIGO 2024 Clinical Practice Guideline for Evaluation and Management of CKD",
        publisher="KDIGO",
        jurisdiction="INTL",
        topic="chronic kidney disease",
        status="current-with-focused-update-underway",
        version="2024",
        published="2024-03-13",
        last_reviewed="2026-08-15",
        url="https://kdigo.org/guidelines/ckd-evaluation-and-management/",
        authority_tier="international-specialty",
        notes="Current global CKD standard; KDIGO reports a focused Chapter 3 update underway.",
    ),
    GuidelineSource(
        id="uk-nice-ng203",
        title="NICE NG203: Chronic kidney disease: assessment and management",
        publisher="NICE",
        jurisdiction="UK",
        topic="chronic kidney disease",
        status="current",
        version="NG203",
        published="2021-08-25",
        last_reviewed="2025-08-19",
        url="https://www.nice.org.uk/guidance/ng203",
        authority_tier="international-reference",
        notes="International comparison source. Local German guidance/policy takes precedence for German deployment.",
    ),
    GuidelineSource(
        id="who-smart-guidelines",
        title="WHO SMART Guidelines",
        publisher="World Health Organization",
        jurisdiction="INTL",
        topic="digital guideline implementation",
        status="active",
        version="program",
        published=None,
        last_reviewed="2026-08-15",
        url="https://www.who.int/teams/digital-health-and-innovation/smart-guidelines",
        authority_tier="international-framework",
        notes="Framework for translating recommendations into interoperable digital implementation artifacts.",
    ),
]


def list_sources() -> list[dict[str, Any]]:
    return [asdict(s) for s in SOURCES]


def select_guidance(topic: str, country: str = "DE") -> dict[str, Any]:
    """Return source hierarchy, not a treatment recommendation."""
    matches = [s for s in SOURCES if topic.lower() in s.topic.lower()]
    local = [s for s in matches if s.jurisdiction == country]
    international = [s for s in matches if s.jurisdiction not in {country, "DE"} or s.jurisdiction == "INTL"]
    return {
        "topic": topic,
        "country": country,
        "local_first": [asdict(s) for s in local],
        "international_context": [asdict(s) for s in international],
        "policy": [
            "Never silently replace local hospital policy with an external guideline.",
            "Every displayed guidance item must show publisher, version/status and source URL.",
            "New or changed guidance enters a review queue; it is never auto-applied to patient care.",
            "CareOS V8 provides reference context only, not patient-specific treatment recommendations.",
        ],
    }
