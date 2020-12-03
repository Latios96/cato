import pytest


def test_get_test_result_by_suite_and_identifier_should_return(
    client, suite_result, test_result
):
    url = "/api/v1/test_results/suite_result/{suite_result_id}/{suite_name}/{test_name}".format(
        suite_result_id=suite_result.id,
        suite_name=suite_result.suite_name,
        test_name=test_result.test_name,
    )

    rv = client.get(url)

    assert rv.status_code == 200
    json = rv.get_json()
    assert json["id"] == 1
    assert json.get("output") is None


def test_get_test_result_by_suite_and_identifier_should_404(client):
    url = "/api/v1/test_results/suite_result/1/suite_name/test_name"

    rv = client.get(url)

    assert rv.status_code == 404


def test_get_test_result_by_suite_id_should_return(client, suite_result, test_result):
    url = "/api/v1/test_results/suite_result/{suite_result_id}".format(
        suite_result_id=suite_result.id
    )

    rv = client.get(url)

    assert rv.status_code == 200
    json = rv.get_json()
    assert len(json) == 1
    assert json[0]["id"] == 1
    assert json[0].get("output") is None


def test_get_test_result_by_suite_id_should_return_empty_list(
    client, suite_result, test_result
):
    url = "/api/v1/test_results/suite_result/42".format(suite_result_id=suite_result.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == []


def test_get_test_result_output_should_return(client, test_result):
    url = "/api/v1/test_results/{}/output".format(test_result.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == ["1", "2", "3"]


def test_get_test_result_output_should_404(client, test_result):
    url = "/api/v1/test_results/42/output"

    rv = client.get(url)

    assert rv.status_code == 404
