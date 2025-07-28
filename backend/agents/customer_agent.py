"""CustomerAgent – create / update CRM records (local DB for now)."""

from __future__ import annotations

import json
from typing import Any

from backend.database import Customer, get_session


class CustomerAgent:  # noqa: D401 – not an LLM
    name = "customer"

    @staticmethod
    def run(payload: dict[str, Any]):  # noqa: D401,ANN001 – generic input
        """Create or update a customer.

        *Upsert* strategy keyed by `email` (required).
        Returns full customer record as dict.
        """

        email = payload.get("email")
        if not email:
            return {"error": "email is required"}

        with get_session() as sess:
            obj: Customer | None = (
                sess.query(Customer)
                .filter(Customer.email == email)
                .one_or_none()  # noqa: E501
            )

            if obj is None:
                obj = Customer(
                    email=email,
                    name=payload.get("name", "Unnamed"),
                )
                sess.add(obj)

            # update mutable fields
            obj.name = payload.get("name", obj.name)
            obj.phone = payload.get("phone", obj.phone)
            obj.suburb = payload.get("suburb", obj.suburb)
            if tags := payload.get("tags"):
                obj.tags = json.dumps(tags)

            sess.commit()

            return {
                "id": obj.id,
                "name": obj.name,
                "email": obj.email,
                "phone": obj.phone,
                "suburb": obj.suburb,
                "tags": json.loads(obj.tags) if obj.tags else [],
                "created_at": obj.created_at.isoformat(),
            }
