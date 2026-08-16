# CareOS SJK Infektiologie — 5-minute synthetic team test

> Synthetic product research only. No real patient data. Do not paste, type, photograph or discuss identifiable patient information in the demo.

## Facilitator rule

**Do not explain how CareOS works before the test.**

Give the participant the browser link and read only:

> „Das ist ein synthetischer infektiologischer Fall. Stell dir vor, du willst dich kurz vor der Visite orientieren. Benutze die Seite so, wie du es intuitiv machen würdest.“

Start the timer.

## Tasks

### 1 — Current microbiology
Ask:
> „Was wissen wir mikrobiologisch schon sicher, und was ist noch offen?“

Record:
- correct / partly / incorrect;
- seconds;
- did they open a source?;
- did they confuse preliminary/pending with final/negative?

### 2 — Documented anti-infective
Ask:
> „Welches Antiinfektivum ist aktuell dokumentiert?“

Record seconds + whether the participant interprets the display as a recommendation. If yes, that is a UX safety failure.

### 3 — Open work
Ask:
> „Welche drei Dinge dürfen heute nicht verloren gehen?“

Record missed pending items.

### 4 — Provenance
Ask:
> „Woher kommt der mikrobiologische Befund?“

Record whether source access is discoverable without coaching.

### 5 — Handover
Ask:
> „Bereite eine kurze Übergabe vor.“

Record:
- seconds;
- corrections the participant would make;
- information they believe is missing;
- information they would remove.

## Structured observer sheet

Use `pilot/sjk_team_test_template.csv`. It deliberately uses participant codes rather than names and its aggregate report ignores free-text notes.

Core fields:

| Metric | Result |
|---|---|
| Participant code | P01 etc. |
| Role / seniority band | |
| Device/browser | |
| Total task time | seconds |
| Microbiology correct? | yes / no |
| Pending status correct? | yes / no |
| Documented therapy correct? | yes / no |
| Source found? | yes / no |
| Handover time | seconds |
| Wrong answers | count |
| Pending items missed | count |
| Source opens | count |
| Corrections | count |
| Needed coaching? | yes / no |
| Effort | 1 / 2 / 3 / 4 / 5 |
| Would use tomorrow? | yes / no |

Do not collect participant names by default. Do not put patient information into the notes column.

### Aggregate the test reproducibly

```bash
python scripts/summarize_sjk_pilot.py pilot/sjk_team_test_results.csv --output data/sjk_team_test_report.json
```

The report contains only structured aggregates such as median time, task correctness, missed-pending-item burden, source discovery, coaching, corrections, effort and would-use-tomorrow. It does **not** automatically declare the pilot a success; observed safety flags remain a human go/no-go decision.

## Six questions after the test

1. **Welche fünf Informationen brauchst du vor fast jeder Visite sofort?**
2. **Wo suchst du dafür heute — und in wie vielen Systemen?**
3. **Wobei telefonierst, wartest oder läufst du Informationen hinterher?**
4. **Was auf diesem Bildschirm würdest du löschen?**
5. **Was fehlt so sehr, dass du CareOS sonst nicht öffnen würdest?**
6. **Was dürfte CareOS auf keinen Fall automatisch entscheiden oder zusammenfassen?**

## Evidence bar before talking integration

The synthetic test has earned an IT conversation when:
- most participants understand the core screen without training;
- pending/preliminary/final status is not systematically misunderstood;
- provenance/source access is discoverable;
- participants identify at least one frequent, costly current information-hunt that the design could remove;
- there is no strong signal that the UI increases correction or cognitive burden.

This is deliberately not a clinical-performance claim. It only determines whether the workflow hypothesis deserves technical integration work.

## Immediate stop/redesign signals

- any participant reads documented treatment as a CareOS treatment recommendation;
- pending is interpreted as negative/complete;
- users trust summary text without understanding how to inspect the source;
- important open work is less visible than in the current workflow;
- the primary reaction is „noch ein System, in dem ich suchen muss“.
