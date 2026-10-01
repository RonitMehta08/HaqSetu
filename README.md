# HaqSetu — evidence-first benefits navigation for Bharat

HaqSetu is a working **Citizen & GovTech** agent prototype for Bharat Agentic
2026. It turns a citizen's broad profile and natural-language need into a
ranked, source-linked screening report. The report exposes the evidence for
each signal, shows what is still unknown, and proposes a cautious next step.

> **Important:** HaqSetu is a preliminary screening aid, not an eligibility
> adjudicator. Official government portals and departments remain authoritative.
> It never asks for Aadhaar, OTPs, bank passwords, or document numbers, and it
> never submits an application.

## Why this can score well

The prototype makes the agent loop visible rather than presenting a chat box:

```text
Understand profile → Retrieve relevant schemes → Test rules → Attach evidence
→ Surface counterfactuals → Plan next steps → Ask for consent before drafting
```

### Stand-out feature: the Evidence + Counterfactual Ledger

Every ranked scheme carries:

1. the official source URL and source freshness warning;
2. rule-by-rule `matched`, `not_matched`, or `missing` evidence;
3. a bounded **what could change the result?** signal;
4. a consent gate before a local draft checklist is prepared.

This prevents the most damaging failure mode in public-benefit assistants:
confidently telling someone that they are approved when the decision belongs to
an official process.

## Repository map

| Path | Purpose |
| --- | --- |
| `backend/` | FastAPI API, deterministic agent services, rule engine, bilingual copy |
| `data/schemes.json` | Seven source-linked scheme records and screening rules |
| `frontend/` | Responsive, bilingual, low-bandwidth judge-facing demo UI |
| `tests/test_agent.py` | Safety, API, determinism, and rule-engine tests |
| `evaluation/` | Realistic anonymised test personas and expected retrieval signals |
| `scripts/run_eval.py` | Reproducible rubric-oriented evaluation harness |
| `docs/` | Research, architecture, pitch, demo script, metrics, and source notes |
| `RUNBOOK.md` | Exact manual commands for setup, demo, Docker, and optional GPU work |
| `agent-manifest.yaml` | YAML submission manifest for the Docker/API route |
| `Dockerfile` | Single-container API + static frontend deployment |

## Fastest local demo

Requirements: Python 3.11+, PowerShell on Windows, and a browser.

Run these commands from the repository root:

```powershell
Set-Location D:\bharat_agentic_ai
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python -m uvicorn backend.main:app --reload --port 8000
```

Open <http://127.0.0.1:8000>. The same process serves the UI and the API.
Swagger is at <http://127.0.0.1:8000/docs>.

The health endpoint is `/api/health`, not `/health`:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/health
```

Click **Small farmer**, **Street vendor**, **Senior citizen**, or **Student**,
then **Analyze my options**. Toggle **हिं** to demonstrate bilingual output and
expand rule evidence on any scheme card.

## API contract

```http
GET  /api/health
GET  /api/schemes?language=en|hi
POST /api/analyze
POST /api/feedback
```

PowerShell example:

```powershell
$body = @{ demo = "farmer" } | ConvertTo-Json -Compress
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/analyze" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

The response contains `intake`, `retrieved_schemes`, `eligibility_evidence`,
`missing_facts`, `counterfactuals`, `action_plan`, `citations`,
`consent_required`, `readiness_score`, and time-saving telemetry.

## Tests and evaluation

```powershell
python -m pytest tests\test_agent.py -q
python scripts\run_eval.py
```

The evaluation harness uses anonymised but realistic personas, not fabricated
approval outcomes. It measures retrieval hit rate, citation coverage, schema
completeness, deterministic repeatability, and safety-language compliance.
The judge-facing interpretation is documented in `docs/evaluation.md`.

## Docker/API submission

Docker is optional for local development. Install and start Docker Desktop
before using these commands:

```powershell
Set-Location D:\bharat_agentic_ai
docker build -t haqsetu:demo .
docker run --rm -p 8000:8000 haqsetu:demo
```

Or:

```powershell
docker compose up --build
```

The manifest is `agent-manifest.yaml`. Before submission, replace the local
demo URL with the publicly reachable endpoint required by the organiser's
submission flow and verify `GET /api/health` from outside the laptop. If
PowerShell reports that `docker` is not recognized, Docker Desktop is not
installed or is not available on PATH; the native Python setup above does not
require Docker.

## GPU note for an RTX 4050 laptop

No model training is required for the contest demo. The deterministic path is
deliberate: it is fast, reproducible, cheap, and easy to audit. An RTX 4050 is
useful only for optional local upgrades such as OCR or a local language-model
paraphrase layer; those upgrades must not replace the evidence/rule layer.
See `RUNBOOK.md` for an optional Ollama/llama.cpp path and memory-conscious
settings. Do not spend hackathon time training a model unless a new dataset,
licence, and evaluation plan are available.

## Responsible deployment boundary

The included catalogue is a curated prototype snapshot. Rules, deadlines,
documents, state implementation, and portal availability can change. A
production version should add signed source snapshots, a scheduled freshness
checker, localisation review, a human facilitator mode, consent receipts, and
an audited connector to the official discovery/application channels.
