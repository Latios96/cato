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


def test_create_suite_result_should_not_create(client, run):
    url = "/api/v1/suite_results"

    data = dict(run_id=42, suite_name="my_suite", suite_variables={"key": "value"})

    rv = client.post(url, json=data)

    assert rv.status_code == 400
    assert rv.get_json() == {"run_id": ["No run with id 42 exists."]}
