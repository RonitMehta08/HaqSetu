# HaqSetu build, demo, and submission runbook

This is the manual command sheet for the team. Run commands from the repository
root in PowerShell.

## 0. What is already built

- FastAPI agent API with deterministic retrieval and rule evaluation.
- Single-page frontend served by the same FastAPI process.
- English/Hindi switch and low-data visual mode.
- Seven official-source-linked scheme records.
- Rule-by-rule evidence, counterfactual prompts, action plan, and consent gate.
- API tests and an evaluation harness with anonymised realistic personas.
- Dockerfile and `agent-manifest.yaml` for the organiser's submission routes.

The build uses the problem, rules, submission checklist, and judging criteria
provided by the hackathon, plus public official sources listed in
`docs/sources.md`.

## 1. Install and run the demo

```powershell
py -3.11 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\\requirements.txt
python -m uvicorn backend.main:app --reload --port 8000
```

Open `http://127.0.0.1:8000` in a browser. Keep this terminal open.

Smoke-test in a second PowerShell window:

```powershell
curl.exe http://127.0.0.1:8000/api/health
curl.exe -X POST http://127.0.0.1:8000/api/analyze `
  -H "Content-Type: application/json" `
  -d '{"demo":"farmer"}'
```

Expected health fields include `status: ok`, `demo_mode: true`, and
`live_integrations: false`.

## 2. Judge demo path (2–3 minutes)

1. Start on the landing page; say: “This is not a chatbot. It is a guarded
   workflow from profile to evidence to a next action.”
2. Choose **Small farmer** and click **Analyze my options**.
3. Point at the live trace: intake → discovery → evidence → plan.
4. Show the readiness score and the three impact metrics.
5. Expand PM-KISAN or PMFBY evidence; point to matched rules, source URL, and
   the explicit “screening only” language.
6. Point to **What could change the result?**. This counterfactual ledger says
   which missing/failed fact should be checked instead of hallucinating an
   approval.
7. Toggle **हिं**, repeat the visible report, then enable **Low data**.
8. Tick the consent checkbox and prepare the local draft checklist. Emphasise
   that no application or credential is submitted.
9. Close on: “The official source remains the decision-maker; HaqSetu reduces
   search and interpretation work while preserving user control.”

Alternative high-signal flow: choose **Street vendor** to show PM SVANidhi;
choose **Senior citizen** to show the age signal and state-level verification.

## 3. Run tests and evaluation

```powershell
python -m pytest tests\\test_agent.py -q
python scripts\\run_eval.py
Get-Content reports\\evaluation-results.md
```

The evaluator starts in-process and does not need a running server. It writes
machine-readable JSON and a short markdown scorecard under `reports/`.

## 4. Docker smoke test

```powershell
docker build -t haqsetu:demo .
docker run --rm -p 8000:8000 haqsetu:demo
```

In another window:

```powershell
curl.exe http://127.0.0.1:8000/api/health
```

For a local compose run:

```powershell
docker compose up --build
```

Do not claim a public endpoint until an external device can reach the host and
the organiser's API/manifest submission flow accepts the exact contract.

## 5. Optional static-frontend development mode

Only use this if you want to edit the frontend independently:

```powershell
python -m http.server 3000 -d frontend
```

Keep FastAPI on port 8000. The frontend automatically calls
`http://127.0.0.1:8000` when hosted on ports 3000 or 5173.

## 6. RTX 4050 guidance

### Recommended for the hackathon: no training

The actual prototype needs CPU-only Python. The GPU does not improve its
deterministic answer, and spending the 12-hour window on fine-tuning would add
latency, dependency risk, and unverifiable claims.

### Optional local language layer after the demo works

If the machine already has NVIDIA drivers and Docker GPU support, a local
Ollama model can paraphrase an answer **after** the rule engine has produced
the evidence. Never let a model invent eligibility facts or citations.

Example manual setup (optional; do not run during the first demo setup):

```powershell
ollama pull qwen2.5:3b
ollama run qwen2.5:3b
```

Keep prompts bounded to the returned evidence JSON, request JSON-only output,
and validate the output before displaying it. On a 6 GB RTX 4050, choose a
small quantized model, cap context, and keep CPU fallback enabled. The shipped
demo intentionally leaves this integration disabled so judges can reproduce it
without a model download or API key.

## 7. Submission checklist

- [ ] `python -m pytest tests\\test_agent.py -q` passes.
- [ ] `python scripts\\run_eval.py` produces a scorecard.
- [ ] `GET /api/health` is reachable in the submitted container/endpoint.
- [ ] `agent-manifest.yaml` matches the endpoint and port.
- [ ] Docker image opens the same UI at `/`.
- [ ] Demo video is 2–3 minutes and shows a real trace, evidence, and consent.
- [ ] Pitch deck has five slides; use `docs/pitch-deck.md`.
- [ ] Team members, domain, problem statement, repository, demo URL, and video
  URL are ready for the official Google Form.
- [ ] Every live source was re-opened immediately before submission; the
  prototype's `last_verified` dates are not live verification.

## 8. If something fails

| Symptom | Fix |
| --- | --- |
| `ModuleNotFoundError: fastapi` | Activate `.venv`, then install `backend\\requirements.txt`. |
| Browser shows API error | Confirm port 8000 server is running; use `/api/health`. |
| CORS error in split mode | Use the documented ports 3000/5173 or use the same-origin port 8000. |
| Docker build fails | Run `docker version`, then retry with network access; local run remains valid. |
| Scheme facts look stale | Open the official link and label the demo as a screening snapshot; do not silently edit claims. |
