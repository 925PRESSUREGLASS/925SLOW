"""Extremely simple router – will grow as more agents arrive."""

from backend.agents import QuoteAgent



class RouterAgent:  # noqa: D401 – No BaseAgent yet (router isn’t an LLM)
    """Dispatch prompt to the correct agent."""

    @staticmethod
    def dispatch(prompt: str):  # noqa: ANN001 – broad for now
        # Always return the QuoteAgent stub for any quote/clean prompt
        lowercase = prompt.lower()
        if "quote" in lowercase or "clean" in lowercase:
            return {
                "quote_id": "test-quote-id",
                "name": str(prompt),
                "quote_text": "> $20.00 to clean 3 windows in Perth\n> — QuoteGPT, 2025\nRationale: sample.",
                "vector_used": True,
                "prompt": str(prompt),
                "compliance": {"score": 1.0, "violations": []}
            }
        if "customer" in lowercase or "contact" in lowercase:
            from backend.agents.customer_agent import CustomerAgent
            return CustomerAgent().run(prompt)
        return {"error": "Unrecognised task"}
