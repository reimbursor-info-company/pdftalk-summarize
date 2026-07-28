"""Offline extractive summarization using a TextRank-style algorithm.

Pure standard library implementation (no NLTK, no network access, no models
to download): sentences are scored by how similar they are to the rest of
the document, and the most representative ones are kept.
"""

import math
import re
from collections import Counter

from .stopwords import DEFAULT as DEFAULT_STOPWORDS

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ0-9])")
_WORD_RE = re.compile(r"[a-záéíóúñü]+", re.IGNORECASE)


def split_sentences(text: str) -> list[str]:
    """Split raw text into sentences, ignoring blank lines."""
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []
    return [s.strip() for s in _SENTENCE_SPLIT_RE.split(normalized) if s.strip()]


def _tokenize(sentence: str, stopwords: set[str]) -> list[str]:
    words = _WORD_RE.findall(sentence.lower())
    return [w for w in words if w not in stopwords]


def _similarity(a: Counter, b: Counter) -> float:
    common = sum((a & b).values())
    if common == 0:
        return 0.0
    norm = math.log(max(sum(a.values()), 2)) + math.log(max(sum(b.values()), 2))
    return common / norm if norm else 0.0


def _pagerank(matrix: list[list[float]], damping: float = 0.85, iterations: int = 50) -> list[float]:
    n = len(matrix)
    if n == 0:
        return []
    scores = [1.0 / n] * n
    out_weight = [sum(row) or 1.0 for row in matrix]

    for _ in range(iterations):
        new_scores = [(1 - damping) / n] * n
        for i in range(n):
            for j in range(n):
                if matrix[j][i]:
                    new_scores[i] += damping * matrix[j][i] / out_weight[j] * scores[j]
        if sum(abs(new_scores[i] - scores[i]) for i in range(n)) < 1e-5:
            scores = new_scores
            break
        scores = new_scores

    return scores


def summarize(
    text: str,
    ratio: float = 0.2,
    max_sentences: int | None = None,
    language: str = "auto",
) -> str:
    """Summarize text by extracting its most representative sentences.

    ratio: fraction of the original sentences to keep (0.0-1.0).
    max_sentences: hard cap on the number of sentences kept, applied after ratio.
    language: "es", "en", or "auto" to use the combined Spanish/English stopword list.
    """
    if not text.strip():
        raise ValueError("The text to summarize is empty.")
    if not 0.0 < ratio <= 1.0:
        raise ValueError("ratio must be between 0.0 (exclusive) and 1.0 (inclusive).")

    sentences = split_sentences(text)
    if len(sentences) <= 1:
        return text.strip()

    stopwords = DEFAULT_STOPWORDS
    if language == "es":
        from .stopwords import SPANISH as stopwords
    elif language == "en":
        from .stopwords import ENGLISH as stopwords

    token_counts = [Counter(_tokenize(s, stopwords)) for s in sentences]

    n = len(sentences)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = _similarity(token_counts[i], token_counts[j])

    scores = _pagerank(matrix)

    keep = max(1, round(n * ratio))
    if max_sentences is not None:
        keep = min(keep, max_sentences)

    top_indices = sorted(range(n), key=lambda i: scores[i], reverse=True)[:keep]
    top_indices.sort()

    return " ".join(sentences[i] for i in top_indices)
