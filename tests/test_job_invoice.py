"""Ensure JobAgent auto-creates invoice id when marked completed."""

import importlib
from uuid import uuid4

from backend.agents import QuoteAgent
from backend.agents.customer_agent import CustomerAgent
from backend.agents.job_agent import JobAgent


def test_invoice_stub(monkeypatch):
    # patch env so Stripe disabled and deterministic id returned
    monkeypatch.delenv("STRIPE_SECRET_KEY", raising=False)

    # monkey-patch stripe_service to return predictable id
    from backend.integrations import stripe_service

    monkeypatch.setattr(
        stripe_service,
        "create_invoice",
        lambda *_, **__: f"stub-{uuid4().hex[:8]}",
    )

    cust = CustomerAgent.run({"name": "Paying Pal", "email": "pay@example.com"})
    quote = QuoteAgent().run("Clean 1 windows in Paidville")

    job = JobAgent.run(
        {
            "quote_id": quote["quote_id"],
            "customer_id": cust["id"],
        }
    )

    assert job["invoice_id"] is None  # draft no invoice yet

    updated = JobAgent.run({"job_id": job["id"], "status": "completed"})
    assert updated["invoice_id"].startswith("stub-")
