def test_get_run_by_project_id_should_return(client, project, run):
    url = "/api/v1/runs/project/{}".format(project.id)

    rv = client.get(url)

    assert rv.status_code == 200
    json = rv.get_json()
    assert len(json) == 1
    assert json[0]["id"] == 1
    assert json[0]["project_id"] == 1


def test_get_run_by_project_id_should_return_empty_list(client, project):
    url = "/api/v1/runs/project/{}".format(project.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == []
