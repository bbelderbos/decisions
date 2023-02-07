import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app, get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_read_decisions(client: TestClient):
    response = client.get("/decisions")
    assert response.status_code == 200
    assert response.json() == []


@freeze_time("2023-01-06")
def test_post_new_decision(client: TestClient):
    payload = {
        "name": "sleep",
        "state_emotional": "string",
        "situation": "string",
        "problem_statement": "string",
        "variables": "string",
        "complications": "string",
        "alternatives": "string",
        "outcome_ranges": "string",
        "expected_with_probabilities": "string",
        "outcome": "string",
    }
    response = client.post("/decisions", json=payload)
    assert response.status_code == 200
    assert response.json() == {
        "time_made": None,
        "time_reviewed": None,
        "status": "Open",
        "review": None,
        "rating": None,
        "id": 1,
        "time_added": "2023-01-06",
        "name": "sleep",
        "state_emotional": "string",
        "situation": "string",
        "problem_statement": "string",
        "variables": "string",
        "complications": "string",
        "alternatives": "string",
        "outcome_ranges": "string",
        "expected_with_probabilities": "string",
        "outcome": "string",
    }
