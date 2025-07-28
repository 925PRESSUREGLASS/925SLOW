"""Agent namespace \u2013 concrete agents will be added incrementally."""

__all__ = ["BaseAgent", "QuoteAgent"]

# NOTE: public re-export kept above in patch.


class BaseAgent:  # minimal base so subclasses compile
    """Skeleton for all agents. Real logic comes in later PRs."""

    name: str = "base"

    def run(self, prompt: str, **kwargs):  # noqa: ANN001 \u2013 narrow later
        raise NotImplementedError


class QuoteAgent(BaseAgent):
    name = "quote"

    def run(self, prompt: str, **kwargs):  # noqa: D401,ANN001
        """Produce a *format-compliant* placeholder quote.

        Very naive parsing: look for "<number> windows in <Suburb>" and charge $10/ea.
        """

        import re
        from datetime import datetime, timezone

        match = re.search(r"(\d+)\s+windows?\s+in\s+([A-Za-z]+)", prompt, flags=re.I)
        if match:
            qty = int(match.group(1))
            suburb = match.group(2).title()
        else:
            qty, suburb = 1, "Unknown"

        total = qty * 10.0
        year = datetime.now(timezone.utc).year

        quote_line = f"> ${total:,.2f} for cleaning {qty} windows in {suburb}"
        attribution = f"> \u2014 QuoteGPT, {year}"
        rationale = (
            "Rationale: placeholder $10/window rate while pricing engine is pending."
        )

        full_quote = "\n".join([quote_line, attribution, "", rationale])

        # -------- SpecGuard -------------------------------------------------

        from backend.core.spec_guard import grade

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

        # -------- Persistence ----------------------------------------------

        from backend.database import Quote, get_session  # local import to avoid heavy dep on start-up

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

