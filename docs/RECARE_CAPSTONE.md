# Recare AI / ML Engineer capstone

[![recare-capstone](https://github.com/mikelninh/care-os/actions/workflows/recare-capstone.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/recare-capstone.yml)

> **For technical reviewers.** This is the local run/API/evaluation guide behind the public Recare browser work sample. If you only want the product story, use the [90-second work sample](https://mikelninh.github.io/recare/). If you want to inspect or run the backend, start here.
>
> **Synthetic-only engineering work sample.** No identifiable patient data. No clinical use. No production write-back.

## What this guide lets you verify

In roughly 5–10 minutes, an engineer can:

1. start the FastAPI capstone locally;
2. inspect the declared capabilities and safety boundaries;
3. run one normal synthetic case;
4. replay wrong-patient, prompt-injection, outage, stale-result and forbidden-write scenarios;
5. inspect machine-readable traces, evidence IDs and automatic eval results.

The capstone turns the CareOS agent-security architecture into one runnable proof:

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

The remainder of this document describes the same synthetic-only capstone and its provider-backed capture path. Production PHI, production write-back and hospital deployment remain outside this work sample.