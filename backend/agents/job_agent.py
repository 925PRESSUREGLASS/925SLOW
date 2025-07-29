from . import BaseAgent


class JobAgent(BaseAgent):
    """Placeholder job management agent."""

    name = "job"

    def run(self, prompt: str, **kwargs):  # noqa: D401,ANN001
        return {"message": "JobAgent stub"}
