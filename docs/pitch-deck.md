# Five-slide pitch deck content

## Slide 1 — HaqSetu: from question to verified next step

**Citizen & GovTech · BHARAT AGENTIC 2026**

Millions of people know the support they need but not the programme, department,
documents, or current rule. HaqSetu is an evidence-first, bilingual agent for
the safe first mile of benefit discovery.

Visual: hero screenshot plus the line `Understand → Reason → Use tools → Act → Deliver`.

## Slide 2 — The gap and the Bharat impact

- Search is fragmented across government portals and long eligibility pages.
- State, season, household, and document conditions are easy to miss.
- Overconfident AI can create false hope or unsafe data sharing.
- Citizens and CSC/NGO facilitators need a quick, explainable hand-off.

Success hypothesis: reduce time-to-first-relevant-official-link while increasing
the share of users who can name the next verification step.

Visual: “many portals → one safe first mile” diagram.

## Slide 3 — The agent, not a chatbot

1. Intake broad facts and natural-language need.
2. Retrieve ranked official-source-linked schemes.
3. Evaluate explicit rules and label every signal.
4. Generate evidence, missing facts, and counterfactuals.
5. Plan the next action; ask for consent before a local draft.

Visual: four-node timeline from the product UI.

## Slide 4 — Why HaqSetu stands out

**Evidence + Counterfactual Ledger**

- Source URL and freshness warning per result.
- Matched / not matched / missing evidence visible.
- “What could change the result?” instead of a hallucinated approval.
- No credentials, no live application submission, no hidden decision.
- English/Hindi, low-data mode, deterministic tests, Docker + YAML manifest.

Visual: annotated PM-KISAN card + counterfactual panel.

## Slide 5 — Working prototype and path to scale

- FastAPI + Pydantic + replaceable scheme catalogue + vanilla accessible UI.
- 25 official source routes represented in a cautious prototype snapshot, with
  12 ranked results available per profile.
- Automated tests for safety, determinism, citations, and retrieval.
- Production path: signed source snapshots, freshness review, multilingual
  retrieval, facilitator mode, audited connectors with human confirmation.

Demo ask: try the farmer or vendor scenario, inspect the evidence, switch Hindi,
and observe the consent gate.
