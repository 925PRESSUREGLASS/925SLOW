"""Agent namespace \u2013 concrete agents will be added incrementally."""

__all__ = ["BaseAgent", "QuoteAgent", "CustomerAgent"]

# NOTE: public re-export kept above in patch.


class BaseAgent:  # minimal base so subclasses compile
    """Skeleton for all agents. Real logic comes in later PRs."""

    name: str = "base"

    def run(self, prompt: str, **kwargs):  # noqa: ANN001 \u2013 narrow later
        raise NotImplementedError


class QuoteAgent(BaseAgent):
    name = "quote"

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

        # Query LLM for a short rationale so we exercise provider logic
        from backend.core.llm_provider import chat as call_llm

        llm_rationale = call_llm(
            f"Give one-sentence explanation for a ${total:.2f} window-cleaning quote."
        )

        quote_line = f"> \${total:,.2f} for cleaning {qty} windows in {suburb}"
        attribution = f"> — QuoteGPT, {year}"
        rationale = f"Rationale: {llm_rationale}"

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
        # local import to avoid heavy dep on start-up
        from backend.database import Quote, get_session

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


from .customer_agent import CustomerAgent  # noqa: E402
