"""Wrapper around external or local LLMs.

Only a stub for now – returns a canned response so QuoteAgent can compile.
The real implementation will call OpenAI or Ollama based on `config.yaml`.
"""

from __future__ import annotations


def chat(prompt: str) -> str:  # noqa: D401,ANN001 – trunkated interface
    """Return a dummy LLM completion (for early tests)."""

    return f"LLM‑stub echo: {prompt}"
