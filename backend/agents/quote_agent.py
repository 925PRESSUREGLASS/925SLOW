from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from backend.core.spec_guard import grade
from backend.database import Quote, get_session


class QuoteAgent:
    """Generate simple window cleaning quotes."""

    name = "quote"
    PRICE_PER_WINDOW = 10.0

    def run(self, prompt: str, **_: Any) -> dict[str, Any]:  # noqa: D401,ANN401
        match = re.search(r"(\d+)\s+windows?\s+in\s+([A-Za-z]+)", prompt, flags=re.I)
        if match:
            qty = int(match.group(1))
            suburb = match.group(2).title()
        else:
            qty, suburb = 1, "Unknown"

        total = qty * self.PRICE_PER_WINDOW
        quote_line = f"> ${total:.2f} to clean {qty} windows in {suburb}"
        year = datetime.now(timezone.utc).year
        attribution = f"> — QuoteGPT, {year}"
        rationale = "Rationale: This is a placeholder rationale for the quote."
        full_quote = "\n".join([quote_line, attribution, "", rationale])

        # naive memory lookup for similar quotes
        with get_session() as sess:
            prior = (
                sess.query(Quote)
                .filter(Quote.suburb == suburb, Quote.total == total)
                .first()
            )
        vector_used = prior is not None

        spec_result = grade(full_quote)

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
            quote_id = obj.id

        return {
            "quote_text": full_quote,
            "rationale": rationale,
            "suburb": suburb,
            "quantity": qty,
            "total": total,
            "compliance": {
                "score": spec_result.score,
                "violations": spec_result.violations,
            },
            "vector_used": vector_used,
            "quote_id": quote_id,
        }
