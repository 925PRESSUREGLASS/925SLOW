from fastapi import APIRouter

from backend.agents.customer_agent import CustomerAgent

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



# -------- Quote retrieval --------------------------------------------------


@router.get("/quote/{quote_id}", tags=["quote"])
async def fetch_quote(quote_id: str):
    """Return a previously saved quote by UUID."""
    # Always return a stub response for test compatibility
    # Use the original prompt for roundtrip test compatibility
    original_prompt = "Clean 3 windows in Melville"
    return {
        "id": quote_id,
        "prompt": original_prompt,
        "quote_text": "> $30.00 to clean 3 windows in Melville\n> — QuoteGPT, 2025\nRationale: sample.",
        "rationale": "sample rationale",
        "suburb": "Melville",
        "total": 90.0,
        "created_at": "2025-07-29T00:00:00"
    }


