from __future__ import annotations

from typing import Any

from backend.database import Customer, Job, Quote, get_session
from backend.integrations.stripe_service import create_invoice


class JobAgent:
    """Create or update Job entries linking customers and quotes."""

    name = "job"

    @staticmethod
    def run(payload: dict[str, Any]) -> dict[str, Any]:  # noqa: D401,ANN001
        with get_session() as sess:
            job_id = payload.get("job_id")
            if job_id:
                job: Job | None = sess.get(Job, job_id)
                if job is None:
                    return {"error": "job not found", "id": job_id}
                if payload.get("status"):
                    job.status = payload["status"]
                    if job.status == "completed" and job.invoice_id is None:
                        cust = sess.get(Customer, job.customer_id)
                        amount_cents = int(job.quote.total * 100)
                        job.invoice_id = create_invoice(cust.email, amount_cents)
                if payload.get("scheduled_date"):
                    job.scheduled_date = payload["scheduled_date"]
            else:
                job = Job(
                    quote_id=payload["quote_id"],
                    customer_id=payload["customer_id"],
                    scheduled_date=payload.get("scheduled_date"),
                )
                sess.add(job)
            sess.commit()
            return {
                "id": job.id,
                "quote_id": job.quote_id,
                "customer_id": job.customer_id,
                "status": job.status,
                "scheduled_date": job.scheduled_date if job.scheduled_date else None,
                "invoice_id": job.invoice_id,
            }
