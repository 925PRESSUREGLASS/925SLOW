from __future__ import annotations

from typing import Any
from uuid import uuid4

from backend.database import Customer, get_session


class CustomerAgent:
    """Create or update customer records."""

    @staticmethod
    def run(payload: dict[str, Any]) -> dict[str, Any]:  # noqa: D401,ANN401
        email = payload["email"]
        with get_session() as sess:
            cust = sess.query(Customer).filter_by(email=email).first()
            if cust is None:
                cust = Customer(id=str(uuid4()), email=email, name=payload.get("name"))
                sess.add(cust)
            else:
                if payload.get("name"):
                    cust.name = payload["name"]
            sess.commit()
            name = cust.name
            cust_id = cust.id
        suburb = payload.get("suburb")
        return {
            "id": cust_id,
            "email": email,
            "name": name,
            "suburb": suburb,
        }
