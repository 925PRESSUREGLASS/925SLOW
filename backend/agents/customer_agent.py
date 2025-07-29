from __future__ import annotations
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


class CustomerAgent:
    """Simple create/update helper for Customer rows."""

    name = "customer"

    @staticmethod
    def run(payload: dict[str, Any]) -> dict[str, Any]:  # noqa: D401,ANN001
        email = payload.get("email")
        if not email:
            return {"error": "email required"}

        with get_session() as sess:
            obj = sess.query(Customer).filter(Customer.email == email).one_or_none()
            if obj is None:
                obj = Customer(
                    name=payload.get("name"),
                    email=email,
                    phone=payload.get("phone"),
                    suburb=payload.get("suburb"),
                    tags=(
                        ",".join(payload.get("tags", []))
                        if payload.get("tags")
                        else None
                    ),
                )
                sess.add(obj)
            else:
                if payload.get("name"):
                    obj.name = payload["name"]
                if payload.get("phone"):
                    obj.phone = payload["phone"]
                if payload.get("suburb"):
                    obj.suburb = payload["suburb"]
                if payload.get("tags") is not None:
                    obj.tags = ",".join(payload.get("tags", []))
            sess.commit()
            return {
                "id": obj.id,
                "name": obj.name,
                "email": obj.email,
                "phone": obj.phone,
                "suburb": obj.suburb,
                "tags": obj.tags.split(",") if obj.tags else [],
            }
