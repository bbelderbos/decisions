from app.main import app
from fastapi import FastAPI
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_decisions():
    response = client.get("/decisions")
    assert response.status_code == 404
    assert response.json() == {}
