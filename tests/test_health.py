# SPDX-License-Identifier: MIT
from fastapi.testclient import TestClient

from backend import create_app


def test_health_endpoint():
    client = TestClient(create_app())
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
