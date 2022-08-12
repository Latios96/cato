from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.utils.datetime_utils import aware_now_in_utc


def test_get_test_edits_by_test_result_id(client_with_session, test_edit, test_result):
    url = f"/api/v1/test_edits/{test_result.id}"

    rv = client_with_session.get(url)

    assert rv.status_code == 200

    json = rv.json()
    now = aware_now_in_utc()
    json[0]["createdAt"] = now
    assert json == [
        {
            "createdAt": now,
            "editType": "COMPARISON_SETTINGS",
            "id": 1,
            "newValue": {
                "comparisonSettings": {"method": "SSIM", "threshold": 10.0},
                "diffImageId": 2,
                "message": "still success",
                "status": "SUCCESS",
                "errorValue": 0.1,
            },
            "oldValue": {
                "comparisonSettings": {"method": "SSIM", "threshold": 1.0},
                "diffImageId": 1,
                "message": "success",
                "status": "SUCCESS",
                "errorValue": 1.0,
            },
            "testId": 1,
            "testIdentifier": "my_suite/my_test_name",
        }
    ]


def test_get_test_edits_by_test_result_id_should_return_empty(client_with_session):
    url = f"/api/v1/test_edits/2"

    rv = client_with_session.get(url)

    assert rv.status_code == 200

    assert rv.json() == []


def test_get_test_edits_by_run_id(client_with_session, test_edit, test_result, run):
    url = f"/api/v1/test_edits/{run.id}"

    rv = client_with_session.get(url)

    assert rv.status_code == 200

    json = rv.json()
    now = aware_now_in_utc()
    json[0]["createdAt"] = now
    assert json == [
        {
            "createdAt": now,
            "editType": "COMPARISON_SETTINGS",
            "id": 1,
            "newValue": {
                "comparisonSettings": {"method": "SSIM", "threshold": 10.0},
                "diffImageId": 2,
                "message": "still success",
                "status": "SUCCESS",
                "errorValue": 0.1,
            },
            "oldValue": {
                "comparisonSettings": {"method": "SSIM", "threshold": 1.0},
                "diffImageId": 1,
                "message": "success",
                "status": "SUCCESS",
                "errorValue": 1,
            },
            "testId": 1,
            "testIdentifier": "my_suite/my_test_name",
        }
    ]


def test_get_test_edits_by_run_id_should_return_empty(client_with_session, run):
    url = f"/api/v1/test_edits/2"

    rv = client_with_session.get(url)

    assert rv.status_code == 200

    assert rv.json() == []


def test_create_comparison_settings_edit_success(
    client_with_session,
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
        unified_test_status=UnifiedTestStatus.SUCCESS,
    )
    url = f"/api/v1/test_edits/comparison_settings"

    rv = client_with_session.post(
        url,
        json={
            "testResultId": test_result.id,
            "newValue": {"method": "SSIM", "threshold": 1},
        },
    )

    assert rv.status_code == 201
    json = rv.json()
    now = aware_now_in_utc()
    json["createdAt"] = now
    assert json == {
        "createdAt": now,
        "editType": "COMPARISON_SETTINGS",
        "id": 1,
        "newValue": {
            "comparisonSettings": {"method": "SSIM", "threshold": 1},
            "diffImageId": 3,
            "message": None,
            "status": "SUCCESS",
            "errorValue": 1,
        },
        "oldValue": {
            "comparisonSettings": {"method": "SSIM", "threshold": 1.0},
            "diffImageId": None,
            "message": "success",
            "status": "SUCCESS",
            "errorValue": None,
        },
        "testId": 1,
        "testIdentifier": "my_suite/my_test_name",
    }


def test_create_comparison_settings_edit_failure(
    client_with_session,
):
    url = f"/api/v1/test_edits/comparison_settings"

    rv = client_with_session.post(
        url,
        json={
            "testResultId": 1,
            "newValue": {"method": "SSIM", "threshold": 1},
        },
    )

    assert rv.status_code == 400
    assert rv.json() == {"id": ["No TestResult with id 1 exists!"]}


def test_can_create_comparison_settings_edit_should_return_true(
    client_with_session,
    sessionmaker_fixture,
    suite_result,
    saving_test_result_factory,
    stored_image,
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

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {"canEdit": True, "message": None}


def test_can_create_comparison_settings_edit_should_return_false(
    client_with_session, sessionmaker_fixture, suite_result, saving_test_result_factory
):
    test_result = saving_test_result_factory(
        suite_result_id=suite_result.id, diff_image=None
    )
    url = f"/api/v1/test_edits/can-edit/{test_result.id}/comparison_settings"

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "canEdit": False,
        "message": "Can't edit a test result which has no comparison settings!",
    }


def test_can_create_reference_image_edit_should_return_true(
    client_with_session,
    sessionmaker_fixture,
    suite_result,
    saving_test_result_factory,
    stored_image,
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

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {"canEdit": True, "message": None}


def test_can_create_reference_image_edit_should_return_false(
    client_with_session, sessionmaker_fixture, suite_result, saving_test_result_factory
):
    test_result = saving_test_result_factory(
        suite_result_id=suite_result.id, image_output=None
    )
    url = f"/api/v1/test_edits/can-edit/{test_result.id}/reference_image"

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "canEdit": False,
        "message": "Can't edit a test result which has no image_output!",
    }


def test_create_reference_image_edit_success(
    client_with_session,
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
        unified_test_status=UnifiedTestStatus.SUCCESS,
    )
    url = f"/api/v1/test_edits/reference_image"

    rv = client_with_session.post(
        url,
        json={"testResultId": test_result.id},
    )

    assert rv.status_code == 201
    json = rv.json()
    now = aware_now_in_utc()
    json["createdAt"] = now
    assert json == {
        "createdAt": now,
        "editType": "REFERENCE_IMAGE",
        "id": 1,
        "newValue": {
            "diffImageId": 3,
            "errorValue": 1.0,
            "message": None,
            "referenceImageId": 1,
            "status": "SUCCESS",
        },
        "oldValue": {
            "diffImageId": None,
            "errorValue": None,
            "message": "success",
            "referenceImageId": 2,
            "status": "SUCCESS",
        },
        "testId": 1,
        "testIdentifier": "my_suite/my_test_name",
    }


def test_create_reference_image_edit_failure(
    client_with_session,
):
    url = f"/api/v1/test_edits/reference_image"

    rv = client_with_session.post(
        url,
        json={
            "testResultId": 1,
        },
    )

    assert rv.status_code == 400
    assert rv.json() == {"id": ["No TestResult with id 1 exists!"]}


def test_test_edits_by_run_id_should_return_test_edit(
    client_with_session, run, test_result, saving_reference_image_edit_factory
):
    now = aware_now_in_utc()
    saving_reference_image_edit_factory(test_id=test_result.id, created_at=now)
    url = f"/api/v1/test_edits/runs/{run.id}/edits-to-sync"

    rv = client_with_session.get(url)

    assert rv.status_code == 200

    json = rv.json()
    assert json == [
        {
            "createdAt": now.isoformat(),
            "editType": "REFERENCE_IMAGE",
            "id": 1,
            "newValue": {
                "diffImageId": 3,
                "errorValue": 1.0,
                "message": None,
                "referenceImageId": 2,
                "status": "SUCCESS",
            },
            "oldValue": {
                "diffImageId": 5,
                "errorValue": 0.5,
                "message": "Failed",
                "referenceImageId": 4,
                "status": "FAILED",
            },
            "testId": 1,
            "testIdentifier": "some/test",
        }
    ]


def test_test_edits_by_run_id_should_return_empty_list(client_with_session, run):
    url = f"/api/v1/test_edits/runs/{run.id}/edits-to-sync"

    rv = client_with_session.get(url)

    assert rv.status_code == 200

    json = rv.json()
    assert json == []


def test_has_edits_by_run_id_should_return_test_edit(
    client_with_session, run, test_result, saving_reference_image_edit_factory
):
    now = aware_now_in_utc()
    saving_reference_image_edit_factory(test_id=test_result.id, created_at=now)
    url = f"/api/v1/test_edits/runs/{run.id}/edits-to-sync-count"

    rv = client_with_session.get(url)

    assert rv.status_code == 200

    assert rv.json() == {"count": 1}


def test_has_edits_by_run_id_should_return_empty_list(client_with_session, run):
    url = f"/api/v1/test_edits/runs/{run.id}/edits-to-sync-count"

    rv = client_with_session.get(url)

    assert rv.status_code == 200

    assert rv.json() == {"count": 0}
