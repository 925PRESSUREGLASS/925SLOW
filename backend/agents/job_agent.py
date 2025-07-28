"""JobAgent – create/update jobs and trigger invoicing when completed."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from dateutil import parser

from backend.database import Customer, Job, Quote, get_session


class JobAgent:
    name = "job"

    @staticmethod
    def _parse_date(val: str | None) -> datetime | None:
        if not val:
            return None
        return parser.parse(val)

    @classmethod
    def run(cls, payload: dict[str, Any]):  # noqa: D401,ANN001
        job_id = payload.get("job_id")
        with get_session() as sess:
            if job_id:
                job: Job | None = sess.get(Job, job_id)
                if job is None:
                    return {"error": "job not found", "id": job_id}

                if payload.get("status"):
                    job.status = payload["status"]
                if payload.get("scheduled_date"):
                    job.scheduled_date = cls._parse_date(payload["scheduled_date"])
                if "notes" in payload:
                    job.notes = payload["notes"]

                # create invoice once when completed
                if job.status == "completed" and job.invoice_id is None:
                    from backend.integrations import stripe_service

                    job.invoice_id = stripe_service.create_invoice(
                        job.customer.email,
                        int(job.quote.total * 100),
                    )

                sess.commit()
            else:
                customer_id = payload.get("customer_id")
                quote_id = payload.get("quote_id")
                if not customer_id or not quote_id:
                    return {"error": "customer_id and quote_id required"}

                customer = sess.get(Customer, customer_id)
                quote = sess.get(Quote, quote_id)
                if customer is None or quote is None:
                    return {"error": "invalid ids"}

                job = Job(
                    customer_id=customer.id,
                    quote_id=quote.id,
                    status=payload.get("status", "draft"),
                    scheduled_date=cls._parse_date(payload.get("scheduled_date")),
                    notes=payload.get("notes"),
                    invoice_id=None,
                )
                sess.add(job)
                sess.commit()

            return {
                "id": job.id,
                "status": job.status,
                "scheduled_date": (
                    job.scheduled_date.isoformat() if job.scheduled_date else None
                ),
                "notes": job.notes,
                "quote_id": job.quote_id,
                "customer_id": job.customer_id,
                "created_at": job.created_at.isoformat(),
                "invoice_id": job.invoice_id,
            }
