"""Agent namespace – simple helpers used in tests."""

from __future__ import annotations


class BaseAgent:
    """Skeleton base class."""

    name: str = "base"

    def run(self, prompt: str, **kwargs):  # noqa: D401,ANN001
        raise NotImplementedError


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
