import datetime


def test_get_test_edits_by_test_result_id(client, test_edit, test_result):
    url = f"/api/v1/test_edits/{test_result.id}"

    rv = client.get(url)

    assert rv.status_code == 200

    json = rv.json()
    now = datetime.datetime.now()
    json[0]["created_at"] = now
    assert json == [
        {
            "created_at": now,
            "edit_type": "COMPARISON_SETTINGS",
            "id": 1,
            "new_value": {"method": "SSIM", "threshold": 10},
            "old_value": {"method": "SSIM", "threshold": 1},
            "test_id": 1,
        }
    ]


def test_get_test_edits_by_test_result_id_should_return_empty(client):
    url = f"/api/v1/test_edits/2"

    rv = client.get(url)

    assert rv.status_code == 200

    assert rv.json() == []


def test_get_test_edits_by_run_id(client, test_edit, test_result, run):
    url = f"/api/v1/test_edits/{run.id}"

    rv = client.get(url)

    assert rv.status_code == 200

    json = rv.json()
    now = datetime.datetime.now()
    json[0]["created_at"] = now
    assert json == [
        {
            "created_at": now,
            "edit_type": "COMPARISON_SETTINGS",
            "id": 1,
            "new_value": {"method": "SSIM", "threshold": 10},
            "old_value": {"method": "SSIM", "threshold": 1},
            "test_id": 1,
        }
    ]


def test_get_test_edits_by_run_id_should_return_empty(client, run):
    url = f"/api/v1/test_edits/2"

    rv = client.get(url)

    assert rv.status_code == 200

    assert rv.json() == []
