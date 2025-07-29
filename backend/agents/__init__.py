from __future__ import annotations

from .base_agent import BaseAgent
from .customer_agent import CustomerAgent
from .job_agent import JobAgent
from .memory_agent import MemoryAgent
from .quote_agent import QuoteAgent

"""Agent namespace – simple helpers used in tests."""

__all__ = [
    "BaseAgent",
    "QuoteAgent",
    "CustomerAgent",
    "MemoryAgent",
    "JobAgent",
]