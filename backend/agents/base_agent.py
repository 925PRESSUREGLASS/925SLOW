from __future__ import annotations

class BaseAgent:
    """Base class for all agents."""
    name: str

    @classmethod
    def run(cls, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement run()")
