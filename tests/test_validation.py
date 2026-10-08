import pytest


@pytest.mark.parametrize("method", ["POST", "DELETE"])
def test_missing_email_is_rejected_without_changing_registrations(client, activity_data, method):
    # Arrange
    url = "/activities/Chess%20Club/signup"

    # Act
    response = client.request(method, url)
    updated = client.get("/activities")

    # Assert
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"] == ["query", "email"] and error["type"] == "missing" for error in errors)
    assert updated.status_code == 200
    assert updated.json() == activity_data
