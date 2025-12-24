from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # ensure a known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_cycle():
    # Choose an activity and a test email
    activity = "Chess Club"
    test_email = "test.user@example.com"

    # Ensure email not already present
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")
    assert test_email in activities[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "Unregistered" in body.get("message", "")
    assert test_email not in activities[activity]["participants"]


def test_signup_duplicate_returns_400():
    activity = "Programming Class"
    # pick an existing participant
    existing = activities[activity]["participants"][0]

    resp = client.post(f"/activities/{activity}/signup?email={existing}")
    assert resp.status_code == 400


def test_unregister_not_registered_returns_400():
    activity = "Gym Class"
    fake_email = "not.registered@example.com"
    # ensure it's not there
    if fake_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(fake_email)

    resp = client.delete(f"/activities/{activity}/unregister?email={fake_email}")
    assert resp.status_code == 400
