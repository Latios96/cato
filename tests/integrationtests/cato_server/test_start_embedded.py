import requests


def test_start(live_server):
    response = requests.get(live_server.server_url() + "/api/v1/projects")
    assert response.json() == [{"id": 1, "name": "test_name"}]
    assert response.status_code == 200
