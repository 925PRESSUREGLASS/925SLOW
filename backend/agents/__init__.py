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
        from datetime import datetime

        match = re.search(r"(\d+)\s+windows?\s+in\s+([A-Za-z]+)", prompt, flags=re.I)
        if match:
            qty = int(match.group(1))
            suburb = match.group(2).title()
        else:
            qty, suburb = 1, "Unknown"

        total = qty * 10.0
        year = datetime.utcnow().year

        quote_line = f"> \${total:,.2f} for cleaning {qty} windows in {suburb}"
        attribution = f"> \u2014 QuoteGPT, {year}"
        rationale = (
            "Rationale: placeholder $10/window rate while pricing engine is pending."
        )

        full_quote = "\n".join([quote_line, attribution, "", rationale])

        return {
            "quote_text": full_quote,
            "rationale": rationale,
            "suburb": suburb,
            "quantity": qty,
            "total": total,
        }

