import pytest
from fastapi.testclient import TestClient

from db.engine import Base, engine
from main import app


@pytest.fixture(scope="module")
def test_client():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    # Drop the database tables after tests
    Base.metadata.drop_all(bind=engine)


def test_create_note(test_client):
    response = test_client.post("/notes/",
                                json={"title": "Test note",
                                      "content": "Test note content."})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["title"] == "Test note"
    assert response.json()["content"] == "Test note content."


def test_get_note(test_client):
    create_response = test_client.post("/notes/",
                                       json={"title": "Test note",
                                             "content": "Test note content."})
    note_id = create_response.json()["id"]

    response = test_client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["title"] == "Test note"
    assert response.json()["content"] == "Test note content."


def test_note_not_found(test_client):
    response = test_client.get("/notes/9999")  # Assuming 9999 does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"
