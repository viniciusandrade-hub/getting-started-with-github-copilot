from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_get_activities_returns_activity_data():
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert activity_name in response.json()


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={quote(email)}"
        )

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
    finally:
        # Cleanup
        activities[activity_name]["participants"] = original_participants


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={quote(email)}"
        )
        assert signup_response.status_code == 200

        # Act
        unregister_response = client.delete(
            f"/activities/{activity_name}/participants/{quote(email)}"
        )

        # Assert
        assert unregister_response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        # Cleanup
        activities[activity_name]["participants"] = original_participants
