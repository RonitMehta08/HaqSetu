# Research notes (1 October 2026)

This note records the external references used to shape the prototype. The
hackathon prompt is the authoritative event brief available in this workspace;
no separate MD attachment or link was present in the folder.

## Hackathon signals

The supplied brief requires a meaningful real-world problem, an agentic flow
that understands, reasons, uses tools/data, acts, and delivers, plus a working
prototype. It names these judging dimensions: agentic capability, Bharat
impact, technical implementation, innovation, UX, scalability/feasibility, and
demo quality. It also requires a project name, team/domain/problem statement,
solution overview, architecture, stack, repository, working demo, 2–3 minute
video, and five-slide pitch deck. The submission routes are a Docker/YAML
manifest or a hosted API endpoint, followed by the official form.

## Product research

The official myScheme site describes a national platform for discovery of
Central and State/UT schemes. Its public “how it works” flow is: enter basic
details, search relevant schemes, then select/apply. This validates the problem
direction and suggests that HaqSetu should complement discovery rather than
pretend to be a department.

## Technical research translated into choices

| Observation | Design choice |
| --- | --- |
| Agent judges need to distinguish action from chat | Show a four-step trace and return structured tool-like outputs. |
| Public-benefit rules change and vary by state | Attach official URLs, `last_verified` metadata, and a freshness warning. |
| Retrieval/generation systems can hallucinate | Use deterministic retrieval/rules for the scoring path; surface every missing fact. |
| Judges need reproducibility | No API key or training required; deterministic demo profiles and tests. |
| Bharat access is heterogeneous | English/Hindi copy, low-data mode, keyboard-safe UI, no image/CDN dependency. |
| Automation can cross a consent boundary | Draft checklist is disabled until explicit consent; no submission endpoint exists. |
| A laptop RTX 4050 is valuable but limited | Keep the baseline CPU-only; document optional small local-model/OCR upgrades. |

## Public references used

The complete source table, with the official link and what it supports, is in
`docs/sources.md`. Search snippets and secondary articles were used only to
understand context; scheme claims in the app point to official portals and are
phrased as screening signals, not approvals.

## Risks found

1. **Stale criteria:** source snapshots can age. The UI explicitly says manual
   verification is required and keeps `live_integrations: false` visible.
2. **State variation:** central scheme rules are not sufficient for final
   eligibility. The catalogue asks for state/local verification facts.
3. **Sensitive information:** an eligibility workflow tempts users to share
   identity and banking data. The UI tells users not to enter it and the logger
   excludes it.
4. **Language drift:** Hindi text needs native review before production. This
   prototype is a bilingual interaction proof, not a language certification.
5. **Selection bias:** curated seven-scheme coverage is not a claim of complete
   national coverage. A production version should ingest signed official source
   snapshots and report coverage.
