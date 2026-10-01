# Interactive testing configuration

HaqSetu exposes a public, deterministic, unauthenticated JSON endpoint at
`POST /v1/run`. That is everything the buyer-testing form needs: no API key, no
session handshake, and no streaming.

The repository ships two deployment paths. Both serve the identical contract.

| | Vercel (`vercel.json`) | Render (`render.yaml`) |
| --- | --- | --- |
| Runtime | Python serverless function | Docker container |
| Cold start | ~300 ms | ~50 s after 15 min idle |
| Free tier | Hobby, **non-commercial use only** | Free, sleeps when idle |
| Best for | Buyer testing, live demos | Container-parity submissions |

**Recommended: Vercel.** The marketplace's *Test Endpoint* button and impatient
buyers both time out on a sleeping Render free service. Vercel's cold start is
fast enough that the first request simply works.

**Licensing caveat you must decide on.** Vercel's Hobby plan is licensed for
personal, non-commercial use. Demoing a hackathon prototype is fine; actively
selling the product through a marketplace is commercial use and needs Vercel Pro
($20/mo). If you want a free tier with no commercial restriction, deploy the
existing `Dockerfile` to Hugging Face Spaces or Google Cloud Run instead — both
reuse the container unchanged and neither sleeps per request.

## Deploy to Vercel

```bash
npx vercel --prod
```

Or from the dashboard: **Add New → Project**, import
`RonitMehta08/HaqSetu`, leave every build setting at its default, and deploy.
`vercel.json` already routes all traffic to `api/index.py` and bundles the
`data/` catalogue and `frontend/` assets into the function.

No environment variables are required. `ALLOWED_ORIGINS` defaults to `*`, which
is appropriate here because the endpoint accepts no credentials and sets no
cookies. Set it to a comma-separated origin list if you later want to restrict
browser access.

## Deploy to Render (fallback)

1. Sign in at <https://dashboard.render.com/> with the GitHub account that can
   access `RonitMehta08/HaqSetu`.
2. Choose **New → Blueprint**, select this repository and the `main` branch.
3. Review the `haqsetu` web service from `render.yaml` and click **Apply**.
4. Wait for the deploy to go live, then verify `GET /api/health`.

Render's free plan sleeps after 15 minutes idle. Use the Starter plan if buyers
need consistently warm responses.

## Verify before publishing the URL

Both checks must pass against the deployed host.

```bash
curl https://YOUR_PUBLIC_HOST/api/health
```

```bash
curl -X POST https://YOUR_PUBLIC_HOST/v1/run -H "Content-Type: application/json" -d "{\"demo\":\"farmer\"}"
```

Health must return HTTP 200 with `status: ok`, `demo_mode: true`, and
`live_integrations: false`. The run call must return a `trace` object containing
`retrieved_schemes` and `citations`.

## Form values

| Form field | Value |
| --- | --- |
| Interactive Testing | **API** |
| API Endpoint Mode | **Yes** |
| Endpoint URL | `https://YOUR_PUBLIC_HOST/v1/run` |
| HTTP method | **POST** |
| Authentication | **No authentication** |
| How should aiKart send the inputs? | **JSON body** |
| How does your endpoint respond? | **JSON response** |
| Internal request fields | *leave empty* |
| Needs a session request first | **No** |

There is no `engine_name` or other internal field to inject, so leave the
internal-request-fields JSON blank.

## Input fields

Nine fields, within the 15-field limit. Names must match exactly; they are the
JSON body keys.

| # | Name | Type | Required | Example / default |
| --- | --- | --- | --- | --- |
| 1 | `state` | text | Yes | `Bihar` |
| 2 | `age` | number | Yes | `42` |
| 3 | `occupation` | text | Yes | `small farmer` |
| 4 | `monthly_income` | number | Yes | `12000` |
| 5 | `social_category` | text | Yes | `OBC` |
| 6 | `landholding` | number | No | `0` |
| 7 | `disability` | boolean | No | `false` |
| 8 | `needs` | text | No | `income support, crop insurance` |
| 9 | `language` | text | No | `en` |

Notes for whoever fills the form:

- `social_category` accepts `General`, `OBC`, `SC`, `ST`, `EWS`, or `Minority`.
  Use a dropdown if the form supports one.
- `needs` accepts either a comma-separated string or a JSON array. The API
  normalises both.
- `language` accepts only `en` or `hi`.
- Optional fields may be submitted blank; the API falls back to the defaults
  above rather than erroring.
- `name` is deliberately **not** exposed. The rule engine never uses it and it
  is excluded from logs, so there is no reason to collect it from buyers.
- Do not add fields for Aadhaar, OTPs, bank details, document numbers, or any
  credential. The endpoint neither needs nor accepts them.

A minimal body that exercises the full trace:

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

For the quickest possible smoke test, `{"demo": "farmer"}` also works and
returns a fixed, repeatable report. Valid demo keys are `farmer`, `vendor_hi`,
and `senior`.

## What buyers see in the result

Map these response paths. The first three carry most of the product's value, so
order them that way if the form preserves order.

| Response path | Suggested label |
| --- | --- |
| `trace.readiness_score` | Screening readiness (%) |
| `trace.retrieved_schemes` | Matched schemes |
| `trace.eligibility_evidence` | Rule-by-rule evidence |
| `trace.missing_facts` | Facts still to verify |
| `trace.counterfactuals` | What could change the result |
| `trace.action_plan` | Recommended next steps |
| `trace.citations` | Official sources |
| `trace.consent_required` | Consent required before acting |
| `trace.estimated_time_saved` | Estimated time saved |
| `disclaimer` | Important disclaimer |

Always map `disclaimer`. The response is a preliminary screening report, and
`readiness_score` is a completeness indicator, **not** a probability of
approval. Official portals and departments remain the decision-makers.

Leaving the form on *Showing full response* is also safe. The payload contains
no secrets and no personal data beyond what the buyer typed.
