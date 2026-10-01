"""A small deterministic and explainable rule engine.

This is a screening aid, not an adjudicator. It reports evidence from the
submitted profile and never claims official enrolment or approval.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


def _norm(value: Any) -> str:
    return str(value).strip().casefold()


def _values(value: Any) -> list[Any]:
    return value if isinstance(value, list) else [value]


def _get(profile: Any, field: str) -> Any:
    if isinstance(profile, dict):
        return profile.get(field)
    return getattr(profile, field, None)


@dataclass(frozen=True)
class RuleResult:
    rule_id: str
    field: str
    operation: str
    result: str
    observed: Any
    expected: Any
    explanation: str
    required: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "field": self.field,
            "operation": self.operation,
            "result": self.result,
            "observed": self.observed,
            "expected": self.expected,
            "explanation": self.explanation,
            "required": self.required,
        }


def evaluate_rule(profile: Any, rule: dict[str, Any]) -> RuleResult:
    field = str(rule.get("field", ""))
    operation = str(rule.get("op", "exists"))
    expected = rule.get("value")
    required = bool(rule.get("required", True))
    observed = _get(profile, field)
    rule_id = str(rule.get("id", field or "rule"))

    missing = observed is None or observed == ""
    if operation == "exists":
        matched = not missing
    elif missing:
        matched = False
    elif operation == "eq":
        matched = _norm(observed) == _norm(expected)
    elif operation == "in":
        matched = _norm(observed) in {_norm(item) for item in _values(expected)}
    elif operation == "contains_any":
        observed_text = _norm(observed)
        matched = any(_norm(item) in observed_text for item in _values(expected))
    elif operation == "list_contains_any":
        observed_values = [_norm(item) for item in _values(observed)]
        matched = any(_norm(item) in value for item in _values(expected) for value in observed_values)
    elif operation == "gt":
        matched = float(observed) > float(expected)
    elif operation == "gte":
        matched = float(observed) >= float(expected)
    elif operation == "lte":
        matched = float(observed) <= float(expected)
    elif operation == "bool_true":
        matched = observed is True
    else:
        # Unknown rules are never silently treated as eligibility matches.
        matched = False

    if missing:
        result = "missing"
        explanation = "This fact was not provided; verify it from an official record or portal."
    elif matched:
        result = "matched"
        explanation = "The supplied profile is consistent with this screening signal."
    else:
        result = "not_matched"
        explanation = "The supplied profile does not match this signal; this is not an official rejection."

    return RuleResult(rule_id, field, operation, result, observed, expected, explanation, required)


def evaluate_scheme(profile: Any, scheme: dict[str, Any]) -> dict[str, Any]:
    results = [evaluate_rule(profile, rule) for rule in scheme.get("rules", [])]
    required_not_matched = [item for item in results if item.required and item.result == "not_matched"]
    missing_required = [item for item in results if item.required and item.result == "missing"]
    matched = [item for item in results if item.result == "matched"]

    if required_not_matched:
        status = "not_matched_on_screening"
    elif missing_required:
        status = "needs_information"
    elif matched:
        status = "promising_signal_verify_officially"
    else:
        status = "verify_official_criteria"

    missing_facts = list(scheme.get("verification_facts", []))
    missing_facts.extend(item.field for item in missing_required if item.field not in missing_facts)
    return {
        "scheme_id": scheme["id"],
        "status": status,
        "confidence": "screening_only",
        "evidence": [item.as_dict() for item in results],
        "missing_facts": missing_facts,
        "required_documents": scheme.get("required_documents", []),
        "caveat": scheme.get("caveat", "Final eligibility is decided by the responsible department."),
    }


def retrieve_schemes(profile: Any, schemes: Iterable[dict[str, Any]], limit: int = 12) -> list[dict[str, Any]]:
    """Rank a broad set of schemes using transparent profile/need overlap."""

    occupation = _norm(_get(profile, "occupation"))
    needs = [_norm(item) for item in (_get(profile, "needs") or [])]
    scored: list[tuple[int, str, dict[str, Any]]] = []
    for scheme in schemes:
        score = 0
        matches: list[str] = []
        for keyword in scheme.get("keywords", []):
            keyword_norm = _norm(keyword)
            if any(keyword_norm in need for need in needs):
                score += 3
                matches.append(f"need:{keyword}")
            elif keyword_norm in occupation:
                score += 2
                matches.append(f"occupation:{keyword}")
        scored.append((score, scheme["id"], {**scheme, "retrieval_score": score, "retrieval_matches": matches}))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in scored[:limit]]
