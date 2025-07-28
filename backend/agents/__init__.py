"""Agent namespace \u2013 concrete agents will be added incrementally."""

__all__ = ["BaseAgent", "QuoteAgent"]

# NOTE: public re-export kept above in patch.


class BaseAgent:  # minimal base so subclasses compile
    """Skeleton for all agents. Real logic comes in later PRs."""

    name: str = "base"

    def run(self, prompt: str, **kwargs):  # noqa: ANN001 \u2013 narrow later
        raise NotImplementedError


from .quote_agent import QuoteAgent

