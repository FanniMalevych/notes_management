import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from db.engine import Base, engine


@pytest.fixture(scope="module")
def test_client():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    # Drop the database tables after tests
    Base.metadata.drop_all(bind=engine)


@patch('ai_integration.summarize_note_with_gemini')
def test_summarize_note_success(mock_summarize, test_client):
    # Mock the summarize function to return a summary
    mock_summarize.return_value = "This is a summary."

    # Create a note in the database for testing
    create_response = test_client.post("/api/notes/", json={"title": "Test Note", "content": "This is a test note."})
    note_id = create_response.json()["id"]

    # Call the summarize endpoint
    response = test_client.post(f"/notes/summarize/{note_id}")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"note_id": note_id, "summary": "This is a summary."}
    mock_summarize.assert_called_once_with("This is a test note.")


@patch('ai_integration.summarize_note_with_gemini')
def test_summarize_note_not_found(mock_summarize, test_client):
    # Call the summarize endpoint with a non-existent note ID
    response = test_client.post("/notes/summarize/999")  # Assuming 999 does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"