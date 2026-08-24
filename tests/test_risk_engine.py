from __future__ import annotations

import unittest

from risk_engine import DemoCase, DemoPolicy, evaluate_case, validate_case


POLICY = DemoPolicy(
    version="test-v1",
    high_risk_below=600,
    low_risk_at_or_above=750,
    manual_review_on_unverified_income=True,
    manual_review_on_recent_late_payments=True,
)


class RiskEngineTests(unittest.TestCase):
    def test_high_classification_uses_threshold(self) -> None:
        decision = evaluate_case(DemoCase("A", 599, 0, True), POLICY)
        self.assertEqual(decision.classification, "high")
        self.assertTrue(decision.manual_review)

    def test_moderate_classification(self) -> None:
        decision = evaluate_case(DemoCase("B", 650, 0, True), POLICY)
        self.assertEqual(decision.classification, "moderate")
        self.assertFalse(decision.manual_review)

    def test_low_classification(self) -> None:
        decision = evaluate_case(DemoCase("C", 800, 0, True), POLICY)
        self.assertEqual(decision.classification, "low")
        self.assertFalse(decision.manual_review)

    def test_late_payment_triggers_review_without_changing_classification(self) -> None:
        decision = evaluate_case(DemoCase("D", 800, 1, True), POLICY)
        self.assertEqual(decision.classification, "low")
        self.assertTrue(decision.manual_review)

    def test_unverified_income_triggers_review(self) -> None:
        decision = evaluate_case(DemoCase("E", 800, 0, False), POLICY)
        self.assertTrue(decision.manual_review)

    def test_invalid_score_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "between 0 and 1000"):
            validate_case(DemoCase("F", 1001, 0, True))


if __name__ == "__main__":
    unittest.main()
