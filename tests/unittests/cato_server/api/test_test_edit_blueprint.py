import datetime

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)


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
    sessionmaker_fixture,
    suite_result,
    test_result_factory,
    stored_image_factory,
):
    test_result = test_result_factory(
        comparison_settings=ComparisonSettings(
            method=ComparisonMethod.SSIM, threshold=1
        ),
        suite_result_id=suite_result.id,
        image_output=stored_image_factory().id,
        reference_image=stored_image_factory().id,
    )
    test_result = SqlAlchemyTestResultRepository(sessionmaker_fixture).save(test_result)
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
    client, sessionmaker_fixture, suite_result, test_result_factory, stored_image
):
    test_result = SqlAlchemyTestResultRepository(sessionmaker_fixture).save(
        test_result_factory(
            suite_result_id=suite_result.id,
            reference_image=stored_image.id,
            image_output=stored_image.id,
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
        )
    )
    url = f"/api/v1/test_edits/can-edit/{test_result.id}/comparison_settings"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {"can_edit": True, "message": None}


def test_can_create_comparison_settings_edit_should_return_false(
    client, sessionmaker_fixture, suite_result, test_result_factory
):
    test_result = SqlAlchemyTestResultRepository(sessionmaker_fixture).save(
        test_result_factory(suite_result_id=suite_result.id, diff_image=None)
    )
    url = f"/api/v1/test_edits/can-edit/{test_result.id}/comparison_settings"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "can_edit": False,
        "message": "Can't edit a test result which has no comparison settings!",
    }
