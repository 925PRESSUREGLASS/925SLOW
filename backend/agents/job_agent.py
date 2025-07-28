"""JobAgent – create & update job lifecycle records."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from dateutil import parser as dtparse

from backend.database import Customer, Job, Quote, get_session


class JobAgent:  # noqa: D401 – orchestrator, no LLM
    name = "job"

    @staticmethod
    def _parse_date(raw: str | None) -> datetime | None:  # noqa: ANN001
        if not raw:
            return None
        try:
            return dtparse.parse(raw, fuzzy=True)
        except (ValueError, OverflowError):
            return None

    @classmethod
    def run(cls, payload: dict[str, Any]):  # noqa: D401,ANN001
        """Create **or** update a Job.

        Required on *create*: `quote_id` **and** `customer_id` *or* `customer_email`.
        Optional: `scheduled_date`, `status`, `notes`.
        If `job_id` is supplied, perform an **update** instead.
        """

        with get_session() as sess:
            # --------------------------------------------------------------
            # Update flow
            # --------------------------------------------------------------

            if job_id := payload.get("job_id"):
                job: Job | None = sess.get(Job, job_id)
                if job is None:
                    return {"error": "job not found", "id": job_id}

                if payload.get("status"):
                    job.status = payload["status"]
                if payload.get("scheduled_date"):
                    if dt := cls._parse_date(payload["scheduled_date"]):
                        job.scheduled_date = dt
                if payload.get("notes") is not None:
                    job.notes = payload["notes"]

                sess.commit()
                return cls._to_dict(job)

            # --------------------------------------------------------------
            # Create flow – need quote & customer
            # --------------------------------------------------------------

            quote_id = payload.get("quote_id")
            if not quote_id:
                return {"error": "quote_id is required"}

            quote: Quote | None = sess.get(Quote, quote_id)
            if quote is None:
                return {"error": "quote not found", "id": quote_id}

            # Customer retrieval by id or email
            customer: Customer | None = None
            if cid := payload.get("customer_id"):
                customer = sess.get(Customer, cid)
            elif email := payload.get("customer_email"):
                customer = (
                    sess.query(Customer).filter(Customer.email == email).one_or_none()
                )

            if customer is None:
                return {"error": "customer not found / unspecified"}

            job = Job(
                customer_id=customer.id,
                quote_id=quote.id,
                status=payload.get("status", "draft"),
                scheduled_date=cls._parse_date(payload.get("scheduled_date")),
                notes=payload.get("notes"),
            )

            sess.add(job)
            sess.commit()

            return cls._to_dict(job)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _to_dict(job: Job):  # noqa: D401,ANN001 – simple converter
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
        }
