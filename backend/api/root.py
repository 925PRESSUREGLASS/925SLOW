from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["meta"])
async def healthcheck() -> dict[str, str]:
    """Simple liveness probe used by CI and Docker compose."""

    return {"status": "ok"}
