from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

HEADERS = {"X-API-Key": "dev-secret-key"}

def test_monthly_costs():
    response = client.get("/api/v1/costs/monthly?period=2026-08", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "total_cost" in data
    assert "breakdown" in data

def test_costs_by_env():
    response = client.get("/api/v1/costs/by-environment?period=2026-08", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "by_environment" in data

def test_costs_by_team():
    response = client.get("/api/v1/costs/by-team?period=2026-08", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "by_team" in data
