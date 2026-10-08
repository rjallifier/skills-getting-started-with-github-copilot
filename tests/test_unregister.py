from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import activities, app


def test_unregister_participant():
    original = deepcopy(activities)
    try:
        with TestClient(app) as client:
            response = client.delete(
                "/activities/Chess%20Club/signup",
                params={"email": "michael@mergington.edu"},
            )
            assert response.status_code == 200
            assert response.json() == {
                "message": "Unregistered michael@mergington.edu from Chess Club"
            }
            updated = client.get("/activities").json()
            assert updated["Chess Club"]["participants"] == ["daniel@mergington.edu"]
            assert updated["Gym Class"] == original["Gym Class"]

            response = client.delete(
                "/activities/Chess%20Club/signup",
                params={"email": "michael@mergington.edu"},
            )
            assert response.status_code == 404
            assert response.json()["detail"] == "Student is not signed up for this activity"

            response = client.post(
                "/activities/Chess%20Club/signup",
                params={"email": "michael@mergington.edu"},
            )
            assert response.status_code == 200
    finally:
        activities.clear()
        activities.update(original)


def test_unregister_unknown_activity_does_not_change_registrations():
    original = deepcopy(activities)
    with TestClient(app) as client:
        response = client.delete(
            "/activities/Unknown/signup",
            params={"email": "michael@mergington.edu"},
        )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
    assert activities == original
