# SPDX-License-Identifier: MIT
import builtins
from importlib import reload


def test_stub_fallback(monkeypatch):
    """With no OPENAI key & no Ollama, provider should fall back to stub."""

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    import httpx

    def _raise(*_, **__):
        raise httpx.NetworkError("no server")

    monkeypatch.setattr(httpx.Client, "post", _raise)

    from backend.core import llm_provider

    reload(llm_provider)

    out = llm_provider.chat("hello")
    assert out.startswith("(stub)")
