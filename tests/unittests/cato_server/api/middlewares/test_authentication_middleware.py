def test_should_pass_without_header(client):
    # todo this will be changed once we enforce Authentication
    response = client.get("/")
    assert response.status_code == 200


def test_should_fail_with_invalid_token(client):
    response = client.get("/", headers={"Authorization": "Bearer test"})
    assert response.status_code == 401


def test_should_pass_with_valid_header(client, api_token_str):
    s = str(api_token_str.to_bearer())
    response = client.get("/", headers={"Authorization": s})

    assert response.status_code == 200
