# Interactive testing configuration

HaqSetu is ready for a buyer-testing form that sends JSON to an HTTP endpoint.
Deploy the container behind a public HTTPS host first; the repository does not
contain credentials or a hosting account.

## Form values

| Field | Value |
| --- | --- |
| Testing mode | API |
| API endpoint mode | Yes |
| Endpoint URL | `https://YOUR_PUBLIC_HOST/v1/run` |
| HTTP method | `POST` |
| Authentication | No authentication |
| Input encoding | JSON body |
| Response | JSON response |
| Session request | No |

The endpoint is deterministic and does not require an API key. It accepts either
a demo selector or a full profile. For the simplest buyer test, use:

```json
{
  "demo": "farmer"
}
```

For a real screening profile, send:

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

## Suggested input fields

Add these fields to the buyer form (all are JSON body properties):

1. `state` — string, required
2. `age` — number, required
3. `occupation` — string, required
4. `monthly_income` — number, required
5. `social_category` — string, required
6. `landholding` — number, optional, default `0`
7. `disability` — boolean, optional, default `false`
8. `needs` — array of strings, optional
9. `language` — `en` or `hi`, optional, default `en`

Do not collect Aadhaar, OTPs, bank passwords, document numbers, or credentials.

## Suggested response mapping

If the form supports field mapping, expose:

- `trace.retrieved_schemes`
- `trace.eligibility_evidence`
- `trace.missing_facts`
- `trace.action_plan`
- `trace.citations`
- `trace.readiness_score`
- `disclaimer`

The full JSON response is safe to show for initial testing. It is a screening
report only; official portals and departments decide eligibility.

## Smoke test after deployment

```powershell
curl.exe -X POST https://YOUR_PUBLIC_HOST/v1/run `
  -H "Content-Type: application/json" `
  -d '{"demo":"farmer"}'
```

The host must also return HTTP 200 from `GET /api/health` before publishing the
endpoint URL to buyers.
