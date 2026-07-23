from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={quote(email)}"
        )
        assert signup_response.status_code == 200

        unregister_response = client.delete(
            f"/activities/{activity_name}/participants/{quote(email)}"
        )
        assert unregister_response.status_code == 200

        activity = client.get("/activities").json()[activity_name]
        assert email not in activity["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants
