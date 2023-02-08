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


@pytest.fixture
def add_payload():
    return {
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


@pytest.fixture
def update_payload():
    return {
        "time_made": "2023-02-04",
        "time_reviewed": "2023-02-06",
        "status": "Made",
        "review": "was good to get some more sleep!",
        "rating": 10,
    }


def test_read_decisions(client: TestClient):
    response = client.get("/decisions")
    assert response.status_code == 200
    assert response.json() == []


@freeze_time("2023-01-06")
def test_post_new_decision(client: TestClient, add_payload: dict):
    response = client.post("/decisions", json=add_payload)
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


def test_get_decision_after_creating_it(client: TestClient, add_payload: dict):
    response = client.post("/decisions", json=add_payload)
    # via all decisions endpoint
    response = client.get("/decisions")
    assert response.status_code == 200
    expected = [
        {
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
            "time_made": None,
            "time_reviewed": None,
            "status": "Open",
            "review": None,
            "rating": None,
            "id": 1,
        }
    ]
    assert response.json() == expected
    # via single decision endpoint
    response = client.get("/decisions/1")
    assert response.status_code == 200
    assert response.json() == expected[0]


def test_get_or_update_non_existing_decision(client: TestClient, update_payload: dict):
    response = client.get("/decisions/7")
    assert response.status_code == 404
    response = client.put("/decisions/7", json=update_payload)
    assert response.status_code == 404


@freeze_time("2023-01-06")
def test_update_decision(client: TestClient, add_payload: dict, update_payload: dict):
    response = client.post("/decisions", json=add_payload)
    response = client.put("/decisions/1", json=update_payload)
    assert response.status_code == 200
    assert response.json() == {
        "time_made": "2023-02-04",
        "time_reviewed": "2023-02-06",
        "status": "Made",
        "review": "was good to get some more sleep!",
        "rating": 10,
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
