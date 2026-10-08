from copy import deepcopy


def test_signup_adds_participant_only_to_selected_activity(client, activity_data):
    # Arrange
    email = "new.student@mergington.edu"
    expected = deepcopy(activity_data)
    expected["Chess Club"]["participants"].append(email)

    # Act
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})
    updated = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert updated.status_code == 200
    assert updated.json() == expected


def test_duplicate_signup_is_rejected_without_changing_registrations(client, activity_data):
    # Arrange
    email = activity_data["Chess Club"]["participants"][0]

    # Act
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})
    updated = client.get("/activities")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}
    assert updated.status_code == 200
    assert updated.json() == activity_data


def test_signup_unknown_activity_does_not_change_registrations(client, activity_data):
    # Arrange
    email = "new.student@mergington.edu"

    # Act
    response = client.post("/activities/Unknown/signup", params={"email": email})
    updated = client.get("/activities")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert updated.status_code == 200
    assert updated.json() == activity_data


def test_participant_can_sign_up_again_after_unregistering(client, activity_data):
    # Arrange
    email = "new.student@mergington.edu"
    url = "/activities/Chess%20Club/signup"
    expected = deepcopy(activity_data)
    expected["Chess Club"]["participants"].append(email)

    # Act
    signup = client.post(url, params={"email": email})
    unregister = client.delete(url, params={"email": email})
    signup_again = client.post(url, params={"email": email})
    updated = client.get("/activities")

    # Assert
    assert signup.status_code == 200
    assert unregister.status_code == 200
    assert signup_again.status_code == 200
    assert signup_again.json() == {"message": f"Signed up {email} for Chess Club"}
    assert updated.status_code == 200
    assert updated.json() == expected
