from fastapi import APIRouter

from backend.agents.router_agent import RouterAgent
from backend.agents.memory_agent import MemoryAgent


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


# -------- Quote retrieval --------------------------------------------------


from backend.database import Quote, get_session  # placed here to avoid circular import earlier


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


# -------- Memory search endpoint ------------------------------------------


@router.post("/memory", tags=["memory"])
async def memory_search(request: dict[str, str]):  # noqa: ANN001 – minimal
    """Return top‑3 similar past quotes to the supplied `prompt`."""

    prompt: str = request.get("prompt", "")
    return MemoryAgent.run(prompt)

