# SPDX-License-Identifier: MIT
"""Minimal Stripe helper – safe to import without real API keys.

In **CI / dev** it falls back to a deterministic stub so tests don’t reach the network.
"""

from __future__ import annotations

import os
import uuid

import stripe


def _is_enabled() -> bool:  # noqa: D401
    return os.getenv("STRIPE_SECRET_KEY") is not None


def create_invoice(
    email: str, amount_cents: int, currency: str = "aud"
) -> str:  # noqa: D401,ANN001
    """Return Stripe invoice ID or stub UUID if disabled."""

    if not _is_enabled():
        return f"stub-inv-{uuid.uuid4().hex[:12]}"

    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

    # 1. ensure customer exists / create one-off
    customers = stripe.Customer.search(query=f"email:'{email}'", limit=1)
    if customers.data:
        cust_id = customers.data[0].id
    else:
        cust = stripe.Customer.create(email=email)
        cust_id = cust.id

    # 2. create invoice item then invoice
    stripe.InvoiceItem.create(
        customer=cust_id,
        amount=amount_cents,
        currency=currency,
        description="Cleaning services",
    )
    inv = stripe.Invoice.create(customer=cust_id, auto_advance=True)

    return inv.id
