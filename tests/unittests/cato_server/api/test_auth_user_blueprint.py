def test_should_return_404_when_no_session_exists(client):
    response = client.get("/api/v1/users/whoami")

    assert response.status_code == 401


def test_should_return_user_from_session_with_fixtures(client_with_session):
    response = client_with_session.get("/api/v1/users/whoami")

    assert response.status_code == 200
    assert response.json() == {
        "email": "foo@bar.com",
        "fullname": "User Username",
        "id": 1,
        "username": "username",
    }
