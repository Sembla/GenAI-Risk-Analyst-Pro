from __future__ import annotations

from risk_engine import DemoCase, RiskDecision


def local_explanation(case: DemoCase, decision: RiskDecision) -> str:
    reasons = "; ".join(decision.reasons)
    review = "required" if decision.manual_review else "not triggered"
    return (
        f"Demo case {case.case_id}: classification={decision.classification}; "
        f"manual review={review}. Reasons: {reasons}. "
        "This prototype output is not a real credit decision."
    )
