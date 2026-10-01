"""Run HaqSetu's deterministic, rubric-oriented offline evaluation.

Usage: python scripts/run_eval.py
The script exercises the real FastAPI application in-process and writes a
machine-readable and human-readable report under reports/.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evaluation" / "cases.json"
REPORTS = ROOT / "reports"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.main import app
REQUIRED_TRACE = {
    "intake", "retrieved_schemes", "eligibility_evidence", "missing_facts",
    "counterfactuals", "action_plan", "citations", "consent_required",
    "readiness_score",
}
# Negative safety language such as “does not guarantee a loan” is desirable;
# flag only affirmative claims that the assistant has approved/guaranteed the
# person or benefit.
FORBIDDEN_CLAIM_PATTERNS = [
    r"\byou(?: are|'re) approved\b",
    r"\bapproved for\b",
    r"\byou(?: are|'re) guaranteed\b",
    r"\bguaranteed to receive\b",
    r"\bguarantee(?:d)? (?:approval|eligibility|payment)\b",
]


def load_cases() -> list[dict[str, Any]]:
    with CASES_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def has_forbidden_claim(value: Any) -> bool:
    text = json.dumps(value, ensure_ascii=False).casefold()
    return any(re.search(pattern, text) for pattern in FORBIDDEN_CLAIM_PATTERNS)


def evaluate_case(client: TestClient, case: dict[str, Any]) -> dict[str, Any]:
    response = client.post("/api/analyze", json={"profile": case["profile"]})
    body = response.json()
    trace = body.get("trace", {}) if response.status_code == 200 else {}
    retrieved = trace.get("retrieved_schemes", [])
    retrieved_ids = {item.get("id") for item in retrieved}
    expected = set(case.get("expected_scheme_ids", []))
    hit = not expected or bool(expected & retrieved_ids)
    citations = trace.get("citations", [])
    citation_coverage = bool(retrieved) and all(
        bool(item.get("source", {}).get("official")) and bool(item.get("source", {}).get("url"))
        for item in citations
    )
    evidence_coverage = len(trace.get("eligibility_evidence", [])) == len(retrieved)
    counterfactual_coverage = (
        bool(trace.get("counterfactuals"))
        if case.get("requires_counterfactual")
        else True
    )
    schema_complete = REQUIRED_TRACE.issubset(trace)
    safe_language = (
        "screening" in json.dumps(body, ensure_ascii=False).casefold()
        and "official" in json.dumps(body, ensure_ascii=False).casefold()
        and not has_forbidden_claim(body)
    )
    repeat = client.post("/api/analyze", json={"profile": case["profile"]})
    deterministic = response.status_code == 200 and body == repeat.json()
    return {
        "id": case["id"],
        "label": case["label"],
        "http_ok": response.status_code == 200,
        "retrieval_hit": hit,
        "retrieved_ids": sorted(retrieved_ids),
        "citation_coverage": citation_coverage,
        "evidence_coverage": evidence_coverage,
        "counterfactual_coverage": counterfactual_coverage,
        "schema_complete": schema_complete,
        "safe_language": safe_language,
        "deterministic": deterministic,
        "readiness_score": trace.get("readiness_score"),
    }


def mean(rows: list[dict[str, Any]], key: str) -> float:
    return round(sum(bool(row.get(key)) for row in rows) / max(1, len(rows)) * 100, 1)


def main() -> int:
    cases = load_cases()
    with TestClient(app) as client:
        rows = [evaluate_case(client, case) for case in cases]
    metrics = {
        key: mean(rows, key)
        for key in (
            "http_ok", "retrieval_hit", "citation_coverage", "evidence_coverage",
            "counterfactual_coverage", "schema_complete", "safe_language", "deterministic",
        )
    }
    report = {
        "project": "HaqSetu",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "case_count": len(rows),
        "metrics_percent": metrics,
        "cases": rows,
        "interpretation": "Offline regression metrics over anonymised realistic fixtures; not official eligibility accuracy.",
    }
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "evaluation-results.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    markdown = [
        "# HaqSetu evaluation results",
        "",
        f"Generated: `{report['generated_at']}`",
        "",
        "> These are offline regression metrics over anonymised realistic test fixtures. They are not official eligibility accuracy.",
        "",
        "| Metric | Score |",
        "| --- | ---: |",
    ]
    for key, value in metrics.items():
        markdown.append(f"| {key.replace('_', ' ').title()} | {value:.1f}% |")
    markdown.extend(["", "| Case | Retrieval | Evidence | Counterfactual | Safe | Deterministic |", "| --- | --- | --- | --- | --- | --- |"])
    for row in rows:
        tick = lambda value: "PASS" if value else "FAIL"
        markdown.append(
            f"| {row['id']} | {tick(row['retrieval_hit'])} | {tick(row['evidence_coverage'])} | "
            f"{tick(row['counterfactual_coverage'])} | {tick(row['safe_language'])} | {tick(row['deterministic'])} |"
        )
    (REPORTS / "evaluation-results.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")
    print("HaqSetu evaluation")
    for key, value in metrics.items():
        print(f"- {key}: {value:.1f}%")
    print(f"- cases: {len(rows)}")
    print(f"- report: {REPORTS / 'evaluation-results.md'}")
    return 0 if all(value >= 80 for value in metrics.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
