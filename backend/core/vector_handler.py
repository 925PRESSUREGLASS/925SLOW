"""Thin wrapper around Chroma *local* client for semantic memory."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

if not hasattr(np, "float_"):  # numpy 2 removed the alias used by chromadb
    np.float_ = np.float64  # type: ignore[attr-defined]

import chromadb
from sentence_transformers import SentenceTransformer

_DATA = Path("data/vector_store")
_DATA.mkdir(parents=True, exist_ok=True)

_client = chromadb.PersistentClient(path=str(_DATA))

_collection = _client.get_or_create_collection("quotes")

# Very small, generic embedding model (all-MiniLM). OK for CPU dev-flow.
try:
    _model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception:  # pragma: no cover - network/model issues
    _model = None


def _embed(texts: list[str]) -> list[list[float]]:  # noqa: D401,ANN001
    if _model is None:
        return [[0.0] * 384 for _ in texts]
    return [vec.tolist() for vec in _model.encode(texts, convert_to_numpy=True)]


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------


def add_quote(quote_id: str, text: str, metadata: dict[str, Any] | None = None):  # noqa: ANN401
    """Store quote text + metadata in Chroma."""

    _collection.add(ids=[quote_id], documents=[text], metadatas=[metadata or {}], embeddings=_embed([text]))


def search(query: str, n_results: int = 3) -> list[dict[str, Any]]:  # noqa: D401,ANN001
    """Semantic search returning `{id, text, score}` dicts."""

    res = _collection.query(query_embeddings=_embed([query]), n_results=n_results)
    # Chroma returns lists; flatten
    out: list[dict[str, Any]] = []
    for ids, docs, dists in zip(res["ids"], res["documents"], res["distances"], strict=False):
        for _id, doc, dist in zip(ids, docs, dists, strict=False):
            out.append({"id": _id, "text": doc, "score": dist})
    return out
