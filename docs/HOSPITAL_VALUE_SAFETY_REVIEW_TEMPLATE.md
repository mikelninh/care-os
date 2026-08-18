# CareOS Hospital Value + Safety Review

Status: reusable **pilot / future production review template**. Populate only with evidence from the actual deployment period; never substitute synthetic values for hospital outcomes.

## Review header

```text
Hospital/site:
Period:
Workflow(s):
CareOS release:
Adapter/profile versions:
Clinical sponsor:
Hospital IT owner:
CareOS/partner owner:
Safety/privacy/security attendees:
```

---

# 1. Executive decision

Choose one:

- **EXPAND** — benefit is meaningful and safety/verification gates hold;
- **HOLD** — keep current scope while resolving evidence/friction gaps;
- **REDUCE** — narrow workflow/capability;
- **ROLL BACK** — benefit/risk or reliability is unacceptable.

Decision rationale:

```text
...
```

No expansion decision may rely on adoption/time savings alone when a safety-stop condition is unresolved.

---

# 2. Time Returned to Care

For each workflow/role:

| Role / workflow | Baseline | Current | Median time returned | n | Status |
|---|---:|---:|---:|---:|---|
| | | | | | |

Also review where available:

- systems/screens opened;
- searches/context switches;
- copy/paste/manual entry;
- clarification calls/messages/faxes;
- cognitive effort;
- abandonment/reversion to legacy workflow.

Question:

> Did the product remove work, or merely move work into a different screen?

---

# 3. Safety + clinical information quality

| Signal | Count / rate | Trend | Action |
|---|---:|---|---|
| wrong-patient events / near misses | | | |
| missed pending work | | | |
| unsupported surfaced claims | | | |
| stale-as-current confusion | | | |
| source-state / lifecycle errors | | | |
| contradictions not surfaced | | | |
| unauthorised action attempts / denials | | | |
| draft-as-recommendation confusion | | | |
| other safety-stop events | | | |

Any safety-stop event requires explicit disposition before scope expansion.

---

# 4. Verification behaviour

Review:

- source-opening rate for consequential facts;
- acceptance without verification;
- corrections after source inspection;
- user ability to locate original evidence;
- whether easier UI is producing over-trust.

Question:

> Are users faster because context is better, or because they stopped checking things they still need to check?

---

# 5. Reliability / degraded operation

| Capability / dependency | Availability / health | Degraded events | Longest event | Notes |
|---|---:|---:|---:|---|
| provider source access | | | | |
| patient/encounter identity | | | | |
| audit | | | | |
| CareOS context | | | | |
| model/agent assistance | | | | |

Review:

- source freshness breaches;
- offline/degraded mode frequency;
- recovery reconciliation events;
- rollback/kill-switch use;
- user fallback success;
- unresolved dependency risk.

Do not collapse upstream source outages and CareOS process availability into one green percentage.

---

# 6. Integration / scaling economics

Capture:

- engineering hours this period;
- custom site-specific code added;
- configuration/mapping changes;
- adapter/profile reuse;
- conformance tests reused/added;
- vendor upgrades encountered;
- upgrade failures caught pre-production;
- support hours;
- compatibility records created/updated.

Question:

> Is this hospital making the next compatible hospital easier?

---

# 7. User experience

Review by role:

- five-second orientation success;
- task completion friction;
- keyboard/touch/shared-terminal issues;
- accessibility issues;
- confusing terminology/state labels;
- alert burden;
- trust/frustration feedback;
- support questions that should become product self-explanation.

Every recurring user question should be considered for:

- UX improvement;
- inline explanation;
- support-agent knowledge;
- regression/usability test.

---

# 8. Patient / family experience where in scope

Review:

- pending-state comprehension;
- medication-change comprehension;
- follow-up ownership comprehension;
- source-location success;
- proxy/delegation friction;
- correction/error-flag workflow;
- accessibility/language barriers;
- false reassurance/confidence events.

Patient engagement is not sufficient; **understanding** is the target.

---

# 9. Incidents / near misses / learning

For each meaningful incident:

```text
Incident ID:
What happened:
Affected scope:
User/patient risk:
Fallback used:
Containment:
Root cause:
Regression/conformance/runbook change:
Owner:
Due date:
```

Rule:

> A generalisable incident should improve the platform for every future compatible deployment.

---

# 10. Upcoming change risk

Next-period changes:

- KIS/LIS/RIS/PACS/vendor upgrades;
- network/identity changes;
- workflow changes;
- new ward/users;
- terminology/mapping updates;
- model/provider/prompt updates;
- new adapter/release;
- privacy/security/regulatory changes.

For each, define preflight/conformance/canary/rollback requirements.

---

# 11. Actions

| Action | Owner | Evidence required | Due | Blocks expansion? |
|---|---|---|---|---|
| | | | | |

---

# 12. Review cadence

### Pilot / first weeks
Use weekly.

### Stable deployment target
- monthly operations review;
- quarterly value + safety review;
- annual/major-change resilience and governance review as appropriate.

The cadence may be adapted to risk and deployment scope; the **joint review of benefit + safety + verification + reliability must not disappear**.
