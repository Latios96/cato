def test_should_pass_without_header(client):
    # todo this will be changed once we enforce Authentication
    response = client.get("/api/v1/api_tokens/is_valid")
    assert response.status_code == 200


def test_should_fail_with_invalid_token(client):
    response = client.get(
        "/api/v1/api_tokens/is_valid", headers={"Authorization": "Bearer test"}
    )
    assert response.status_code == 401


def test_should_pass_with_valid_header(client, api_token_str):
    s = str(api_token_str.to_bearer())
    response = client.get("/api/v1/api_tokens/is_valid", headers={"Authorization": s})

    assert response.status_code == 200
