from . import BaseAgent


class CustomerAgent(BaseAgent):
    """Placeholder for future customer management logic."""

    name = "customer"

    def run(self, prompt: str, **kwargs):  # noqa: D401,ANN001
        return {"message": "CustomerAgent stub"}
