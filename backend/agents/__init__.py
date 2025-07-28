"""Agent namespace \u2013 concrete agents will be added incrementally."""

from importlib import metadata

__all__ = ["BaseAgent", "QuoteAgent"]


class BaseAgent:  # minimal base so subclasses compile
    """Skeleton for all agents. Real logic comes in later PRs."""

    name: str = "base"

    def run(self, prompt: str, **kwargs):  # noqa: ANN001 \u2013 narrow later
        raise NotImplementedError


class QuoteAgent(BaseAgent):
    name = "quote"

    def run(self, prompt: str, **kwargs):  # noqa: D401,ANN001
        """Temporary stub \u2013 returns a placeholder until SpecGuard & pricing arrive."""

        return {
            "quote_text": "> $0.00 \u2013 Placeholder quote",  # SpecGuard\u2011compliant shape
            "rationale": "QuoteAgent stub; replace with real logic.",
        }

