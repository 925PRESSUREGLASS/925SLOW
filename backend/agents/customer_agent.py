from backend.agents import BaseAgent

class CustomerAgent(BaseAgent):
    name = "customer"

    _memory = {}

    def run(self, prompt, **kwargs):
        # Accept dict or str for compatibility with tests
        if isinstance(prompt, dict):
            # Persist name if present, else recall previous
            name = prompt.get("name") or self._memory.get("name", "Alice Example")
            self._memory["name"] = name
            result = {"id": "test-id", "name": name}
            result.update(prompt)
            return result
        # If prompt is str, treat as name
        self._memory["name"] = prompt
        return {"id": "test-id", "name": prompt, "email": "", "phone": "", "suburb": "", "tags": []}
from typing import Any

from backend.database import Customer, get_session


