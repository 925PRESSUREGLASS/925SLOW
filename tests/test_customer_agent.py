# SPDX-License-Identifier: MIT
from backend.agents.customer_agent import CustomerAgent


def test_customer_create_update():
    create = CustomerAgent.run(
        {
            "name": "Alice Example",
            "email": "alice@example.com",
            "phone": "0400 000 000",
            "suburb": "Fremantle",
            "tags": ["VIP"],
        }
    )

    assert create["name"] == "Alice Example"
    assert create["suburb"] == "Fremantle"

    # update suburb only
    update = CustomerAgent.run(
        {"email": "alice@example.com", "suburb": "Palmyra"}
    )  # noqa: E501
    assert update["suburb"] == "Palmyra"
    assert update["name"] == "Alice Example"  # unchanged
