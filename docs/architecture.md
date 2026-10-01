# Architecture

## Runtime flow

```text
Browser / API client
        │
        ▼
FastAPI request boundary ── validation + safe logging
        │
        ▼
Intake normaliser ── profile facts + language + broad needs
        │
        ▼
Transparent retrieval ── keyword/occupation overlap over scheme catalogue
        │
        ▼
Rule engine ── matched / not_matched / missing per rule
        │
        ├── Evidence ledger ── official URL + source freshness warning
        ├── Counterfactual generator ── next fact that could change signal
        └── Action planner ── verify → collect only listed facts → consent gate
        │
        ▼
Structured response ── UI trace, score, citations, checklist draft
```

## Components

| Component | Responsibility | Why it is explicit |
| --- | --- | --- |
| `backend/main.py` | HTTP boundary, validation, static frontend | Stable submission contract. |
| `backend/models.py` | Pydantic input constraints | Reject malformed profiles early. |
| `backend/rules.py` | Safe rule operators and statuses | No hidden LLM eligibility decision. |
| `backend/services.py` | Retrieval orchestration, evidence, plan | One inspectable agent loop. |
| `data/schemes.json` | Scheme cards, rules, sources, caveats | Replaceable knowledge snapshot. |
| `frontend/app.js` | Render trace/report, consent interaction | User sees evidence and control. |
| `scripts/run_eval.py` | Offline regression/evaluation | Prevent demo-only success. |

## Data contract highlights

```json
{
  "analysis_id": "hs-…",
  "mode": "demo",
  "trace": {
    "retrieved_schemes": [],
    "eligibility_evidence": [],
    "missing_facts": [],
    "counterfactuals": [],
    "citations": [],
    "consent_required": true,
    "readiness_score": 68
  }
}
```

`readiness_score` is a bounded screening-completeness indicator. It is not a
probability, confidence of approval, or ranking of human worth.

## Security and privacy controls

- Request model deliberately excludes Aadhaar, OTP, passwords, bank numbers,
  and document images.
- `privacy_safe_log` records only state, age band, language, counts, and score.
- The frontend escapes API-provided strings before rendering HTML.
- External source links use `noopener noreferrer`.
- No network integration is required for the core path.
- No automatic submission tool exists; draft creation requires consent.
- Docker runs as a non-root user and read-only compose mode is provided.

## Scale path

1. Replace JSON with versioned, signed source snapshots and a Postgres/SQLite
   catalogue for provenance.
2. Add BM25/vector hybrid retrieval with multilingual embeddings, then retain a
   deterministic policy/rule layer for final signals.
3. Add a source freshness job and human review queue.
4. Add facilitator workspaces, audit receipts, rate limits, and per-state
   policy packs.
5. Add official connectors only with permissions and a human confirmation step.

The future LLM layer may explain a structured result, but it must not authorise
eligibility or create unsupported sources.
