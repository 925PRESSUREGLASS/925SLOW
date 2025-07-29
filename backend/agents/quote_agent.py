from __future__ import annotations

import re
from datetime import datetime, timezone

from backend.core.spec_guard import grade
from backend.database import Quote, get_session
from backend.quote_pricing import WindowJob

from . import BaseAgent


class QuoteAgent(BaseAgent):
    name = "quote"

    def run(self, prompt: str, **kwargs):
        """Produce a format-compliant quote using simple heuristics."""
        match = re.search(r"(\d+)\s+windows?\s+in\s+([A-Za-z]+)", prompt, flags=re.I)
        if match:
            qty = int(match.group(1))
            suburb = match.group(2).title()
        else:
            qty, suburb = 1, "Unknown"

        # pricing via shared util
        total = WindowJob(qty).price()
        year = datetime.now(timezone.utc).year

        quote_line = f"> ${total:,.2f} for cleaning {qty} windows in {suburb}"
        attribution = f"> — QuoteGPT, {year}"
        rationale = "Rationale: placeholder $10/window rate while pricing engine is pending."

        full_quote = "\n".join([quote_line, attribution, "", rationale])

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
