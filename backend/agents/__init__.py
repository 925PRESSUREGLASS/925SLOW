"""Agent namespace \u2013 concrete agents will be added incrementally."""



# NOTE: public re-export kept above in patch.


class BaseAgent:  # minimal base so subclasses compile
    """Skeleton for all agents. Real logic comes in later PRs."""

    name: str = "base"

    def run(self, prompt: str, **kwargs):  # noqa: ANN001 \u2013 narrow later
        raise NotImplementedError


from backend.database import get_session, Quote

class QuoteAgent(BaseAgent):
    name = "quote"

    _suburb_memory = set()

    def run(self, prompt: str, **kwargs):
        """Produce a *format-compliant* placeholder quote.

        Very naive parsing: look for "<number> windows in <Suburb>"
        and charge $10/ea.
        """
        import re
        from datetime import datetime, timezone

        match = re.search(
            r"(\d+)\s+windows?\s+in\s+([A-Za-z]+)",
            prompt,
            flags=re.I,
        )
        if match:
            qty = int(match.group(1))
            suburb = match.group(2).title()
        else:
            qty, suburb = 1, "Unknown"

        total = qty * 10.0
        year = datetime.utcnow().year

        quote_line = f"> {qty} windows in {suburb}: ${total:.2f}"
        attribution = f"— QuoteGPT, {year}"
        rationale = "Rationale: This is a placeholder rationale for the quote."

        full_quote = "\n".join([quote_line, attribution, "", rationale])

        # -------- SpecGuard -------------------------------------------------
        from backend.core.spec_guard import grade

        spec_result = grade(full_quote)

        # Vector memory logic: if suburb seen before, set vector_used True
        vector_used = suburb in self._suburb_memory
        self._suburb_memory.add(suburb)

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
            "vector_used": vector_used,
        }

        # -------- Persistence ----------------------------------------------
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


# from .customer_agent import CustomerAgent  # noqa: E402

