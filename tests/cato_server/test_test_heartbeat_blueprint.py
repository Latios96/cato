import datetime


def test_should_create_new_test_heartbeat(client, test_result):
    rv = client.post(f"/api/v1/test_heartbeats/{test_result.id}")

    assert rv.status_code == 200
    json = rv.get_json()
    assert json["id"] == 1
    assert json["test_result_id"] == 1
    assert (
        datetime.datetime.now() - datetime.datetime.fromisoformat(json["last_beat"])
    ).seconds < 1


def test_should_update_new_test_heartbeat(client, test_result):
    client.post(f"/api/v1/test_heartbeats/{test_result.id}")
    rv = client.post(f"/api/v1/test_heartbeats/{test_result.id}")

    assert rv.status_code == 200
    json = rv.get_json()
    assert json["id"] == 1
    assert json["test_result_id"] == 1
    assert (
        datetime.datetime.now() - datetime.datetime.fromisoformat(json["last_beat"])
    ).seconds < 1


def test_not_existing_test_result_id_should_400(client):
    rv = client.post("/api/v1/test_heartbeats/42")

    assert rv.status_code == 400
    assert rv.get_json() == {"test_result_id": "No test result found with id 42"}
