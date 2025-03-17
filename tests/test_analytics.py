import pytest
from db.engine import Base, engine
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def test_client():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    # Drop the database tables after tests
    Base.metadata.drop_all(bind=engine)


def test_analyze_notes(test_client):
    test_client.post("/notes/",
                     json={"title": "Note 1", "content": "This is the test note."})
    test_client.post("/notes/",
                     json={"title": "Note 2", "content": "This is the second test note."})

    response = test_client.get("/analytics")
    assert response.status_code == 200
    assert "total_word_count" in response.json()
    assert "average_note_length" in response.json()
    assert "most_common_words" in response.json()
    assert "top_3_longest_notes" in response.json()
    assert "top_3_shortest_notes" in response.json()
