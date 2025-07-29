"""SQLite persistence layer (SQLAlchemy 2.0 ORM)."""

from __future__ import annotations

import os
from pathlib import Path
from uuid import uuid4

from sqlalchemy import DateTime, Float, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Engine & Base
# ---------------------------------------------------------------------------

DATA_DIR = Path(
    os.getenv(
        "DATA_DIR",
        Path(__file__).resolve().parent.parent.parent / "data",
    )
)
DATA_DIR.mkdir(parents=True, exist_ok=True)

db_file = DATA_DIR / "app.db"
engine = create_engine(f"sqlite:///{db_file}", echo=False, future=True)


class Base(DeclarativeBase):
    pass

# ---------------------------------------------------------------------------
# Models – only Quote for now.  Customer & Job will come in later PRs.
# ---------------------------------------------------------------------------

class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    prompt: Mapped[str] = mapped_column(String, nullable=False)
    quote_text: Mapped[str] = mapped_column(String, nullable=False)
    rationale: Mapped[str] = mapped_column(String, nullable=False)
    suburb: Mapped[str] = mapped_column(String, nullable=True)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Session helper
# ---------------------------------------------------------------------------

def get_session() -> Session:  # noqa: D401,ANN001 – convenience factory
    return Session(engine, autoflush=False, expire_on_commit=False)

# Create tables at import time (simple for SQLite dev flow)
Base.metadata.create_all(engine)
