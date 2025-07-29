from fastapi.testclient import TestClient
from backend.api.root import app

client = TestClient(app)

def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_generate_quote():
    response = client.post("/quote", json={"prompt": "Test prompt"})
    assert response.status_code == 200
    # Optionally check response structure if RouterAgent.dispatch is implemented

def test_fetch_quote():
    quote_id = "test-uuid"
    response = client.get(f"/quote/{quote_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == quote_id
    assert data["prompt"] == "Clean 3 windows in Melville"