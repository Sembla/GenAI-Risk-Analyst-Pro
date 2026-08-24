"""Optional explanation adapter. The LLM does not calculate the decision."""

from __future__ import annotations

import json
import os
from dataclasses import asdict

from retrieval import RetrievedDocument
from risk_engine import RiskDecision


def explain_decision(
    decision: RiskDecision,
    documents: list[RetrievedDocument],
    question: str,
) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    from openai import OpenAI

    payload = {
        "question": question,
        "deterministic_decision": asdict(decision),
        "retrieved_documents": [
            {"source": document.source, "content": document.content}
            for document in documents
        ],
    }
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Explain the supplied deterministic demo decision in Brazilian Portuguese. "
                    "Do not change the classification. Cite source filenames and state that this "
                    "is an educational prototype, not a real credit decision."
                ),
            },
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content.strip()
