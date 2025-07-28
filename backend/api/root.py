from fastapi import APIRouter

from backend.agents.router_agent import RouterAgent


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

