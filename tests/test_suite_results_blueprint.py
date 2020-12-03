import json

import pytest

from cato.storage.domain.suite_result import SuiteResult


def test_get_run_by_project_id_should_return(client, suite_result, run):
    url = "/api/v1/suite_results/run/{}".format(run.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == [
        {
            "id": 1,
            "run_id": 1,
            "suite_name": "my_suite",
            "suite_variables": {"key": "value"},
        }
    ]


def test_get_run_by_project_id_should_return_empty_list(client):
    url = "/api/v1/suite_results/run/42"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == []


@pytest.mark.parametrize(
    "data,errors",
    [
        (
            {},
            {
                "run_id": ["Missing data for required field."],
                "suite_name": ["Missing data for required field."],
                "suite_variables": ["Missing data for required field."],
            },
        ),
        (
            {"run_id": 2},
            {
                "run_id": ["No run with id 2 exists."],
                "suite_name": ["Missing data for required field."],
                "suite_variables": ["Missing data for required field."],
            },
        ),
        (
            {"run_id": 1, "suite_name": "yrsdt*$%$$"},
            {
                "suite_name": ["String does not match expected pattern."],
                "suite_variables": ["Missing data for required field."],
            },
        ),
        (
            {
                "run_id": 1,
                "suite_name": "suite_name",
                "suite_variables": {"Test": 6546565},
            },
            {
                "suite_variables": ["Not a mapping of str->str: Test=6546565"],
            },
        ),
    ],
)
def test_create_suite_result_invalid_data_should_not_create(data, errors, client, run):
    url = "/api/v1/suite_results"

    rv = client.post(url, json=data)

    assert rv.status_code == 400
    assert rv.get_json() == errors


def test_create_suite_result_should_create(client, run):
    url = "/api/v1/suite_results"

    data = dict(run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"})

    rv = client.post(url, json=data)

    assert rv.status_code == 201
    assert rv.get_json() == {
        "id": 1,
        "run_id": 1,
        "suite_name": "my_suite",
        "suite_variables": {"key": "value"},
    }
