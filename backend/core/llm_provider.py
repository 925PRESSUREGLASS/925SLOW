"""Unified LLM interface with **fallback order**: GPT-4 -> Ollama -> stub.

* Reads provider + model from `config.yaml` (loaded by ``core.load_config``).
* For OpenAI, pulls ``OPENAI_API_KEY`` from env.
* Ollama requests local HTTP endpoint (no auth by default).
* On any exception, drops down to the next provider.
"""

from __future__ import annotations

import os
from typing import Any

import httpx
import openai

from backend.core import load_config

_cfg = load_config().get("llm", {})


# ---------------------------------------------------------------------------
# OpenAI driver
# ---------------------------------------------------------------------------

def _openai_chat(prompt: str) -> str:  # noqa: D401,ANN001
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")

    openai.api_key = key

    model = _cfg.get("openai", {}).get("model", "gpt-4o-mini")
    temperature = float(_cfg.get("openai", {}).get("temperature", 0.2))

    resp = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )

    return resp.choices[0].message.content.strip()


# ---------------------------------------------------------------------------
# Ollama driver (local inference)
# ---------------------------------------------------------------------------

def _ollama_chat(prompt: str) -> str:  # noqa: D401,ANN001
    host = _cfg.get("ollama", {}).get("host", "http://localhost:11434")
    model = _cfg.get("ollama", {}).get("model", "mistral")

    payload = {"model": model, "prompt": prompt, "stream": False}
    with httpx.Client(timeout=60) as client:
        resp = client.post(f"{host}/api/generate", json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", "").strip()


# ---------------------------------------------------------------------------
# Public helper – tries each driver in order
# ---------------------------------------------------------------------------

def chat(prompt: str) -> str:  # noqa: D401,ANN001 – primary entry point
    provider = _cfg.get("provider", "openai").lower()

    drivers: list[tuple[str, Any]] = []
    if provider == "openai":
        drivers = [("openai", _openai_chat), ("ollama", _ollama_chat)]
    elif provider == "ollama":
        drivers = [("ollama", _ollama_chat), ("openai", _openai_chat)]

    # fallback stub (deterministic)
    drivers.append(("stub", lambda p: f"(stub) {p[::-1]}"))

    last_err: Exception | None = None
    for name, fn in drivers:
        try:
            return fn(prompt)
        except Exception as err:  # noqa: BLE001
            last_err = err
            continue

    raise RuntimeError(f"All LLM providers failed: {last_err}")

