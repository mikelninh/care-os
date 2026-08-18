COUNTRY_PACKS = {
    "DE": {
        "name": "Deutschland",
        "interop": ["FHIR R4", "ISiK", "TI/ePA adapters", "EHDS/EEHRxF boundary"],
        "trust": ["provider identity", "TI identity/context path", "audit/logging"],
        "guidance": ["RKI/KRINKO", "AWMF/NVL", "DGN", "Onkopedia"],
        "status": "active-prototype",
    },
    "EU": {
        "name": "EU / cross-border",
        "interop": ["FHIR", "International Patient Summary", "MyHealth@EU", "EHDS/EEHRxF"],
        "trust": ["EHDS logging/interoperability components", "national contact/trust infrastructure"],
        "guidance": ["EU/national overlays"],
        "status": "architecture",
    },
    "EE": {
        "name": "Estonia",
        "interop": ["national Health Information System adapter", "FHIR/IPS portability boundary"],
        "trust": ["national digital identity", "citizen-visible access logs"],
        "guidance": ["national-source registry required"],
        "status": "reference-pattern-only",
    },
    "FI": {
        "name": "Finland",
        "interop": ["Kanta adapter", "FHIR migration boundary", "IPS portability boundary"],
        "trust": ["Kanta certification/joint testing", "professional authentication"],
        "guidance": ["national-source registry required"],
        "status": "reference-pattern-only",
    },
    "DK": {
        "name": "Denmark",
        "interop": ["National Service Platform adapter", "Shared Medication Record adapter", "FHIR/IPS portability boundary"],
        "trust": ["SEB/local IdP trust", "national service trust agreements"],
        "guidance": ["national-source registry required"],
        "status": "reference-pattern-only",
    },
    "NL": {
        "name": "Netherlands",
        "interop": ["MedMij-compatible boundary", "FHIR profiles", "IPS portability boundary"],
        "trust": ["MedMij participation/trust framework"],
        "guidance": ["national-source registry required"],
        "status": "reference-pattern-only",
    },
    "VN": {
        "name": "Vietnam",
        "interop": ["FHIR-capable adapters", "IPS export/import", "local-system connector pack"],
        "trust": ["local issuer verification required", "future WHO/GDHCN-compatible trust boundary"],
        "guidance": ["national-source registry required"],
        "status": "future-country-pack",
    },
    "GLOBAL": {
        "name": "Global portability",
        "interop": ["HL7 FHIR", "International Patient Summary", "international terminology mappings"],
        "trust": ["digital signatures", "issuer provenance", "WHO/GDHCN-compatible trust boundary"],
        "guidance": ["receiving-jurisdiction policy always applies"],
        "status": "architecture+synthetic-contract",
    },
}

LANGUAGE_PACKS = {
    "de": {"name": "Deutsch", "status": "primary"},
    "en": {"name": "English", "status": "scaffold"},
    "vi": {"name": "Tiếng Việt", "status": "scaffold"},
}

AUDIENCE_PACKS = {
    "clinician": {"name": "Clinician", "rule": "show clinical context needed for care"},
    "patient_family": {"name": "Patient & Family", "rule": "plain language + permissions; planned V10"},
    "payer": {
        "name": "Payer / Care Coordination",
        "rule": "minimum necessary data only; no default access to clinical ePA contents; patient consent / legal purpose required",
    },
}


def architecture_manifest():
    return {
        "countries": COUNTRY_PACKS,
        "languages": LANGUAGE_PACKS,
        "audiences": AUDIENCE_PACKS,
        "composition": "CareOS Core + Specialty Pack + Country Pack + Language Pack + Audience View",
        "global_rule": "country policy and trust may vary; clinical state/provenance must not silently degrade across packs",
    }
