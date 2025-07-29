"""Agent namespace – concrete agents will be added incrementally."""


class BaseAgent:  # minimal base so subclasses compile
    """Skeleton for all agents. Real logic comes in later PRs."""

    name: str = "base"

    def run(self, prompt: str, **kwargs):  # noqa: ANN001 – narrow later
        raise NotImplementedError


# Stubs for upcoming agents
from .customer_agent import CustomerAgent
from .job_agent import JobAgent
from .memory_agent import MemoryAgent
from .quote_agent import QuoteAgent

__all__ = [
    "BaseAgent",
    "QuoteAgent",
    "CustomerAgent",
    "MemoryAgent",
    "JobAgent",
]
