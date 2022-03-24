import requests


def test_start(live_server):
    response = requests.get(live_server.server_url() + "/")
    assert response.status_code == 200
