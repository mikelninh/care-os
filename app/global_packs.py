COUNTRY_PACKS = {
    "DE": {"name":"Deutschland","interop":["FHIR R4","ISiK","TI/ePA adapters"],"guidance":["RKI/KRINKO","AWMF/NVL","DGN","Onkopedia"],"status":"active-prototype"},
    "EU": {"name":"EU / cross-border","interop":["FHIR R4","International Patient Summary","MyHealth@EU/EHDS-ready boundary"],"guidance":["EU/national overlays"],"status":"architecture"},
    "VN": {"name":"Vietnam","interop":["FHIR-capable adapters","IPS export/import"],"guidance":["national-source registry required"],"status":"future-country-pack"},
}
LANGUAGE_PACKS = {
    "de": {"name":"Deutsch","status":"primary"},
    "en": {"name":"English","status":"scaffold"},
    "vi": {"name":"Tiếng Việt","status":"scaffold"},
}
AUDIENCE_PACKS = {
    "clinician": {"name":"Clinician","rule":"show clinical context needed for care"},
    "patient_family": {"name":"Patient & Family","rule":"plain language + permissions; planned V10"},
    "payer": {"name":"Payer / Care Coordination","rule":"minimum necessary data only; no default access to clinical ePA contents; patient consent / legal purpose required"},
}

def architecture_manifest():
    return {"countries":COUNTRY_PACKS,"languages":LANGUAGE_PACKS,"audiences":AUDIENCE_PACKS,
            "composition":"CareOS Core + Specialty Pack + Country Pack + Language Pack + Audience View"}
