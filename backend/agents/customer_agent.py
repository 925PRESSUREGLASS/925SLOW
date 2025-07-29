from __future__ import annotations

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
