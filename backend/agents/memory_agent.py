"""MemoryAgent – retrieves semantically similar past quotes."""

from __future__ import annotations

from backend.core.vector_handler import search


class MemoryAgent:  # noqa: D401 – no BaseAgent (doesn’t generate)
    name = "memory"

    @staticmethod
    def run(prompt: str, top_k: int = 3):  # noqa: D401,ANN001 – simple API
        """Return the *text* of the top‑K similar quotes."""

        matches = search(prompt, n_results=top_k)
        return [{"id": m["id"], "score": m["score"], "snippet": m["text"][:200]} for m in matches]
