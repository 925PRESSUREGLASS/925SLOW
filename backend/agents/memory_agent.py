"""Simple memory lookup for past quotes via the database."""

from __future__ import annotations

import re
from typing import Any

from backend.database import Quote, get_session

from . import BaseAgent


class MemoryAgent(BaseAgent):
    """Retrieve past quotes that match the suburb mentioned in the prompt."""

    name = "memory"

    def run(
        self, prompt: str, top_k: int = 3, **kwargs: Any
    ) -> list[dict[str, Any]]:  # noqa: D401,ANN001
        """Return recent quote snippets for the same suburb, newest first."""

        match = re.search(r"in\s+([A-Za-z]+)", prompt, flags=re.I)
        suburb = match.group(1).title() if match else None

        if not suburb:
            return []

        with get_session() as sess:
            rows = (
                sess.query(Quote)
                .filter(Quote.suburb == suburb)
                .order_by(Quote.created_at.desc())
                .limit(top_k)
                .all()
            )

        return [{"snippet": q.quote_text, "score": 0.5} for q in rows]
