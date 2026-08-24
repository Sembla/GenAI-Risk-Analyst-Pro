"""Small TF-IDF retriever used to demonstrate document grounding."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class RetrievedDocument:
    source: str
    score: float
    content: str


def load_documents(directory: Path) -> list[tuple[str, str]]:
    documents: list[tuple[str, str]] = []
    for path in sorted(directory.glob("*.txt")):
        content = path.read_text(encoding="utf-8").strip()
        if content:
            documents.append((path.name, content))
    if not documents:
        raise ValueError(f"No text documents found in {directory}")
    return documents


def retrieve(
    question: str,
    documents: list[tuple[str, str]],
    top_k: int = 2,
) -> list[RetrievedDocument]:
    if not question.strip():
        raise ValueError("question cannot be empty")
    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")
    if not documents:
        raise ValueError("documents cannot be empty")

    names, contents = zip(*documents)
    vectorizer = TfidfVectorizer(lowercase=True, strip_accents="unicode")
    document_vectors = vectorizer.fit_transform(contents)
    question_vector = vectorizer.transform([question])
    scores = cosine_similarity(question_vector, document_vectors).flatten()
    ranked = scores.argsort()[::-1][: min(top_k, len(documents))]

    return [
        RetrievedDocument(
            source=names[index],
            score=float(scores[index]),
            content=contents[index],
        )
        for index in ranked
    ]
