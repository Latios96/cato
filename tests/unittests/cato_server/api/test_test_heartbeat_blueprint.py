import datetime

from cato_common.utils.datetime_utils import aware_now_in_utc


def test_should_create_new_test_heartbeat(client_with_session, test_result):
    rv = client_with_session.post(f"/api/v1/test_heartbeats/{test_result.id}")

    assert rv.status_code == 200
    json = rv.json()
    assert json["id"] == 1
    assert json["testResultId"] == 1
    assert (
        aware_now_in_utc() - datetime.datetime.fromisoformat(json["lastBeat"])
    ).seconds < 1


def test_should_update_new_test_heartbeat(client_with_session, test_result):
    client_with_session.post(f"/api/v1/test_heartbeats/{test_result.id}")
    rv = client_with_session.post(f"/api/v1/test_heartbeats/{test_result.id}")

    assert rv.status_code == 200
    json = rv.json()
    assert json["id"] == 1
    assert json["testResultId"] == 1
    assert (
        aware_now_in_utc() - datetime.datetime.fromisoformat(json["lastBeat"])
    ).seconds < 1


def test_not_existing_test_result_id_should_400(client_with_session):
    rv = client_with_session.post("/api/v1/test_heartbeats/42")

    assert rv.status_code == 400
    assert rv.json() == {"testResultId": "No test result found with id 42"}


def test_should_create_new_test_heartbeat_for_run_id_and_test_identifier(
    client_with_session, run, test_result
):
    rv = client_with_session.post(
        f"/api/v1/test_heartbeats/run/{run.id}/{test_result.test_identifier.suite_name}/{test_result.test_identifier.test_name}"
    )

    assert rv.status_code == 200
    json = rv.json()
    assert json["id"] == 1
    assert json["testResultId"] == 1
    assert (
        aware_now_in_utc() - datetime.datetime.fromisoformat(json["lastBeat"])
    ).seconds < 1


def test_should_update_new_test_heartbeat_for_run_id_and_test_identifier(
    client_with_session, run, test_result
):
    rv = client_with_session.post(
        f"/api/v1/test_heartbeats/run/{run.id}/{test_result.test_identifier.suite_name}/{test_result.test_identifier.test_name}"
    )
    rv = client_with_session.post(
        f"/api/v1/test_heartbeats/run/{run.id}/{test_result.test_identifier.suite_name}/{test_result.test_identifier.test_name}"
    )

    assert rv.status_code == 200
    json = rv.json()
    assert json["id"] == 1
    assert json["testResultId"] == 1
    assert (
        aware_now_in_utc() - datetime.datetime.fromisoformat(json["lastBeat"])
    ).seconds < 1


def test_not_existing_test_result_id_should_400_for_run_id_and_test_identifier(
    client_with_session,
):
    rv = client_with_session.post(
        f"/api/v1/test_heartbeats/run/42/suite_name/test_name"
    )

    assert rv.status_code == 400
    assert rv.json() == {
        "runId": "No test result found with run id 42 and test identifier suite_name/test_name",
        "testIdentifier": "No test result found with run id 42 and test identifier suite_name/test_name",
    }
