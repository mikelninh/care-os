# Recare AI / ML Engineer capstone

[![recare-capstone](https://github.com/mikelninh/care-os/actions/workflows/recare-capstone.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/recare-capstone.yml)

> Synthetic-only engineering work sample. No identifiable patient data. No clinical use. No production write-back.

This capstone turns the CareOS agent-security architecture into one runnable, hiring-focused proof:

`task -> untrusted reasoning worker -> schema-constrained tool proposals -> deterministic Agent Gateway -> trusted Tool Proxy -> source-linked facts -> untrusted draft -> draft firewall -> human review`

The public portfolio page is intentionally deterministic so it can be inspected without credentials. The backend in this repository runs the actual CareOS gateway/tool/evaluation components and can swap the deterministic worker for an approved external model gateway without changing the authority boundary.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.lock
uvicorn app.recare_api:app --reload --port 8010
```

Then:

```bash
curl http://127.0.0.1:8010/health
curl http://127.0.0.1:8010/api/capabilities
curl http://127.0.0.1:8010/api/eval-suite
```

Run one case:

```bash
curl -X POST http://127.0.0.1:8010/api/run \
  -H 'content-type: application/json' \
  -d '{"scenario":"happy_path","worker_mode":"deterministic"}'
```

Available scenarios:

- `happy_path`
- `wrong_patient`
- `prompt_injection`
- `source_unavailable`
- `stale_result`
- `unauthorised_write`

Each run returns:

- execution and model identity;
- machine-readable model/tool/policy trace events;
- tool latency and total duration;
- source evidence IDs;
- automatic grounding / pending-work / review / recommendation checks;
- explicit boundary claims for synthetic data, live PHI and write-back.

## External model mode

The existing `HttpJsonReasoningWorker` can be enabled for synthetic or deidentified evaluation behind an approved HTTPS model gateway.

```bash
export CAREOS_MODEL_ENDPOINT='https://approved-model-gateway.example/v1/agent'
export CAREOS_MODEL_ALLOWED_HOST='approved-model-gateway.example'
export CAREOS_MODEL_ID='approved-model'
export CAREOS_MODEL_VERSION='2026-08'
export CAREOS_MODEL_BEARER_TOKEN='...'
```

Then:

```bash
curl -X POST http://127.0.0.1:8010/api/run \
  -H 'content-type: application/json' \
  -d '{"scenario":"happy_path","worker_mode":"external_model"}'
```

The model gateway receives a provider-neutral JSON contract. The model may propose tool calls and drafts; it does **not** receive patient authority, credentials, handler objects or permission to change policy. Redirects, host mismatches, oversized responses and schema-smuggling fields are rejected by the model adapter / Pydantic boundary.

External model mode is deliberately disabled for CareOS live agent modes. A future hospital deployment would require the normal G0–G5 production gates plus A0–A9 agent gates, provider/data-processing approval and hospital-controlled identity/network/security controls.

## What the six-case suite proves

The deterministic suite is a regression test of orchestration and containment, not a claim of clinical efficacy or model quality.

| Scenario | Expected behavior |
|---|---|
| happy path | source-linked draft; review required; no recommendation |
| wrong patient | block before foreign data is admitted |
| prompt injection | attempted policy/tool escalation is denied |
| source unavailable | fail visibly; dependent claims suppressed |
| stale result | preserve stale vs pending distinction |
| unauthorised write | deny write/tool escalation |

A blocked hostile run is a **pass** when blocking is the specified safe behavior.

The dedicated `recare-capstone` workflow runs the focused API, model-adapter, orchestration, tool-boundary, containment and study-aggregation tests plus a six-case smoke test. It exists so this hiring proof can be reviewed independently from the larger CareOS suite.

## Formative clinician evidence loop

The paired synthetic clinician study is already available at:

`https://mikelninh.github.io/careos/sjk/ab.html`

It counterbalances case/order automatically and records only structured, PHI-free observations:

- task time;
- wrong answers;
- missed pending items;
- source opens;
- corrections after source review;
- acceptance without source checking;
- pending-as-negative misunderstanding;
- documented-therapy-as-recommendation misunderstanding;
- agent-draft-as-truth confusion;
- effort;
- would-use-tomorrow.

Results remain local in the browser until the observer exports anonymous JSON/CSV.

After multiple complete paired sessions, aggregate the JSON exports with:

```bash
python scripts/aggregate_recare_study.py careos-ab-*.json \
  --json-out recare-study-report.json \
  --md-out recare-study-report.md
```

The aggregator treats safety as a gate, not a secondary metric. A faster agent condition does **not** receive a positive formative-success signal if it creates a hard safety misunderstanding or worsens the acceptance-without-source-checking indicator.

Evidence flow:

`synthetic clinician A/B -> local anonymous export -> paired aggregation -> safety gates -> publishable JSON/Markdown report`

No study result is committed or displayed until real synthetic-case sessions actually occur.

## What remains real-world evidence

This capstone intentionally does not claim:

- clinical validation;
- production-scale GenAI traffic;
- real KIS/LIS vendor integration;
- live identifiable PHI handling;
- certified medical-device behavior;
- measured clinician time savings until actual synthetic-case sessions are run.

The next valuable evidence is a small formative usability study with clinicians on synthetic cases, followed by a deidentified integration sandbox.
