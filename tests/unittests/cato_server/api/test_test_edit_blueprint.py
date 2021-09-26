import datetime

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings


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
            "new_value": {
                "comparison_settings": {"method": "SSIM", "threshold": 10.0},
                "diff_image_id": 2,
                "message": "still success",
                "status": "SUCCESS",
                "error_value": 0.1,
            },
            "old_value": {
                "comparison_settings": {"method": "SSIM", "threshold": 1.0},
                "diff_image_id": 1,
                "message": "success",
                "status": "SUCCESS",
                "error_value": 1,
            },
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
            "new_value": {
                "comparison_settings": {"method": "SSIM", "threshold": 10.0},
                "diff_image_id": 2,
                "message": "still success",
                "status": "SUCCESS",
                "error_value": 0.1,
            },
            "old_value": {
                "comparison_settings": {"method": "SSIM", "threshold": 1.0},
                "diff_image_id": 1,
                "message": "success",
                "status": "SUCCESS",
                "error_value": 1,
            },
            "test_id": 1,
        }
    ]


def test_get_test_edits_by_run_id_should_return_empty(client, run):
    url = f"/api/v1/test_edits/2"

    rv = client.get(url)

    assert rv.status_code == 200

    assert rv.json() == []


def test_create_comparison_settings_edit_success(
    client,
    suite_result,
    saving_test_result_factory,
    stored_image_factory,
):
    test_result = saving_test_result_factory(
        comparison_settings=ComparisonSettings(
            method=ComparisonMethod.SSIM, threshold=1
        ),
        suite_result_id=suite_result.id,
        image_output=stored_image_factory().id,
        reference_image=stored_image_factory().id,
    )
    url = f"/api/v1/test_edits/comparison_settings"

    rv = client.post(
        url,
        json={
            "test_result_id": test_result.id,
            "new_value": {"method": "SSIM", "threshold": 1},
        },
    )

    assert rv.status_code == 201
    json = rv.json()
    now = datetime.datetime.now()
    json["created_at"] = now
    assert json == {
        "created_at": now,
        "edit_type": "COMPARISON_SETTINGS",
        "id": 1,
        "new_value": {
            "comparison_settings": {"method": "SSIM", "threshold": 1},
            "diff_image_id": 3,
            "message": None,
            "status": "SUCCESS",
            "error_value": 1,
        },
        "old_value": {
            "comparison_settings": {"method": "SSIM", "threshold": 1.0},
            "diff_image_id": None,
            "message": "success",
            "status": "SUCCESS",
            "error_value": None,
        },
        "test_id": 1,
    }


def test_create_comparison_settings_edit_failure(
    client,
):
    url = f"/api/v1/test_edits/comparison_settings"

    rv = client.post(
        url,
        json={
            "test_result_id": 1,
            "new_value": {"method": "SSIM", "threshold": 1},
        },
    )

    assert rv.status_code == 400
    assert rv.json() == {"id": ["No TestResult with id 1 exists!"]}


def test_can_create_comparison_settings_edit_should_return_true(
    client, sessionmaker_fixture, suite_result, saving_test_result_factory, stored_image
):
    test_result = saving_test_result_factory(
        suite_result_id=suite_result.id,
        reference_image=stored_image.id,
        image_output=stored_image.id,
        comparison_settings=ComparisonSettings(
            method=ComparisonMethod.SSIM, threshold=0.5
        ),
    )
    url = f"/api/v1/test_edits/can-edit/{test_result.id}/comparison_settings"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {"can_edit": True, "message": None}


def test_can_create_comparison_settings_edit_should_return_false(
    client, sessionmaker_fixture, suite_result, saving_test_result_factory
):
    test_result = saving_test_result_factory(
        suite_result_id=suite_result.id, diff_image=None
    )
    url = f"/api/v1/test_edits/can-edit/{test_result.id}/comparison_settings"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "can_edit": False,
        "message": "Can't edit a test result which has no comparison settings!",
    }


def test_can_create_reference_image_edit_should_return_true(
    client, sessionmaker_fixture, suite_result, saving_test_result_factory, stored_image
):
    test_result = saving_test_result_factory(
        suite_result_id=suite_result.id,
        reference_image=stored_image.id,
        image_output=stored_image.id,
        comparison_settings=ComparisonSettings(
            method=ComparisonMethod.SSIM, threshold=0.5
        ),
    )
    url = f"/api/v1/test_edits/can-edit/{test_result.id}/reference_image"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {"can_edit": True, "message": None}


def test_can_create_reference_image_edit_should_return_false(
    client, sessionmaker_fixture, suite_result, saving_test_result_factory
):
    test_result = saving_test_result_factory(
        suite_result_id=suite_result.id, image_output=None
    )
    url = f"/api/v1/test_edits/can-edit/{test_result.id}/reference_image"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "can_edit": False,
        "message": "Can't edit a test result which has no image_output!",
    }


def test_create_reference_image_edit_success(
    client,
    suite_result,
    saving_test_result_factory,
    stored_image_factory,
):
    test_result = saving_test_result_factory(
        comparison_settings=ComparisonSettings(
            method=ComparisonMethod.SSIM, threshold=1
        ),
        suite_result_id=suite_result.id,
        image_output=stored_image_factory().id,
        reference_image=stored_image_factory().id,
    )
    url = f"/api/v1/test_edits/reference_image"

    rv = client.post(
        url,
        json={"test_result_id": test_result.id},
    )

    assert rv.status_code == 201
    json = rv.json()
    now = datetime.datetime.now()
    json["created_at"] = now
    assert json == {
        "created_at": now,
        "edit_type": "REFERENCE_IMAGE",
        "id": 1,
        "new_value": {
            "diff_image_id": 3,
            "error_value": 1.0,
            "message": None,
            "reference_image_id": 1,
            "status": "SUCCESS",
        },
        "old_value": {
            "diff_image_id": None,
            "error_value": None,
            "message": "success",
            "reference_image_id": 2,
            "status": "SUCCESS",
        },
        "test_id": 1,
    }


def test_create_reference_image_edit_failure(
    client,
):
    url = f"/api/v1/test_edits/reference_image"

    rv = client.post(
        url,
        json={
            "test_result_id": 1,
        },
    )

    assert rv.status_code == 400
    assert rv.json() == {"id": ["No TestResult with id 1 exists!"]}


def test_test_edits_by_run_id_should_return_test_edit(
    client, run, test_result, saving_reference_image_edit_factory
):
    now = datetime.datetime.now()
    saving_reference_image_edit_factory(test_id=test_result.id, created_at=now)
    url = f"/api/v1/test_edits/runs/{run.id}/edits-to-sync"

    rv = client.get(url)

    assert rv.status_code == 200

    json = rv.json()
    assert json == [
        {
            "created_at": now.isoformat(),
            "edit_type": "REFERENCE_IMAGE",
            "id": 1,
            "new_value": {
                "diff_image_id": 3,
                "error_value": 1.0,
                "message": None,
                "reference_image_id": 2,
                "status": "SUCCESS",
            },
            "old_value": {
                "diff_image_id": 5,
                "error_value": 0.5,
                "message": "Failed",
                "reference_image_id": 4,
                "status": "FAILED",
            },
            "test_id": 1,
        }
    ]


def test_test_edits_by_run_id_should_return_empty_list(client, run):
    url = f"/api/v1/test_edits/runs/{run.id}/edits-to-sync"

    rv = client.get(url)

    assert rv.status_code == 200

    json = rv.json()
    assert json == []


def test_has_edits_by_run_id_should_return_test_edit(
    client, run, test_result, saving_reference_image_edit_factory
):
    now = datetime.datetime.now()
    saving_reference_image_edit_factory(test_id=test_result.id, created_at=now)
    url = f"/api/v1/test_edits/runs/{run.id}/edits-to-sync-count"

    rv = client.get(url)

    assert rv.status_code == 200

    assert rv.json() == {"count": 1}


def test_has_edits_by_run_id_should_return_empty_list(client, run):
    url = f"/api/v1/test_edits/runs/{run.id}/edits-to-sync-count"

    rv = client.get(url)

    assert rv.status_code == 200

    assert rv.json() == {"count": 0}
