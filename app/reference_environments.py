from __future__ import annotations

from copy import deepcopy

from .specialties import SPECIALTY_PACKS


REFERENCE_ENVIRONMENTS = {
    "sjk-infectiology": {
        "id": "sjk-infectiology",
        "name": "St. Joseph Krankenhaus Berlin-Tempelhof · Infektiologie reference",
        "status": "public-information reference only; not endorsed or integrated",
        "synthetic_only": True,
        "location": "Berlin-Tempelhof",
        "public_context": {
            "inpatient": "Station 21",
            "day_clinic": "Station 21a / Tagesklinik und ASV-Ambulanz",
            "consult_service": "24/7 physician hotline",
            "clinical_strengths": [
                "HIV-associated disease and AIDS",
                "acute infectious diseases",
                "infective endocarditis",
                "periprosthetic and device-associated infections",
                "infection in immunosuppression",
                "antimicrobial stewardship",
            ],
        },
        "workflow_hypotheses": [
            {
                "id": "morning-board",
                "moment": "Früh-/Bettenbesprechung",
                "job": "In under 60 seconds, identify overnight changes, new positive microbiology, isolation changes and unresolved safety-critical items.",
                "success_metric": "time-to-first-correct-priority + missed critical item rate",
            },
            {
                "id": "ward-round",
                "moment": "Visite",
                "job": "Show the latest microbiology, antimicrobial record, relevant renal/hepatic trend, devices, isolation state and pending diagnostics with one-tap provenance.",
                "success_metric": "source searches/clicks + provenance opens + correction rate",
            },
            {
                "id": "results-chase",
                "moment": "Befunde sichten / anfordern",
                "job": "Distinguish pending, resulted, stale and unavailable tests so absence of data is never presented as a negative result.",
                "success_metric": "manual result chases + calls/faxes avoided + stale-result errors",
            },
            {
                "id": "microbiology",
                "moment": "Mikrobiologie",
                "job": "Keep specimen, collection time, organism, preliminary/final status, susceptibility and source together across the timeline.",
                "success_metric": "time to reconstruct microbiology story + wrong-source rate",
            },
            {
                "id": "handover",
                "moment": "Übergabe / Mittagsbesprechung",
                "job": "Prepare a source-linked concise handover that clearly separates documented facts, pending items and review-required uncertainty.",
                "success_metric": "handover preparation time + corrections + omitted pending items",
            },
            {
                "id": "day-clinic-continuity",
                "moment": "Tagesklinik / ASV",
                "job": "Bridge prior inpatient episodes, external documents and current ambulatory follow-up without forcing duplicate history collection.",
                "success_metric": "duplicate documentation + missing prior-context events",
            },
            {
                "id": "consult-hotline",
                "moment": "Infektiologisches Konsil / Hotline",
                "job": "Create a compact consult context containing the question, relevant microbiology, therapies, organ function, devices and exact missing information.",
                "success_metric": "time to answer consult + follow-up calls for missing context",
            },
            {
                "id": "ams-review",
                "moment": "Antimicrobial-Stewardship review",
                "job": "Surface documented antimicrobial course, microbiology timeline and unresolved diagnostics without making autonomous treatment recommendations.",
                "success_metric": "record reconstruction time + source completeness + clinician correction burden",
            },
        ],
        "must_never_do": [
            "Infer that an unavailable/pending microbiology result is negative.",
            "Recommend or change antimicrobial treatment autonomously.",
            "Auto-merge patients from name/date-of-birth similarity.",
            "Hide contradictory source information by selecting a winner silently.",
            "Send identifiable patient data to the public synthetic demo.",
        ],
        "questions_for_team": [
            "Welche 5 Informationen braucht ihr vor der Visite fast immer?",
            "Wo sucht ihr aktuell am längsten nach Befunden?",
            "Welche Ergebnisse müsst ihr am häufigsten telefonisch oder manuell nachverfolgen?",
            "Was wird bei Übergaben am häufigsten vergessen oder doppelt dokumentiert?",
            "Welche Information wäre gefährlich, wenn CareOS sie veraltet oder unvollständig zeigt?",
            "Welche Systeme/Fenster öffnet ihr für einen typischen infektiologischen Patienten?",
            "Welche lokalen SOPs oder Hygieneinformationen müssen im richtigen Moment sichtbar sein?",
            "Was dürfte CareOS auf keinen Fall automatisieren?",
        ],
    }
}


def list_reference_environments() -> list[dict]:
    return [deepcopy(item) for item in REFERENCE_ENVIRONMENTS.values()]


def reference_environment(env_id: str) -> dict | None:
    env = REFERENCE_ENVIRONMENTS.get(env_id)
    if env is None:
        return None
    result = deepcopy(env)
    if env_id == "sjk-infectiology":
        result["specialty_pack"] = deepcopy(SPECIALTY_PACKS["infectiology"])
        result["specialty_pack"]["demo"]["patient"]["ward"] = "Synthetischer Referenzfall · Station 21"
        result["specialty_pack"]["demo"]["patient"]["room"] = "synthetisch"
        result["specialty_pack"]["demo"]["headline"] = "Was muss das Team vor der nächsten Entscheidung wissen?"
    return result
