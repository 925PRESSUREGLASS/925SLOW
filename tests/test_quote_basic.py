# SPDX-License-Identifier: MIT
from backend import create_app

from fastapi.testclient import TestClient


def test_quote_endpoint_blockquote():
    client = TestClient(create_app())
    resp = client.post("/quote", json={"prompt": "Clean 2 windows in Perth"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["quote_text"].startswith(">")  # Spec minimal
    assert "Perth" in body["quote_text"]
    assert "$20.00" in body["quote_text"]
    # SpecGuard embedded
    assert body["compliance"]["score"] >= 0.7
