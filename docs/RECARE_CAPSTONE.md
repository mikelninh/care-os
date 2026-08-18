# Recare AI / ML Engineer capstone

[![recare-capstone](https://github.com/mikelninh/care-os/actions/workflows/recare-capstone.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/recare-capstone.yml)

> **Synthetic-only engineering work sample.** No identifiable patient data. No clinical use. No production write-back.

This capstone turns the CareOS agent-security architecture into one runnable proof:

`task → untrusted reasoning worker → schema-constrained tool proposal → deterministic Agent Gateway → trusted Tool Proxy → source-linked facts → untrusted draft → draft firewall → human review`

The public portfolio page is deterministic so anyone can inspect it without credentials. The repository backend runs the actual CareOS policy/tool/evaluation path and supports three reasoning-worker modes **without changing the authority boundary**:

1. `deterministic` — reproducible default / CI;
2. `external_model` — provider-neutral approved HTTPS model gateway;
3. `openai_responses` — direct OpenAI Responses API adapter for synthetic evaluation.

The model never becomes the authority in any of these modes.

---

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

Run one deterministic case:

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

- execution / worker / model identity;
- machine-readable model, policy and tool trace events;
- tool latency + total duration;
- source evidence IDs;
- automatic grounding / pending-work / human-review / recommendation checks;
- token counts where exposed by a configured provider;
- explicit synthetic/live-PHI/write-back boundary claims.

---

## Direct OpenAI Responses mode

`OpenAIResponsesReasoningWorker` is an **optional synthetic-only provider adapter**.

It uses:

- the official Responses API endpoint;
- strict JSON-Schema structured output;
- `store: false`;
- bounded request/response sizes;
- redirect denial;
- no direct access to CareOS tools;
- no model-controlled patient/encounter scope;
- no model-controlled egress/write/break-glass authority.

Configure locally:

```bash
export OPENAI_API_KEY='...'
export CAREOS_OPENAI_MODEL='gpt-5.6'
export CAREOS_OPENAI_MODEL_VERSION='gpt-5.6'
```

Then run:

```bash
curl -X POST http://127.0.0.1:8010/api/run \
  -H 'content-type: application/json' \
  -d '{"scenario":"happy_path","worker_mode":"openai_responses"}'
```

The provider only proposes tool requests and a draft. `bind_tool_proposal()` injects the authoritative delegated patient/encounter context, then the deterministic `AgentGateway` and `AgentToolProxy` decide whether any call is admitted.

A provider failure, malformed structured output, policy violation or unsafe draft **fails closed**.

### Capture a reproducible provider-backed proof

Do not screenshot a terminal and call that evidence. Use the capture script:

```bash
python scripts/capture_recare_model_run.py \
  --worker openai_responses \
  --scenario happy_path \
  --out artifacts/recare-provider-backed-run.json
```

The artifact records:

```text
captured timestamp
synthetic-only claim boundary
model + version
execution status
model / policy / tool trace
evidence IDs
eval result
latency
token usage when available
```

**Important:** no provider-backed result is claimed until this command has actually run with a real credential. A deterministic/mock run is not relabelled as a real model run.

---

## Provider-neutral external model mode

The existing `HttpJsonReasoningWorker` remains available when a hospital/company has an approved HTTPS model gateway.

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

The generic gateway receives a provider-neutral JSON contract. Redirects, host mismatches, oversized responses and schema-smuggling fields are rejected before output can influence the CareOS policy boundary.

Both provider-backed modes remain disabled for live CareOS agent modes. A hospital deployment would still require the normal production/agent gates plus provider/data-processing approval and hospital-controlled identity, network and security operations.

---

## What the six-case suite proves

The deterministic suite is a regression test of **orchestration and containment**, not clinical efficacy or model quality.

| Scenario | Expected behavior |
|---|---|
| happy path | source-linked draft; review required; no recommendation |
| wrong patient | block before foreign data is admitted |
| prompt injection | attempted policy/tool escalation is denied |
| source unavailable | fail visibly; dependent claims suppressed |
| stale result | preserve stale vs pending distinction |
| unauthorised write | deny write/tool escalation |

A blocked hostile run is a **pass** when blocking is the specified safe behavior.

The dedicated `recare-capstone` workflow runs focused API, direct-provider-adapter, provider-neutral-adapter, orchestration, tool-boundary, containment and study-aggregation tests plus the six-case smoke suite.

---

## Formative clinician evidence loop

The paired synthetic clinician study is available at:

`https://mikelninh.github.io/careos/sjk/ab.html`

It counterbalances case/order and records only structured, PHI-free observations:

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

Results remain local until the observer exports anonymous JSON/CSV.

Aggregate multiple complete paired sessions with:

```bash
python scripts/aggregate_recare_study.py careos-ab-*.json \
  --json-out recare-study-report.json \
  --md-out recare-study-report.md
```

The aggregator treats safety as a gate. Faster is **not** a positive result when verification degrades or a hard safety misunderstanding appears.

---

## What remains real-world evidence

This capstone intentionally does **not** claim:

- clinical validation;
- production-scale GenAI traffic;
- real KIS/LIS vendor integration;
- live identifiable PHI handling;
- certified medical-device behavior;
- measured clinician time savings before real synthetic-case sessions;
- production security maturity equivalent to a real hospital platform.

The next valuable evidence after the optional provider-backed synthetic run is external: clinician behaviour, real workflow observation and a governed deidentified integration sandbox.
