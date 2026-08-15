# Ethical Monetization Agent

CareOS should be economically sustainable **because it creates measurable value**, not because patient data is commercially exploitable.

The agent exists to keep commercial exploration out of the founder's main product loop while preserving explicit human approval for consequential business decisions.

## Red lines

- never sell or broker identifiable/re-identifiable patient data;
- never put safety-critical patient information behind a usage/paywall mechanic;
- never optimise for unnecessary tests, treatment, admissions or referrals;
- never let sponsor/payment relationships influence clinical ranking or recommendations;
- never claim savings/outcomes that have not been measured;
- never give payers an unrestricted mirror of the clinician record.

## Agent loop

```text
market / reimbursement / grant / partner signal
                    ↓
             buyer identified?
                    ↓
           measurable value?
                    ↓
          ethical incentives aligned?
                    ↓
         legal / procurement path?
                    ↓
         smallest evidence experiment
                    ↓
          HUMAN COMMERCIAL APPROVAL
```

## Preferred early models

1. **Hospital workflow pilot** → fixed pilot fee, then platform/integration fee if useful.
2. **Practice/MVZ subscription** → simple per-site pricing, not per clinical event.
3. **Public-interest/grant pilots** → interoperability, patient-access and evaluation work where it accelerates evidence without product drift.
4. **Payer care-coordination programme** → later, purpose-bound minimum dataset and measured coordination/outcome value; never default access to clinical records.

The API manifest is available at `/api/monetization/ethical-agent`.
