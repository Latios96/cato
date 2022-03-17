import datetime


def test_should_create_new_test_heartbeat(client, test_result):
    rv = client.post(f"/api/v1/test_heartbeats/{test_result.id}")

    assert rv.status_code == 200
    json = rv.json()
    assert json["id"] == 1
    assert json["testResultId"] == 1
    assert (
        datetime.datetime.now() - datetime.datetime.fromisoformat(json["lastBeat"])
    ).seconds < 1


def test_should_update_new_test_heartbeat(client, test_result):
    client.post(f"/api/v1/test_heartbeats/{test_result.id}")
    rv = client.post(f"/api/v1/test_heartbeats/{test_result.id}")

    assert rv.status_code == 200
    json = rv.json()
    assert json["id"] == 1
    assert json["testResultId"] == 1
    assert (
        datetime.datetime.now() - datetime.datetime.fromisoformat(json["lastBeat"])
    ).seconds < 1


def test_not_existing_test_result_id_should_400(client):
    rv = client.post("/api/v1/test_heartbeats/42")

    assert rv.status_code == 400
    assert rv.json() == {"testResultId": "No test result found with id 42"}


def test_should_create_new_test_heartbeat_for_run_id_and_test_identifier(
    client, run, test_result
):
    rv = client.post(
        f"/api/v1/test_heartbeats/run/{run.id}/{test_result.test_identifier.suite_name}/{test_result.test_identifier.test_name}"
    )

    assert rv.status_code == 200
    json = rv.json()
    assert json["id"] == 1
    assert json["testResultId"] == 1
    assert (
        datetime.datetime.now() - datetime.datetime.fromisoformat(json["lastBeat"])
    ).seconds < 1


def test_should_update_new_test_heartbeat_for_run_id_and_test_identifier(
    client, run, test_result
):
    rv = client.post(
        f"/api/v1/test_heartbeats/run/{run.id}/{test_result.test_identifier.suite_name}/{test_result.test_identifier.test_name}"
    )
    rv = client.post(
        f"/api/v1/test_heartbeats/run/{run.id}/{test_result.test_identifier.suite_name}/{test_result.test_identifier.test_name}"
    )

    assert rv.status_code == 200
    json = rv.json()
    assert json["id"] == 1
    assert json["testResultId"] == 1
    assert (
        datetime.datetime.now() - datetime.datetime.fromisoformat(json["lastBeat"])
    ).seconds < 1


def test_not_existing_test_result_id_should_400_for_run_id_and_test_identifier(client):
    rv = client.post(f"/api/v1/test_heartbeats/run/42/suite_name/test_name")

    assert rv.status_code == 400
    assert rv.json() == {
        "runId": "No test result found with run id 42 and test identifier suite_name/test_name",
        "testIdentifier": "No test result found with run id 42 and test identifier suite_name/test_name",
    }
