from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from backend.core.spec_guard import grade
from backend.database import Quote, get_session
from backend.quote_pricing import WindowJob

from .memory_agent import MemoryAgent


class QuoteAgent:
    """Generate placeholder quotes using simple heuristics."""

    name = "quote"

    def run(self, prompt: str, **kwargs: Any) -> dict[str, Any]:  # noqa: D401,ANN001
        match = re.search(r"(\d+)\s+windows?\s+in\s+([A-Za-z]+)", prompt, flags=re.I)
        if match:
            qty = int(match.group(1))
            suburb = match.group(2).title()
        else:
            qty, suburb = 1, "Unknown"

        total = WindowJob(qty).price()
        quote_line = f"> ${total:.2f} to clean {qty} windows in {suburb}"
        year = datetime.utcnow().year
        attribution = f"> — QuoteGPT, {year}"
        rationale = "Rationale: This is a placeholder rationale for the quote."

        full_quote = "\n".join([quote_line, attribution, "", rationale])

        relevant_snippets = MemoryAgent().run(prompt)
        spec_result = grade(full_quote)

        result = {
            "quote_text": full_quote,
            "rationale": rationale,
            "suburb": suburb,
            "quantity": qty,
            "total": total,
            "compliance": {
                "score": spec_result.score,
                "violations": spec_result.violations,
            },
            "vector_used": bool(relevant_snippets),
        }

        with get_session() as sess:
            obj = Quote(
                prompt=prompt,
                quote_text=full_quote,
                rationale=rationale,
                suburb=suburb,
                total=total,
            )
            sess.add(obj)
            sess.commit()
            result["quote_id"] = obj.id

        return result
