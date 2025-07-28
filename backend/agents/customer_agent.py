from __future__ import annotations

from typing import Any

from backend.database import Customer, get_session


class CustomerAgent:  # noqa: D401 – orchestrator, no LLM
    name = "customer"

    @staticmethod
    def run(payload: dict[str, Any]):  # noqa: D401,ANN001
        """Create or update a customer record."""

        with get_session() as sess:
            if cid := payload.get("customer_id"):
                obj: Customer | None = sess.get(Customer, cid)
                if obj is None:
                    return {"error": "customer not found", "id": cid}

                if payload.get("name") is not None:
                    obj.name = payload["name"]
                if payload.get("email") is not None:
                    obj.email = payload["email"]
                if payload.get("phone") is not None:
                    obj.phone = payload["phone"]

                sess.commit()
                return CustomerAgent._to_dict(obj)

            name = payload.get("name")
            email = payload.get("email")
            if not name or not email:
                return {"error": "name and email required"}

            obj = sess.query(Customer).filter(Customer.email == email).one_or_none()
            if obj:
                obj.name = name
                if payload.get("phone") is not None:
                    obj.phone = payload["phone"]
            else:
                obj = Customer(name=name, email=email, phone=payload.get("phone"))
                sess.add(obj)
            sess.commit()
            return CustomerAgent._to_dict(obj)

    @staticmethod
    def _to_dict(obj: Customer):  # noqa: ANN001,D401
        return {
            "id": obj.id,
            "name": obj.name,
            "email": obj.email,
            "phone": obj.phone,
            "created_at": obj.created_at.isoformat(),
        }
