from fastapi import APIRouter

from backend.agents.customer_agent import CustomerAgent
from backend.agents.job_agent import JobAgent
from backend.agents.router_agent import RouterAgent
from backend.database import (  # placed here to avoid circular import earlier
    Quote, get_session)

router = APIRouter()


@router.get("/health", tags=["meta"])
async def healthcheck() -> dict[str, str]:
    """Simple liveness probe used by CI and Docker compose."""
    return {"status": "ok"}


# -------- Quote endpoint ---------------------------------------------------


@router.post("/quote", tags=["quote"])
async def generate_quote(request: dict[str, str]):  # noqa: ANN001 – minimal
    """Accept `{ "prompt": "…" }` and return QuoteAgent JSON output."""
    prompt: str = request.get("prompt", "")
    return RouterAgent.dispatch(prompt)


# -------- Customer helpers -------------------------------------------------


@router.post("/customer", tags=["customer"])
async def upsert_customer(body: dict):  # noqa: ANN001 – FastAPI will coerce JSON
    return CustomerAgent.run(body)


# -------- Quote retrieval --------------------------------------------------


@router.get("/quote/{quote_id}", tags=["quote"])
async def fetch_quote(quote_id: str):
    """Return a previously saved quote by UUID."""
    with get_session() as sess:
        obj: Quote | None = sess.get(Quote, quote_id)
        if obj is None:
            return {"error": "quote not found", "id": quote_id}
        return {
            "id": obj.id,
            "prompt": obj.prompt,
            "quote_text": obj.quote_text,
            "rationale": obj.rationale,
            "suburb": obj.suburb,
            "total": obj.total,
            "created_at": obj.created_at.isoformat(),
        }


# -------- Job lifecycle ----------------------------------------------------


@router.post("/job", tags=["job"])
async def upsert_job(body: dict):  # noqa: ANN001
    """Create a new job or update an existing one.

    *Create* requires `quote_id` + `customer_id` **or** `customer_email`.
    *Update* requires `job_id` plus any fields to change.
    """

    return JobAgent.run(body)


@router.get("/job/{job_id}", tags=["job"])
async def get_job(job_id: str):
    with get_session() as sess:
        from backend.database import \
            Job  # local import to avoid top-level circular

        job: Job | None = sess.get(Job, job_id)
        if job is None:
            return {"error": "job not found", "id": job_id}
        return JobAgent._to_dict(job)
