"""Deterministic demonstration engine for synthetic credit-risk cases."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DemoPolicy:
    version: str
    high_risk_below: int
    low_risk_at_or_above: int
    manual_review_on_unverified_income: bool
    manual_review_on_recent_late_payments: bool


@dataclass(frozen=True)
class DemoCase:
    case_id: str
    score: int
    recent_late_payments: int
    income_verified: bool


@dataclass(frozen=True)
class RiskDecision:
    classification: str
    manual_review: bool
    reasons: tuple[str, ...]
    policy_version: str


def load_policy(path: Path) -> DemoPolicy:
    payload = json.loads(path.read_text(encoding="utf-8"))
    policy = DemoPolicy(
        version=str(payload["version"]),
        high_risk_below=int(payload["high_risk_below"]),
        low_risk_at_or_above=int(payload["low_risk_at_or_above"]),
        manual_review_on_unverified_income=bool(
            payload["manual_review_on_unverified_income"]
        ),
        manual_review_on_recent_late_payments=bool(
            payload["manual_review_on_recent_late_payments"]
        ),
    )
    if not 0 < policy.high_risk_below < policy.low_risk_at_or_above <= 1000:
        raise ValueError("Invalid policy thresholds")
    return policy


def validate_case(case: DemoCase) -> None:
    if not case.case_id.strip():
        raise ValueError("case_id cannot be empty")
    if not 0 <= case.score <= 1000:
        raise ValueError("score must be between 0 and 1000")
    if case.recent_late_payments < 0:
        raise ValueError("recent_late_payments cannot be negative")


def evaluate_case(case: DemoCase, policy: DemoPolicy) -> RiskDecision:
    """Apply transparent demonstration rules without an LLM."""
    validate_case(case)
    reasons: list[str] = []

    if case.score < policy.high_risk_below:
        classification = "high"
        reasons.append("score is below the demo high-risk threshold")
    elif case.score >= policy.low_risk_at_or_above:
        classification = "low"
        reasons.append("score meets the demo low-risk threshold")
    else:
        classification = "moderate"
        reasons.append("score is inside the demo review range")

    manual_review = classification == "high"
    if policy.manual_review_on_recent_late_payments and case.recent_late_payments > 0:
        manual_review = True
        reasons.append("recent late payments require review under the demo policy")
    if policy.manual_review_on_unverified_income and not case.income_verified:
        manual_review = True
        reasons.append("income is not verified")

    return RiskDecision(
        classification=classification,
        manual_review=manual_review,
        reasons=tuple(reasons),
        policy_version=policy.version,
    )
