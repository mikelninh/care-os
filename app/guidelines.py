from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
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
        id="de-rki-krinko",
        title="KRINKO recommendations",
        publisher="Robert Koch Institute / KRINKO",
        jurisdiction="DE",
        topic="infectiology infection prevention hospital hygiene",
        status="active",
        version="registry",
        published=None,
        last_reviewed="2026-08-15",
        url="https://www.rki.de/DE/Themen/Infektionskrankheiten/Krankenhaushygiene/KRINKO/Empfehlungen-der-KRINKO/empfehlungen-der-krinko-node.html",
        authority_tier="national-specialty",
        notes="Versioned infection-prevention context for the Infectiology Pack; local hospital SOP remains explicit.",
    ),
    GuidelineSource(
        id="de-onkopedia",
        title="Onkopedia guidelines",
        publisher="DGHO and partner societies",
        jurisdiction="DE",
        topic="oncology hematology",
        status="active",
        version="registry",
        published=None,
        last_reviewed="2026-08-15",
        url="https://www.onkopedia.com/de/onkopedia/guidelines",
        authority_tier="national-specialty",
        notes="Versioned oncology context; local tumour-board policy and intended clinical use remain separate.",
    ),
    GuidelineSource(
        id="de-dgn",
        title="DGN guidelines",
        publisher="German Society of Neurology (DGN)",
        jurisdiction="DE",
        topic="neurology",
        status="active",
        version="registry",
        published=None,
        last_reviewed="2026-08-15",
        url="https://www.dgn.org/leitlinien",
        authority_tier="national-specialty",
        notes="Neurology guidance registry; previous versions remain relevant for reproducibility.",
    ),
    GuidelineSource(
        id="hl7-ips-201",
        title="International Patient Summary Implementation Guide",
        publisher="HL7 International",
        jurisdiction="INTL",
        topic="cross-border portable patient summary",
        status="current-published",
        version="2.0.1 STU 2",
        published="2026-06-19",
        last_reviewed="2026-08-15",
        url="https://www.hl7.org/fhir/uv/ips/en/index.html",
        authority_tier="international-standard",
        notes="Portable summary interoperability baseline; CareOS preview is not a conformance claim.",
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
            "CareOS V9 provides reference context only, not patient-specific treatment recommendations.",
        ],
    }
