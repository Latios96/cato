import pytest

from cato_server.api.suite_results_blueprint import _is_filtered
from cato_server.domain.run_status import RunStatus
from cato_server.storage.abstract.status_filter import StatusFilter
from cato_server.storage.abstract.suite_result_filter_options import (
    SuiteResultFilterOptions,
)


def test_get_suite_result_by_run_id_should_return(client, suite_result, run):
    url = "/api/v1/suite_results/run/{}".format(run.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == [
        {
            "id": 1,
            "run_id": 1,
            "status": "NOT_STARTED",
            "suite_name": "my_suite",
            "suite_variables": {"key": "value"},
        }
    ]


def test_get_suite_result_by_run_id_filtered_should_return(client, suite_result, run):
    url = "/api/v1/suite_results/run/{}?statusFilter=NOT_STARTED".format(run.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == [
        {
            "id": 1,
            "run_id": 1,
            "status": "NOT_STARTED",
            "suite_name": "my_suite",
            "suite_variables": {"key": "value"},
        }
    ]


def test_get_suite_result_by_run_id_should_return_empty_list(client):
    url = "/api/v1/suite_results/run/42"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == []


def test_get_suite_by_run_id_paged_should_return(client, suite_result, run):
    url = "/api/v1/suite_results/run/{}?page_number=1&page_size=10".format(run.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [
            {
                "id": 1,
                "run_id": 1,
                "status": "NOT_STARTED",
                "suite_name": "my_suite",
                "suite_variables": {"key": "value"},
            }
        ],
        "page_number": 1,
        "page_size": 10,
        "total_entity_count": 1,
    }


def test_get_suite_by_run_id_paged_and_filtered_should_return(
    client, suite_result, run
):
    url = "/api/v1/suite_results/run/{}?page_number=1&page_size=10&statusFilter=NOT_STARTED".format(
        run.id
    )

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [
            {
                "id": 1,
                "run_id": 1,
                "status": "NOT_STARTED",
                "suite_name": "my_suite",
                "suite_variables": {"key": "value"},
            }
        ],
        "page_number": 1,
        "page_size": 10,
        "total_entity_count": 1,
    }


def test_get_suite_by_run_id_pages_should_return_empty_page(client, project):
    url = "/api/v1/suite_results/run/{}?page_number=1&page_size=10".format(project.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [],
        "page_number": 1,
        "page_size": 10,
        "total_entity_count": 0,
    }


def test_get_by_id_should_find(client, suite_result):
    url = f"/api/v1/suite_results/{suite_result.id}"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "id": 1,
        "runId": 1,
        "suite_name": "my_suite",
        "suite_variables": {"key": "value"},
        "tests": [],
    }


def test_get_by_id_should_find_should_contain_no_tests(
    client, suite_result, test_result
):
    url = f"/api/v1/suite_results/{suite_result.id}"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "id": 1,
        "runId": 1,
        "suite_name": "my_suite",
        "suite_variables": {"key": "value"},
        "tests": [
            {
                "execution_status": "NOT_STARTED",
                "id": 1,
                "name": "my_test_name",
                "status": "SUCCESS",
                "test_identifier": "my_suite/my_test_name",
                "thumbnail_file_id": None,
            }
        ],
    }


def test_get_by_id_should_404(client):
    url = "/api/v1/suite_results/42"

    rv = client.get(url)

    assert rv.status_code == 404


@pytest.mark.parametrize(
    "status_filter,status,expected_result",
    [
        (StatusFilter.NONE, RunStatus.NOT_STARTED, False),
        (StatusFilter.NONE, RunStatus.RUNNING, False),
        (StatusFilter.NONE, RunStatus.FAILED, False),
        (StatusFilter.NONE, RunStatus.SUCCESS, False),
        (StatusFilter.NOT_STARTED, RunStatus.NOT_STARTED, False),
        (StatusFilter.NOT_STARTED, RunStatus.RUNNING, True),
        (StatusFilter.NOT_STARTED, RunStatus.FAILED, True),
        (StatusFilter.NOT_STARTED, RunStatus.SUCCESS, True),
        (StatusFilter.RUNNING, RunStatus.NOT_STARTED, True),
        (StatusFilter.RUNNING, RunStatus.RUNNING, False),
        (StatusFilter.RUNNING, RunStatus.FAILED, True),
        (StatusFilter.RUNNING, RunStatus.SUCCESS, True),
        (StatusFilter.FAILED, RunStatus.NOT_STARTED, True),
        (StatusFilter.FAILED, RunStatus.RUNNING, True),
        (StatusFilter.FAILED, RunStatus.FAILED, False),
        (StatusFilter.FAILED, RunStatus.SUCCESS, True),
        (StatusFilter.SUCCESS, RunStatus.NOT_STARTED, True),
        (StatusFilter.SUCCESS, RunStatus.RUNNING, True),
        (StatusFilter.SUCCESS, RunStatus.FAILED, True),
        (StatusFilter.SUCCESS, RunStatus.SUCCESS, False),
    ],
)
def test_if_filtered(status_filter, status, expected_result):
    assert (
        _is_filtered(SuiteResultFilterOptions(status_filter), status) == expected_result
    )
