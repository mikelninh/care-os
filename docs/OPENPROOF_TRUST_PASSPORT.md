# CareOS × OpenProof — Trust Passport MVP

## Goal

Prove a narrow set of workflow trust conditions without copying the underlying professional credentials, governance files or clinical context into every participating system.

A Trust Passport answers:

> **Are the declared trust conditions for this exact workflow currently satisfied?**

It does **not** answer:

- is a diagnosis correct?
- is a treatment appropriate?
- is this patient safe to discharge?
- is this clinician universally authorised?
- has a regulator approved CareOS?

## Golden proof

```text
private professional + governance credentials
        ↓
OpenProof / future Midnight prover
        ↓
licence active              ✓
role authorised             ✓
required consent valid      ✓
privacy review current      ✓
security review current     ✓
credential current          ✓
        ↓
workflow-bound Trust Passport
        ↓
CareOS policy gate / human review
```

No patient record, diagnosis, medication, note or raw credential document belongs in the public proof.

## Current implementation

`app/openproof_trust_passport.py` provides:

- OpenProof `0.1` public envelope;
- purpose binding (`careos.trust-passport`);
- workflow/hospital scope commitment;
- SHA-256 private-witness commitment;
- six explicit trust predicates;
- zero raw disclosures;
- fail-closed verification;
- explicit clinical-authority and data boundaries.

`tests/test_openproof_trust_passport.py` checks:

- positive synthetic trust state;
- no leakage of clinician name, licence number, internal review notes or deliberately injected synthetic patient context;
- missing consent -> `REVIEW_REQUIRED`;
- expired credential -> reject;
- different workflow scope -> reject;
- any raw disclosure -> reject.

The deliberately injected synthetic patient context in the test is a leakage canary only. **Production callers must not put PHI into the Trust Passport witness at all.**

## Security truth

`careos-trust-local-v0` is not a zero-knowledge backend. It is an integration and privacy-surface prototype that demonstrates the application can consume predicate proofs instead of raw credentials.

Production should replace it with issuer-bound credentials and a Midnight Compact circuit that:

1. verifies the credential issuer / attestation signature;
2. binds the subject and exact workflow scope;
3. evaluates trust predicates privately;
4. binds expiry, policy version and replay protection;
5. discloses only the minimum proof result;
6. leaves clinical truth and clinical authority in their authoritative systems and humans.

## PHI rule

> **Midnight/OpenProof is a proof rail around CareOS, never the clinical record.**

Patient data remains in approved clinical systems / governed CareOS context paths. A cryptographic proof may establish consent, role, credential freshness or approval state without moving the underlying record on-chain.

## Graduation gates

- compile/test the Compact predicate scaffold with the pinned Midnight toolchain;
- add trusted issuer verification in-circuit;
- prove no raw witness value reaches ledger/indexer-visible state;
- add revocation + expiry + replay/nullifier tests;
- bind approval receipts to exact workflow/scope/version;
- independent privacy/security review;
- clinician/hospital shadow testing with synthetic or approved deidentified data before any PHI production path.
