"""SQLite persistence layer (SQLAlchemy 2.0 ORM)."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from slugify import slugify
from sqlalchemy import DateTime, Float, ForeignKey, String, create_engine
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session, mapped_column,
                            relationship)

# ---------------------------------------------------------------------------
# Engine & Base
# ---------------------------------------------------------------------------

DATA_DIR = Path(
    os.getenv("DATA_DIR", Path(__file__).resolve().parent.parent.parent / "data")
)
DATA_DIR.mkdir(parents=True, exist_ok=True)

db_file = DATA_DIR / "app.db"
engine = create_engine(f"sqlite:///{db_file}", echo=False, future=True)


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid4())
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid4())
    )
    prompt: Mapped[str] = mapped_column(String, nullable=False)
    quote_text: Mapped[str] = mapped_column(String, nullable=False)
    rationale: Mapped[str] = mapped_column(String, nullable=False)
    suburb: Mapped[str] = mapped_column(String, nullable=True)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


# ---------------------------------------------------------------------------
# Job model (new)
# ---------------------------------------------------------------------------


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid4())
    )

    customer_id: Mapped[str] = mapped_column(
        String, ForeignKey("customers.id"), nullable=False
    )
    quote_id: Mapped[str] = mapped_column(
        String, ForeignKey("quotes.id"), nullable=False
    )

    status: Mapped[str] = mapped_column(
        String, default="draft"
    )  # draft|confirmed|completed
    scheduled_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # relationships (lazy = select by default)
    customer = relationship("Customer")
    quote = relationship("Quote")


# ---------------------------------------------------------------------------
# Session helper
# ---------------------------------------------------------------------------


def get_session() -> Session:  # noqa: D401,ANN001 – convenience factory
    return Session(engine, autoflush=False, expire_on_commit=False)


# Create tables at import time (simple for SQLite dev flow)
Base.metadata.create_all(engine)
