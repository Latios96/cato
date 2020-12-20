def test_get_suite_result_by_run_id_should_return(client, suite_result, run):
    url = "/api/v1/suite_results/run/{}".format(run.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == [
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


def test_get_by_id_should_find(client, suite_result):
    url = f"/api/v1/suite_results/{suite_result.id}"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == {
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
    assert rv.get_json() == {
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
            }
        ],
    }


def test_get_by_id_should_404(client):
    url = "/api/v1/suite_results/42"

    rv = client.get(url)

    assert rv.status_code == 404
