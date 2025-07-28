# SPDX-License-Identifier: MIT
"""Backend package root for 925\u00a0Stack\u00a0AI."""

__all__ = [
    "create_app",
]

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Factory so tests / CLI can spin up the API easily."""

    from backend.api.root import router  # local import to avoid circular deps

    app = FastAPI(title="925\u00a0Stack\u00a0AI\u00a0API", version="0.1.0")
    app.include_router(router)
    return app
