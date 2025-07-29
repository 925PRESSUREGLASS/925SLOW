"""Extremely simple router – will grow as more agents arrive."""

from backend.agents.quote_agent import QuoteAgent


class RouterAgent:  # noqa: D401 – No BaseAgent yet (router isn’t an LLM)
    """Dispatch prompt to the correct agent."""

    @staticmethod
    def dispatch(prompt: str):  # noqa: ANN001 – broad for now
        # Always return the QuoteAgent stub for any quote/clean prompt
        lowercase = prompt.lower()
        if "quote" in lowercase or "clean" in lowercase:
            return QuoteAgent().run(prompt)
        if "customer" in lowercase or "contact" in lowercase:
            from backend.agents.customer_agent import CustomerAgent
            return CustomerAgent().run(prompt)
        return {"error": "Unrecognised task"}
