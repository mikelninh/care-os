# Payer / care-coordination view (architecture)

CareOS must not expose a full clinician record to a Krankenkasse by default.

A future payer view should be purpose-bound and data-minimised, for example:
- insurance/eligibility state;
- authorised care-plan or case-management status;
- discharge/transition milestones where legally permitted;
- approved follow-up completion signals;
- patient-consented additional-app data;
- aggregated outcome/quality metrics;
- duplicated-process and coordination indicators without unnecessary clinical narrative.

Every field needs a provenance + legal/purpose basis + audience policy. Patient-facing consent and revocation should be first-class where consent is the basis.
