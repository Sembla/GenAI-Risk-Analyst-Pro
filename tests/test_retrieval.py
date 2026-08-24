from __future__ import annotations

import unittest

from retrieval import retrieve


class RetrievalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.documents = [
            ("policy.txt", "Scores below the threshold trigger a high classification."),
            ("review.txt", "Unverified income triggers a manual human review."),
            ("audit.txt", "Every output records the active policy version."),
        ]

    def test_retrieves_relevant_document(self) -> None:
        result = retrieve("When is manual review required?", self.documents, top_k=1)
        self.assertEqual(result[0].source, "review.txt")

    def test_limits_results(self) -> None:
        self.assertEqual(len(retrieve("policy", self.documents, top_k=2)), 2)

    def test_empty_question_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "question cannot be empty"):
            retrieve(" ", self.documents)


if __name__ == "__main__":
    unittest.main()
