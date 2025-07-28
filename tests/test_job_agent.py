# SPDX-License-Identifier: MIT
from backend.agents.customer_agent import CustomerAgent
from backend.agents.job_agent import JobAgent
from backend.agents.quote_agent import QuoteAgent


def test_job_create_and_update():
    # set up customer & quote
    cust = CustomerAgent.run({"name": "Bob", "email": "bob@example.com"})
    quote = QuoteAgent().run("Clean 5 windows in Bobsville")

    create = JobAgent.run(
        {
            "quote_id": quote["quote_id"],
            "customer_id": cust["id"],
            "scheduled_date": "next Monday 9am",
        }
    )

    assert create["status"] == "draft"
    assert create["scheduled_date"] is not None

    update = JobAgent.run({"job_id": create["id"], "status": "confirmed"})
    assert update["status"] == "confirmed"
