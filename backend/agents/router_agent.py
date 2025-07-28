"""Extremely simple router – will grow as more agents arrive."""

from backend.agents import QuoteAgent
from backend.agents.customer_agent import CustomerAgent
from backend.agents.job_agent import JobAgent


class RouterAgent:  # noqa: D401 – No BaseAgent yet (router isn’t an LLM)
    """Dispatch prompt to the correct agent."""

    @staticmethod
    def dispatch(prompt: str):  # noqa: ANN001 – broad for now
        lowercase = prompt.lower()
        if "quote" in lowercase or "clean" in lowercase:
            return QuoteAgent().run(prompt)
        if "customer" in lowercase or "contact" in lowercase:
            # naive – expects payload in API; CLI path could be improved later
            return {"error": "Customer task requires JSON payload via /customer"}
        if "job" in lowercase or "schedule" in lowercase:
            return {"error": "Job task requires JSON payload via /job"}
        return {"error": "Unrecognised task"}
