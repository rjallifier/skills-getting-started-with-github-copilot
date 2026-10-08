from copy import deepcopy


def test_unregister_removes_participant_only_from_selected_activity(client, activity_data):
    # Arrange
    email = activity_data["Chess Club"]["participants"][0]
    expected = deepcopy(activity_data)
    expected["Chess Club"]["participants"].remove(email)

    # Act
    response = client.delete("/activities/Chess%20Club/signup", params={"email": email})
    updated = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    assert updated.status_code == 200
    assert updated.json() == expected


def test_unregister_unregistered_student_does_not_change_registrations(client, activity_data):
    # Arrange
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete("/activities/Chess%20Club/signup", params={"email": email})
    updated = client.get("/activities")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
    assert updated.status_code == 200
    assert updated.json() == activity_data


def test_unregister_unknown_activity_does_not_change_registrations(client, activity_data):
    # Arrange
    email = activity_data["Chess Club"]["participants"][0]

    # Act
    response = client.delete("/activities/Unknown/signup", params={"email": email})
    updated = client.get("/activities")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert updated.status_code == 200
    assert updated.json() == activity_data


def test_unregister_last_participant_leaves_empty_list(client, activity_data):
    # Arrange
    email = "new.student@mergington.edu"
    signup = client.post("/activities/Basketball%20Team/signup", params={"email": email})
    assert signup.status_code == 200

    # Act
    response = client.delete("/activities/Basketball%20Team/signup", params={"email": email})
    updated = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Basketball Team"}
    assert updated.status_code == 200
    assert updated.json() == activity_data
