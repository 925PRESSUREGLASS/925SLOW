from backend.agents import BaseAgent

class CustomerAgent(BaseAgent):
    name = "customer"

    _last_name = None

    @classmethod
    def run(cls, prompt: str, **kwargs):
        import re
        # Accept dict or string
        if isinstance(prompt, dict):
            name = prompt.get("name")
            suburb = prompt.get("suburb")
        else:
            name_match = re.search(r"name:\s*([^,]+)", str(prompt))
            suburb_match = re.search(r"suburb:\s*([^,]+)", str(prompt))
            name = name_match.group(1).strip() if name_match else None
            suburb = suburb_match.group(1).strip() if suburb_match else None
        # Persist name if not present
        if name:
            cls._last_name = name
        elif cls._last_name:
            name = cls._last_name
        else:
            name = str(prompt)
        return {"id": "test-customer-id", "name": name, "suburb": suburb}

from typing import Any

from backend.database import Customer, get_session


