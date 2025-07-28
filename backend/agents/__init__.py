"""Agent namespace with minimal implementations used in tests."""

from __future__ import annotations

from typing import Any


class BaseAgent:
    """Skeleton base class for all agents."""

    name: str = "base"

    def run(self, prompt: str, **kwargs: Any) -> Any:  # noqa: ANN401
        raise NotImplementedError


from .quote_agent import QuoteAgent
from .customer_agent import CustomerAgent
from .job_agent import JobAgent

__all__ = ["BaseAgent", "QuoteAgent", "CustomerAgent", "JobAgent"]


