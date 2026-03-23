import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Chess Club/signup", params={"email": "test@example.com"})
    assert response.status_code == 200
    assert "Signed up test@example.com for Chess Club" in response.json()["message"]
    
    # Test duplicate signup
    response = client.post("/activities/Chess Club/signup", params={"email": "test@example.com"})
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "test@example.com"})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_remove_participant():
    # First signup
    client.post("/activities/Programming Class/signup", params={"email": "remove@example.com"})
    # Then remove
    response = client.delete("/activities/Programming Class/participants", params={"email": "remove@example.com"})
    assert response.status_code == 200
    assert "Removed remove@example.com from Programming Class" in response.json()["message"]

def test_remove_nonexistent_participant():
    response = client.delete("/activities/Programming Class/participants", params={"email": "nonexistent@example.com"})
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]