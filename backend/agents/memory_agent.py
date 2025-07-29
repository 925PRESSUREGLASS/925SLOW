from . import BaseAgent


class MemoryAgent(BaseAgent):
    """Placeholder memory retrieval handler."""

    name = "memory"

    def run(self, prompt: str, **kwargs):  # noqa: D401,ANN001
        return {"message": "MemoryAgent stub"}
