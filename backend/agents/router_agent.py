"""Extremely simple router – will grow as more agents arrive."""

from backend.agents.quote_agent import QuoteAgent
from backend.agents.memory_agent import MemoryAgent


class RouterAgent:  # noqa: D401 – No BaseAgent yet (router isn’t an LLM)
    """Dispatch prompt to the correct agent."""

    @staticmethod
    def dispatch(prompt: str):  # noqa: ANN001 – broad for now
        lowercase = prompt.lower()
        if "quote" in lowercase or "clean" in lowercase:
            return QuoteAgent().run(prompt)
        if "history" in lowercase or "similar" in lowercase or "memory" in lowercase:
            return MemoryAgent.run(prompt)
        return {"error": "Unrecognised task"}
