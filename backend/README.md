# HaqSetu backend

HaqSetu is an evidence-first, multilingual government-benefits screening API
for a hackathon prototype. It is deliberately deterministic and needs **no API
key**. It does not submit applications, call a live government API, or decide
official eligibility.

## Run locally

From the repository root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python -m uvicorn backend.main:app --reload --port 8000
```

The API is at <http://127.0.0.1:8000>; interactive docs are at
<http://127.0.0.1:8000/docs>.

## Endpoints

* `GET /api/health` — service health and explicit `live_integrations: false`.
* `GET /api/schemes?language=en|hi` — the seeded source-linked catalogue.
* `POST /api/analyze` — accepts a bare profile, `{ "profile": { ... } }`, or
  `{ "demo": "farmer" }`, `{ "demo": "vendor_hi" }`, or `{ "demo": "senior" }`.
* `POST /v1/run` — versioned marketplace/buyer-testing alias for `/api/analyze`.
* `POST /api/feedback` — accepts anonymous `rating`, `helpful`, and optional
  short `comment`; feedback is acknowledged for the demo and not persisted.

Example deterministic request:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/analyze `
  -H "Content-Type: application/json" `
  -d '{"demo":"farmer"}'
```

For an external buyer-testing form, use the same body against
`https://<your-public-host>/v1/run` with `Content-Type: application/json` and no
authentication.

Example profile:

```json
{
  "state": "Bihar",
  "age": 42,
  "occupation": "small farmer",
  "monthly_income": 12000,
  "social_category": "OBC",
  "landholding": 1.2,
  "disability": false,
  "needs": ["income support", "crop insurance"],
  "language": "en"
}
```

The analysis trace includes intake, ranked retrieval, rule-by-rule evidence,
missing facts, cautious action steps, official citations, consent guidance,
a bounded readiness/completeness score, and an estimated time-saving note.

## Tests

```powershell
python -m pytest tests\test_agent.py -q
```

## Data and safety notes

Seed data is in `data/schemes.json`; the rule engine is in `backend/rules.py`.
Each source has a URL, a `last_verified` date, and a freshness warning. The
official portal or department is always authoritative because scheme criteria,
deadlines, documents, and state implementation can change.

The logger records only aggregate diagnostics (state, age band, language,
counts, and scores). It intentionally excludes names, income, raw needs, and
credentials. No Aadhaar, OTP, bank password, or other secret should be sent to
this prototype.
