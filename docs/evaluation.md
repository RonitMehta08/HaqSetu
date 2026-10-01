# Evaluation plan and rubric alignment

## Offline test set

`evaluation/cases.json` contains seven anonymised personas based on common
first-mile questions: farmer, vendor, senior citizen, student, rural housing
need, healthcare need, and a non-match control. They are test fixtures, not real
people and do not encode approval decisions.

## Automated metrics

| Metric | Definition | Why a judge should care |
| --- | --- | --- |
| Retrieval hit rate | Expected scheme appears in top six for each case. | Measures useful discovery. |
| Citation coverage | Every returned scheme has an official URL. | Measures provenance. |
| Evidence coverage | Every returned scheme has rule evidence and a safe status. | Measures agent reasoning. |
| Counterfactual coverage | Cases with an unknown/failed rule surface a bounded what-if prompt. | Demonstrates the unique feature. |
| Schema completeness | Required trace fields are present. | Makes the API dependable. |
| Determinism | Same profile produces byte-equivalent JSON. | Reproducibility under judging. |
| Safety-language coverage | Response contains screening/official-verification boundary and no approval claim. | Reduces harmful overclaiming. |

Run:

```powershell
python scripts\run_eval.py
```

The script prints a compact table and writes `reports/evaluation-results.json`
and `reports/evaluation-results.md`.

## Manual judge checks

1. Change a farmer's landholding to `0`; confirm PM-KISAN is not called an
   official rejection and a counterfactual/verification prompt remains.
2. Leave a relevant fact out; confirm `missing` appears rather than an invented
   value.
3. Toggle Hindi; confirm report copy and source links remain present.
4. Try to prepare a draft without consent; confirm the button is disabled.
5. Enter a name; confirm the report says it is not used for rules and logs do
   not include it.
6. Open a source link; confirm it is an official portal, not an invented route.
7. Use low-data mode; confirm the core form and report remain usable.

## Mapping to the supplied judging criteria

### Agentic capability

Visible intake → retrieval → rule evaluation → evidence → planning trace,
structured actions, and a consent-gated output rather than a single answer.

### Bharat impact

Targets the first mile of public-benefit discovery, supports English/Hindi,
works with broad facts and low bandwidth, and is useful to a facilitator.

### Technical implementation

FastAPI, Pydantic validation, deterministic tool-like modules, source metadata,
tests, Dockerfile, YAML manifest, and an evaluation harness.

### Innovation

Evidence + Counterfactual Ledger and explicit “screening completeness, not
approval probability” design make uncertainty a first-class output.

### UX

Responsive one-screen intake, scenario buttons, timeline, score, citations,
keyboard-safe controls, Hindi switch, low-data mode, and a visible consent gate.

### Scalability and feasibility

No API key or GPU required, replaceable catalogue, stateless API, Docker
deployment, and a credible versioned-source/connector scale path.

### Demo

The 2–3 minute path in `RUNBOOK.md` shows a complete agent trace, evidence,
counterfactual, bilingual mode, and safe action boundary.
