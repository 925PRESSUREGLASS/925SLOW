from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from backend.database import Customer, Job, Quote, get_session
from backend.integrations import stripe_service


class JobAgent:
    """Create or update cleaning jobs."""

    @staticmethod
    def run(payload: dict[str, Any]) -> dict[str, Any]:  # noqa: D401,ANN401
        job_id = payload.get("job_id")
        with get_session() as sess:
            if job_id:
                job = sess.get(Job, job_id)
                if job is None:
                    return {"error": "job not found", "id": job_id}
                if payload.get("status"):
                    job.status = payload["status"]
                    if job.status == "completed" and job.invoice_id is None:
                        customer = sess.get(Customer, job.customer_id)
                        quote = sess.get(Quote, job.quote_id)
                        if customer and quote:
                            job.invoice_id = stripe_service.create_invoice(
                                customer.email,
                                int(quote.total * 100),
                            )
                if payload.get("scheduled_date"):
                    job.scheduled_date = datetime.now(timezone.utc)
                sess.commit()
            else:
                job = Job(
                    customer_id=payload["customer_id"],
                    quote_id=payload["quote_id"],
                    scheduled_date=datetime.now(timezone.utc)
                    if payload.get("scheduled_date")
                    else None,
                )
                sess.add(job)
                sess.commit()
            result = {
                "id": job.id,
                "customer_id": job.customer_id,
                "quote_id": job.quote_id,
                "status": job.status,
                "scheduled_date": job.scheduled_date.isoformat()
                if job.scheduled_date
                else None,
                "invoice_id": job.invoice_id,
            }
        return result
