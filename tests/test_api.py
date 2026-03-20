def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_shape(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_happy_path_adds_participant(client):
    email = "new.student@mergington.edu"

    signup_response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for Chess Club"

    activities_response = client.get("/activities")
    assert email in activities_response.json()["Chess Club"]["participants"]


def test_unregister_happy_path_removes_participant(client):
    email = "remove.student@mergington.edu"

    client.post("/activities/Chess Club/signup", params={"email": email})
    unregister_response = client.post("/activities/Chess Club/unregister", params={"email": email})

    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from Chess Club"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()["Chess Club"]["participants"]


def test_duplicate_signup_returns_400(client):
    email = "duplicate.student@mergington.edu"

    first_signup = client.post("/activities/Chess Club/signup", params={"email": email})
    second_signup = client.post("/activities/Chess Club/signup", params={"email": email})

    assert first_signup.status_code == 200
    assert second_signup.status_code == 400
    assert second_signup.json()["detail"] == "Student already signed up for this activity"