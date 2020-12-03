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
