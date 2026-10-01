from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import app
from backend.rules import evaluate_rule


client = TestClient(app)


def test_health_is_explicitly_demo_only() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["demo_mode"] is True
    assert body["live_integrations"] is False


def test_scheme_catalogue_has_broad_official_coverage() -> None:
    response = client.get("/api/schemes?language=hi")
    assert response.status_code == 200
    body = response.json()
    assert len(body["schemes"]) >= 20
    assert all(item["source"]["official"] is True for item in body["schemes"])
    assert len(body["schemes"]) == len({item["id"] for item in body["schemes"]})
    assert any("प्रधानमंत्री" in item["name"] for item in body["schemes"])
    assert body["live_lookup"] is False


def test_analysis_returns_more_than_the_original_six_scheme_window() -> None:
    response = client.post("/api/analyze", json={"demo": "farmer"})
    assert response.status_code == 200
    retrieved = response.json()["trace"]["retrieved_schemes"]
    assert len(retrieved) == 12
    assert all(item["source"]["official"] is True for item in retrieved)


def test_demo_analysis_contains_evidence_trace_and_is_repeatable() -> None:
    first = client.post("/api/analyze", json={"demo": "farmer"})
    second = client.post("/api/analyze", json={"demo": "farmer"})
    assert first.status_code == 200
    assert second.status_code == 200
    body = first.json()
    assert body == second.json()
    trace = body["trace"]
    for key in (
        "intake", "retrieved_schemes", "eligibility_evidence", "missing_facts",
        "action_plan", "citations", "consent_required", "readiness_score",
        "estimated_time_saved_minutes", "estimated_time_saved",
    ):
        assert key in trace
    assert body["mode"] == "demo"
    assert "official" in body["disclaimer"].lower()
    assert all(item["confidence"] == "screening_only" for item in trace["eligibility_evidence"])


def test_bare_hindi_profile_is_adapted_without_live_calls() -> None:
    payload = {
        "state": "Uttar Pradesh",
        "age": 35,
        "occupation": "street vendor",
        "monthly_income": 15000,
        "social_category": "SC",
        "landholding": 0,
        "disability": False,
        "needs": ["ऋण", "स्वास्थ्य"],
        "language": "hi",
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "screening"
    assert body["trace"]["intake"]["language"] == "hi"
    assert "आधिकारिक" in body["disclaimer"]
    assert any(item["id"] == "pm-svanidhi" for item in body["trace"]["retrieved_schemes"])


def test_invalid_profile_is_rejected() -> None:
    response = client.post("/api/analyze", json={"demo": "does-not-exist"})
    assert response.status_code == 400
    response = client.post("/api/analyze", json={"state": "Bihar", "age": 20})
    assert response.status_code == 422


def test_rule_engine_reports_missing_and_match_explicitly() -> None:
    result = evaluate_rule(
        {"age": 65},
        {"id": "age", "field": "age", "op": "gte", "value": 60, "required": True},
    )
    assert result.result == "matched"
    missing = evaluate_rule(
        {},
        {"id": "land", "field": "landholding", "op": "gt", "value": 0, "required": True},
    )
    assert missing.result == "missing"


def test_feedback_does_not_require_identity() -> None:
    response = client.post("/api/feedback", json={"rating": 5, "helpful": True})
    assert response.status_code == 200
    assert response.json()["accepted"] is True


def test_counterfactual_ledger_and_consent_boundary_are_present() -> None:
    response = client.post("/api/analyze", json={"demo": "farmer"})
    assert response.status_code == 200
    trace = response.json()["trace"]
    assert trace["counterfactuals"]
    assert trace["consent_required"] is True
    assert all("official" in item["why_it_matters"].lower() for item in trace["counterfactuals"])
    assert all("url" in item["source"] for item in trace["citations"])


def test_same_origin_frontend_is_served_for_container_demo() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "HaqSetu" in response.text
    assert client.get("/app.js").status_code == 200
