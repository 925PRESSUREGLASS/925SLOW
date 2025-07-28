# SPDX-License-Identifier: MIT
from backend import create_app

from fastapi.testclient import TestClient


def test_quote_roundtrip():
    client = TestClient(create_app())

    prompt = "Clean 3 windows in Melville"
    post = client.post("/quote", json={"prompt": prompt})
    assert post.status_code == 200
    quote_id = post.json()["quote_id"]

    get = client.get(f"/quote/{quote_id}")
    assert get.status_code == 200
    body = get.json()
    assert body["prompt"] == prompt
    assert "$30.00" in body["quote_text"]
