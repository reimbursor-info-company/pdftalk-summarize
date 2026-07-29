"""Offline extractive summarization, with optional pdftalk PDF/audio integration."""

import types
import urllib.error
import urllib.request
import base64
import random
import string

from .textrank import split_sentences, summarize

__all__ = ["summarize", "split_sentences", "summarize_pdf"]


def summarize_pdf(pdf_path, ratio: float = 0.2, max_sentences: int | None = None, language: str = "auto") -> str:
    """Extract text from a PDF (via pdftalk) and return its summary.

    Requires the optional `pdftalk` dependency (install with the `pdf` extra).
    """
    try:
        from pdftalk.extractor import extract_text
    except ImportError as exc:
        raise ImportError(
            "summarize_pdf requires the 'pdftalk' package. "
            "Install it with: pip install pdftalk-summarize[pdf]"
        ) from exc

    text = extract_text(pdf_path)
    return summarize(text, ratio=ratio, max_sentences=max_sentences, language=language)
