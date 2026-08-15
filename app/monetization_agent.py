from dataclasses import dataclass, asdict

ETHICAL_RED_LINES = [
    "No sale or brokerage of identifiable or re-identifiable patient data.",
    "No paywall around safety-critical patient information or core patient access.",
    "No incentives that reward unnecessary tests, treatment, admissions, or referrals.",
    "No opaque referral fees or ranking influenced by commercial relationships.",
    "No monetization that weakens clinical independence or patient consent.",
    "No pricing claim based on unmeasured time savings or clinical outcomes.",
]

VALUE_METRICS = [
    "measured clinician admin minutes saved",
    "fewer phone/fax retrieval steps",
    "fewer duplicated administrative processes",
    "faster safe discharge / transition workflows",
    "fewer documentation corrections",
    "lower cognitive effort without increased safety risk",
]

@dataclass(frozen=True)
class RevenueModel:
    id: str
    buyer: str
    model: str
    alignment: str
    evidence_needed: list[str]
    ethical_risks: list[str]
    stage: str

MODELS = [
    RevenueModel(
        id="hospital-pilot",
        buyer="Hospital / hospital group",
        model="Fixed-price workflow pilot, then annual platform + integration fee tied to enabled sites/workflows rather than patient volume.",
        alignment="Hospital pays when CareOS removes measurable administrative burden and integrates safely.",
        evidence_needed=["baseline vs CareOS time", "correction/error rate", "clinician adoption", "security/integration readiness"],
        ethical_risks=["automation pressure must not override clinician judgement", "avoid pricing incentives tied to more clinical activity"],
        stage="now",
    ),
    RevenueModel(
        id="practice-subscription",
        buyer="Practice / MVZ",
        model="Low-friction per-site subscription with optional connector fees; core patient access never metered.",
        alignment="Simple SaaS economics for admin reduction without monetising sensitive data.",
        evidence_needed=["time saved per practice", "integration/support cost", "retention"],
        ethical_risks=["do not gate safety-critical information by seat or usage"],
        stage="after clinician validation",
    ),
    RevenueModel(
        id="payer-coordination",
        buyer="Krankenkasse / payer",
        model="Purpose-bound care-coordination or outcomes pilot using minimum-necessary data; pricing based on programme/service value, not access to clinical records.",
        alignment="Payer funds coordination improvements that can be measured without gaining unrestricted clinical-record access.",
        evidence_needed=["legal/purpose basis", "patient consent where applicable", "transition/follow-up metrics", "cost/outcome evidence"],
        ethical_risks=["payer incentives must not steer individual treatment", "no clinical-record resale or default access"],
        stage="later pilot",
    ),
    RevenueModel(
        id="public-interest",
        buyer="Public programmes / grants / research consortia",
        model="Grant-funded interoperability, evaluation, patient-access, or cross-border pilots with publishable methodology.",
        alignment="De-risks public infrastructure and evidence generation without extracting value from patients.",
        evidence_needed=["clear public-benefit hypothesis", "evaluation protocol", "open standards contribution"],
        ethical_risks=["avoid grant-driven feature drift"],
        stage="now-if-non-distracting",
    ),
]


def monetization_manifest():
    return {
        "mission": "Make CareOS financially sustainable only where revenue aligns with more time for care, safer coordination, patient agency, and measurable utility.",
        "red_lines": ETHICAL_RED_LINES,
        "value_metrics": VALUE_METRICS,
        "models": [asdict(x) for x in MODELS],
        "founder_focus_rule": "Do not distract product/customer work unless an opportunity has a named buyer, clear next experiment, and evidence path.",
    }
