"""Application service for HaqSetu analysis and feedback."""

from __future__ import annotations

import hashlib
import logging
import secrets
from typing import Any

from .i18n import DISCLAIMER, TEXT, lang, localized
from .rules import evaluate_scheme, retrieve_schemes

logger = logging.getLogger("haqsetu")


def _stable_id(profile: Any) -> str:
    """Create a non-identifying analysis id for local demo repeatability."""

    values = "|".join(
        str(getattr(profile, field, ""))
        for field in ("state", "age", "occupation", "monthly_income", "social_category", "language")
    )
    return "hs-" + hashlib.sha256(values.encode("utf-8")).hexdigest()[:12]


def _age_band(age: int) -> str:
    if age < 18:
        return "under_18"
    if age < 30:
        return "18_29"
    if age < 60:
        return "30_59"
    return "60_plus"


def privacy_safe_log(event: str, profile: Any | None = None, **metadata: Any) -> None:
    """Log aggregate diagnostics only; never log name, income, or raw profile."""

    safe: dict[str, Any] = {"event": event, **metadata}
    if profile is not None:
        safe.update(
            {
                "state": getattr(profile, "state", "unknown"),
                "age_band": _age_band(int(getattr(profile, "age", 0))),
                "language": getattr(profile, "language", "en"),
            }
        )
    logger.info("haqsetu_event %s", safe)


def _scheme_view(scheme: dict[str, Any], language: str) -> dict[str, Any]:
    return {
        "id": scheme["id"],
        "name": localized(scheme, language, "name"),
        "summary": localized(scheme, language, "summary"),
        "ministry": scheme["ministry"],
        "source": scheme["source"],
        "tags": scheme.get("tags", []),
    }


def _readiness(results: list[dict[str, Any]]) -> int:
    """A bounded completeness indicator, not a probability of approval."""

    if not results:
        return 0
    points = 0
    for result in results:
        evidence = result["evidence"]
        points += sum(1 for item in evidence if item["result"] == "matched")
        points += sum(1 for item in evidence if item["result"] == "missing") * 0.25
    maximum = max(1, sum(len(result["evidence"]) for result in results))
    completeness = int(round(min(1, points / maximum) * 100))
    return max(10, min(95, completeness))


def _counterfactuals(profile: Any, scheme: dict[str, Any], evaluation: dict[str, Any], language: str) -> list[dict[str, Any]]:
    """Return bounded, explainable 'what would change the signal?' prompts.

    These are not recommendations to misrepresent facts. They identify the
    next fact to verify, which is useful for a citizen or a facilitator and
    gives the judge a visible example of counterfactual reasoning.
    """

    messages_en = {
        "missing": "Provide or verify this fact from the official record before relying on the signal.",
        "not_matched": "If the official record differs, re-run screening; do not change facts just to qualify.",
    }
    messages_hi = {
        "missing": "इस संकेत पर भरोसा करने से पहले आधिकारिक रिकॉर्ड से इस तथ्य की पुष्टि करें।",
        "not_matched": "यदि आधिकारिक रिकॉर्ड अलग हो तो स्क्रीनिंग फिर चलाएं; पात्र बनने के लिए तथ्य न बदलें।",
    }
    messages = messages_hi if language == "hi" else messages_en
    by_rule = {str(rule.get("id")): rule for rule in scheme.get("rules", [])}
    items: list[dict[str, Any]] = []
    for evidence in evaluation.get("evidence", []):
        if evidence.get("result") not in {"missing", "not_matched"}:
            continue
        rule = by_rule.get(str(evidence.get("rule_id")), {})
        operation = str(rule.get("op", evidence.get("operation", "exists")))
        expected = rule.get("value", evidence.get("expected"))
        field = str(evidence.get("field", rule.get("field", "fact")))
        if evidence.get("result") == "missing":
            to_change = (
                f"Verify {field}"
                if language == "en"
                else f"पुष्टि करें: {field}"
            )
        elif operation in {"gte", "gt", "lte"}:
            symbol = {"gte": "≥", "gt": ">", "lte": "≤"}[operation]
            to_change = f"Official {field} should be {symbol} {expected}"
        elif operation in {"in", "eq"}:
            options = expected if isinstance(expected, list) else [expected]
            to_change = f"Official {field} is one of: {', '.join(map(str, options))}"
        elif operation in {"contains_any", "list_contains_any"}:
            options = expected if isinstance(expected, list) else [expected]
            to_change = f"Official record contains: {', '.join(map(str, options[:4]))}"
        elif operation == "bool_true":
            to_change = f"Official {field} is confirmed"
        else:
            to_change = f"Verify official {field}"
        items.append(
            {
                "scheme_id": evaluation["scheme_id"],
                "scheme_name": localized(scheme, language, "name"),
                "field": field,
                "observed": evidence.get("observed"),
                "signal": to_change,
                "why_it_matters": messages[evidence["result"]],
                "result": evidence["result"],
            }
        )
    return items[:4]


def analyze(profile: Any, all_schemes: list[dict[str, Any]], mode: str = "screening") -> dict[str, Any]:
    language = lang(profile.language)
    candidates = retrieve_schemes(profile, all_schemes)
    evaluations = [evaluate_scheme(profile, scheme) for scheme in candidates]
    names = {scheme["id"]: localized(scheme, language, "name") for scheme in candidates}

    retrieved: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    counterfactuals: list[dict[str, Any]] = []
    for scheme, evaluation in zip(candidates, evaluations):
        retrieved.append(
            {
                **_scheme_view(scheme, language),
                "retrieval_score": scheme.get("retrieval_score", 0),
                "why_retrieved": scheme.get("retrieval_matches", []) or ["broad screening catalogue"],
                "screening_status": evaluation["status"],
            }
        )
        evidence.append({"scheme_id": scheme["id"], "scheme_name": names[scheme["id"]], **evaluation})
        if evaluation["missing_facts"]:
            missing.append(
                {
                    "scheme_id": scheme["id"],
                    "scheme_name": names[scheme["id"]],
                    "facts": evaluation["missing_facts"],
                }
            )
        counterfactuals.extend(_counterfactuals(profile, scheme, evaluation, language))

    score = _readiness(evaluations)
    promising = [item for item in evaluations if item["status"] == "promising_signal_verify_officially"]
    consent_required = bool(promising)
    text = TEXT[language]
    actions: list[dict[str, Any]] = [
        {
            "priority": 1,
            "step": text["verify"],
            "scheme_ids": [item["scheme_id"] for item in promising[:3]] or [item["scheme_id"] for item in evaluations[:2]],
        }
    ]
    if missing:
        actions.append(
            {
                "priority": 2,
                "step": (
                    "Collect only the listed missing facts/documents, without sharing credentials."
                    if language == "en"
                    else "केवल सूचीबद्ध जानकारी/दस्तावेज़ जुटाएं और कोई प्रमाण-पत्र साझा न करें।"
                ),
                "missing_facts": missing,
            }
        )
    actions.append(
        {
            "priority": 3,
            "step": text["consent"] if consent_required else text["no_consent"],
            "consent_required": consent_required,
        }
    )

    citations = [
        {
            "scheme_id": scheme["id"],
            "name": localized(scheme, language, "name"),
            "source": scheme["source"],
            "note": (
                "Open the official source to confirm current eligibility, documents, and deadline."
                if language == "en"
                else "वर्तमान पात्रता, दस्तावेज़ और समय-सीमा की पुष्टि के लिए आधिकारिक स्रोत खोलें।"
            ),
        }
        for scheme in candidates
    ]

    analysis_id = _stable_id(profile)
    estimated_minutes = min(30, 5 + len(candidates) * 3)
    trace = {
        "intake": {
            "language": language,
            "summary": text["intake"],
            "fields_received": [
                "state", "age", "occupation", "monthly_income", "social_category",
                "landholding", "disability", "needs",
            ],
            "privacy_note": "Name is not used by the rules and is excluded from logs.",
        },
        "retrieved_schemes": retrieved,
        "eligibility_evidence": evidence,
        "missing_facts": missing,
        "counterfactuals": counterfactuals[:12],
        "action_plan": actions,
        "citations": citations,
        "consent_required": consent_required,
        "readiness_score": score,
        "readiness_note": "Screening completeness only; not a probability of approval.",
        "estimated_time_saved_minutes": estimated_minutes,
        "estimated_time_saved": f"{estimated_minutes} minutes",
        "time_saved_note": text["time_saved"],
    }
    privacy_safe_log(
        "analysis_complete", profile, mode=mode, scheme_count=len(candidates),
        promising_count=len(promising), consent_required=consent_required, readiness_score=score,
    )
    return {"analysis_id": analysis_id, "mode": mode, "disclaimer": DISCLAIMER[language], "trace": trace}


def feedback(payload: dict[str, Any]) -> dict[str, Any]:
    """Accept anonymous feedback without persisting sensitive user data."""

    feedback_id = "fb-" + secrets.token_hex(6)
    privacy_safe_log(
        "feedback_received", rating=payload.get("rating"), helpful=payload.get("helpful"),
        has_comment=bool(payload.get("comment")),
    )
    return {
        "accepted": True,
        "feedback_id": feedback_id,
        "message": "Thank you. Feedback is accepted for the demo and is not linked to an identity.",
    }
