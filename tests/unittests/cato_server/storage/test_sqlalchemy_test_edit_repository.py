import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_edit import (
    EditTypes,
    ComparisonSettingsEdit,
    ComparisonSettingsEditValue,
    ReferenceImageEdit,
    ReferenceImageEditValue,
)
from cato_common.utils.datetime_utils import aware_now_in_utc


def test_save_comparison_settings_edit(
    test_result, sqlalchemy_test_edit_repository, stored_image_factory
):
    test_edit = ComparisonSettingsEdit(
        id=0,
        test_id=test_result.id,
        test_identifier=test_result.test_identifier,
        created_at=aware_now_in_utc(),
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1.0
            ),
            status=ResultStatus.SUCCESS,
            message=None,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
            status=ResultStatus.FAILED,
            message="Failed",
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )

    saved_test_edit = sqlalchemy_test_edit_repository.save(test_edit)
    test_edit.id = saved_test_edit.id

    assert test_edit == saved_test_edit


def test_save_reference_image_edit(
    test_result, sqlalchemy_test_edit_repository, stored_image_factory
):
    test_edit = ReferenceImageEdit(
        id=0,
        test_id=test_result.id,
        test_identifier=test_result.test_identifier,
        created_at=aware_now_in_utc(),
        new_value=ReferenceImageEditValue(
            status=ResultStatus.SUCCESS,
            message=None,
            reference_image_id=stored_image_factory().id,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ReferenceImageEditValue(
            status=ResultStatus.FAILED,
            message="Failed",
            reference_image_id=stored_image_factory().id,
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )

    saved_test_edit = sqlalchemy_test_edit_repository.save(test_edit)
    test_edit.id = saved_test_edit.id

    assert test_edit == saved_test_edit


def test_save_not_existing_test_result(
    sqlalchemy_test_edit_repository, stored_image_factory
):
    test_edit = ComparisonSettingsEdit(
        id=0,
        test_id=10,
        test_identifier=TestIdentifier.from_string("some/test"),
        created_at=aware_now_in_utc(),
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1.0
            ),
            status=ResultStatus.SUCCESS,
            message=None,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
            status=ResultStatus.FAILED,
            message="Failed",
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )

    with pytest.raises(IntegrityError):
        sqlalchemy_test_edit_repository.save(test_edit)


def test_find_by_test_id_should_find_empty_list(sqlalchemy_test_edit_repository):
    result = sqlalchemy_test_edit_repository.find_by_test_id(1)

    assert result == []


def test_find_by_test_id(
    sqlalchemy_test_edit_repository,
    sqlalchemy_test_result_repository,
    test_result,
    stored_image_factory,
):
    now = aware_now_in_utc()
    test_edits = [
        ComparisonSettingsEdit(
            id=0,
            test_id=test_result.id,
            test_identifier=test_result.test_identifier,
            created_at=now + datetime.timedelta(seconds=-1),
            new_value=ComparisonSettingsEditValue(
                comparison_settings=ComparisonSettings(
                    method=ComparisonMethod.SSIM, threshold=1.0
                ),
                status=ResultStatus.SUCCESS,
                message=None,
                diff_image_id=stored_image_factory().id,
                error_value=1,
            ),
            old_value=ComparisonSettingsEditValue(
                comparison_settings=ComparisonSettings(
                    method=ComparisonMethod.SSIM, threshold=0.5
                ),
                status=ResultStatus.FAILED,
                message="Failed",
                diff_image_id=stored_image_factory().id,
                error_value=0.5,
            ),
        )
        for _ in range(10)
    ]
    sqlalchemy_test_edit_repository.insert_many(test_edits)
    test_result_id = test_result.id
    test_result.id = 0
    test_result = sqlalchemy_test_result_repository.save(test_result)
    sqlalchemy_test_edit_repository.save(
        ComparisonSettingsEdit(
            id=0,
            test_id=test_result.id,
            test_identifier=test_result.test_identifier,
            created_at=now,
            new_value=ComparisonSettingsEditValue(
                comparison_settings=ComparisonSettings(
                    method=ComparisonMethod.SSIM, threshold=1.0
                ),
                status=ResultStatus.SUCCESS,
                message=None,
                diff_image_id=stored_image_factory().id,
                error_value=1,
            ),
            old_value=ComparisonSettingsEditValue(
                comparison_settings=ComparisonSettings(
                    method=ComparisonMethod.SSIM, threshold=0.5
                ),
                status=ResultStatus.FAILED,
                message="Failed",
                diff_image_id=stored_image_factory().id,
                error_value=0.5,
            ),
        )
    )

    results = sqlalchemy_test_edit_repository.find_by_test_id(test_result_id)

    assert len(results) == 10
    for i, test_edit in enumerate(test_edits):
        test_edit.id = i + 1
        assert test_edit.test_id == test_result_id


def test_find_by_test_id_should_return_all_test_edit_instances(
    sqlalchemy_test_edit_repository, test_result, stored_image_factory
):
    now = aware_now_in_utc()
    comparison_settings_edit = ComparisonSettingsEdit(
        id=0,
        test_id=test_result.id,
        test_identifier=test_result.test_identifier,
        created_at=now,
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1.0
            ),
            status=ResultStatus.SUCCESS,
            message=None,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
            status=ResultStatus.FAILED,
            message="Failed",
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )
    reference_image_edit = ReferenceImageEdit(
        id=0,
        test_id=test_result.id,
        test_identifier=test_result.test_identifier,
        created_at=aware_now_in_utc(),
        new_value=ReferenceImageEditValue(
            status=ResultStatus.SUCCESS,
            message=None,
            reference_image_id=stored_image_factory().id,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ReferenceImageEditValue(
            status=ResultStatus.FAILED,
            message="Failed",
            reference_image_id=stored_image_factory().id,
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )
    comparison_settings_edit = sqlalchemy_test_edit_repository.save(
        comparison_settings_edit
    )
    reference_image_edit = sqlalchemy_test_edit_repository.save(reference_image_edit)

    results = sqlalchemy_test_edit_repository.find_by_test_id(test_result.id)

    assert results == [reference_image_edit, comparison_settings_edit]


def test_find_by_test_id_with_edit_type(
    test_result, sqlalchemy_test_edit_repository, stored_image_factory
):
    test_edit = ComparisonSettingsEdit(
        id=0,
        test_id=test_result.id,
        test_identifier=test_result.test_identifier,
        created_at=aware_now_in_utc(),
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1
            ),
            status=ResultStatus.SUCCESS,
            message=None,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
            status=ResultStatus.FAILED,
            message="Failed",
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )
    saved_test_edit = sqlalchemy_test_edit_repository.save(test_edit)
    other_test_edit = ReferenceImageEdit(
        id=0,
        test_id=test_result.id,
        test_identifier=test_result.test_identifier,
        created_at=aware_now_in_utc(),
        new_value=ReferenceImageEditValue(
            status=ResultStatus.SUCCESS,
            message=None,
            reference_image_id=stored_image_factory().id,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ReferenceImageEditValue(
            status=ResultStatus.FAILED,
            message="Failed",
            reference_image_id=stored_image_factory().id,
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )
    sqlalchemy_test_edit_repository.save(other_test_edit)

    results = sqlalchemy_test_edit_repository.find_by_test_id(
        test_result.id, edit_type=EditTypes.COMPARISON_SETTINGS
    )

    assert results == [saved_test_edit]


def test_find_by_run_id_should_find_empty_list(sqlalchemy_test_edit_repository, run):
    result = sqlalchemy_test_edit_repository.find_by_run_id(run.id)

    assert result == []


def test_find_by_run_id_should_find(
    sqlalchemy_test_edit_repository, run, test_result, stored_image_factory
):
    test_edit = ComparisonSettingsEdit(
        id=0,
        test_id=test_result.id,
        test_identifier=test_result.test_identifier,
        created_at=aware_now_in_utc(),
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1
            ),
            status=ResultStatus.SUCCESS,
            message=None,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
            status=ResultStatus.FAILED,
            message="Failed",
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )
    saved_test_edit = sqlalchemy_test_edit_repository.save(test_edit)

    result = sqlalchemy_test_edit_repository.find_by_run_id(run.id)

    assert result == [saved_test_edit]


def test_find_edits_to_sync_by_run_id_should_find_all_latest_edits_per_test_for_run(
    sqlalchemy_test_edit_repository,
    saving_test_result_factory,
    run,
    saving_comparison_settings_edit_factory,
    saving_run_factory,
    saving_suite_result_factory,
    saving_reference_image_edit_factory,
):
    (
        comparison_settings_edit_two_for_test_result_one,
        comparison_settings_edit_two_for_test_result_two_run_one,
        reference_image_edit_two_for_run_one,
        run_one,
    ) = setup_test_edits_for_multiple_runs_and_tests(
        saving_comparison_settings_edit_factory,
        saving_reference_image_edit_factory,
        saving_run_factory,
        saving_suite_result_factory,
        saving_test_result_factory,
    )

    edits = sqlalchemy_test_edit_repository.find_edits_to_sync_by_run_id(run_one.id)

    assert to_id_set(edits) == {
        comparison_settings_edit_two_for_test_result_one.id,
        reference_image_edit_two_for_run_one.id,
        comparison_settings_edit_two_for_test_result_two_run_one.id,
    }


def test_find_edits_to_sync_no_edits_exist_should_find_empty_list(
    run, sqlalchemy_test_edit_repository
):
    edits = sqlalchemy_test_edit_repository.find_edits_to_sync_by_run_id(run.id)

    assert edits == []


def test_has_edits_to_sync_by_run_id_should_find_all_latest_edits_per_test_for_run(
    sqlalchemy_test_edit_repository,
    saving_test_result_factory,
    run,
    saving_comparison_settings_edit_factory,
    saving_run_factory,
    saving_suite_result_factory,
    saving_reference_image_edit_factory,
):
    (
        comparison_settings_edit_two_for_test_result_one,
        comparison_settings_edit_two_for_test_result_two_run_one,
        reference_image_edit_two_for_run_one,
        run_one,
    ) = setup_test_edits_for_multiple_runs_and_tests(
        saving_comparison_settings_edit_factory,
        saving_reference_image_edit_factory,
        saving_run_factory,
        saving_suite_result_factory,
        saving_test_result_factory,
    )

    assert (
        sqlalchemy_test_edit_repository.edits_to_sync_by_run_id_count(run_one.id) == 3
    )


def test_has_edits_to_sync_no_edits_exist_should_find_empty_list(
    run, sqlalchemy_test_edit_repository
):
    assert sqlalchemy_test_edit_repository.edits_to_sync_by_run_id_count(run.id) == 0


# todo extract this
def to_id_list(entites):
    return list(map(lambda x: x.id, entites))


def to_id_set(entites):
    return set(map(lambda x: x.id, entites))


def setup_test_edits_for_multiple_runs_and_tests(
    saving_comparison_settings_edit_factory,
    saving_reference_image_edit_factory,
    saving_run_factory,
    saving_suite_result_factory,
    saving_test_result_factory,
):
    run_one = saving_run_factory()
    run_two = saving_run_factory()
    suite_result_one = saving_suite_result_factory(run_id=run_one.id)
    suite_result_two = saving_suite_result_factory(run_id=run_two.id)
    test_result_one_run_one = saving_test_result_factory(
        suite_result_id=suite_result_one.id,
        test_identifier=TestIdentifier.from_string(f"{suite_result_one.id}/1"),
    )
    test_result_two_run_one = saving_test_result_factory(
        suite_result_id=suite_result_one.id,
        test_identifier=TestIdentifier.from_string(f"{suite_result_one.id}/2"),
    )
    test_result_run_two = saving_test_result_factory(
        suite_result_id=suite_result_two.id,
        test_identifier=TestIdentifier.from_string(f"{suite_result_two.id}/1"),
    )
    comparison_settings_edit_one_for_test_result_one = (
        saving_comparison_settings_edit_factory(
            test_id=test_result_one_run_one.id,
            created_at=aware_now_in_utc() - datetime.timedelta(seconds=30),
        )
    )
    comparison_settings_edit_two_for_test_result_one = (
        saving_comparison_settings_edit_factory(
            test_id=test_result_one_run_one.id,
            created_at=aware_now_in_utc() - datetime.timedelta(seconds=20),
        )
    )
    comparison_settings_edit_two_for_test_result_two_run_one = (
        saving_comparison_settings_edit_factory(
            test_id=test_result_two_run_one.id,
            created_at=aware_now_in_utc() - datetime.timedelta(seconds=20),
        )
    )
    reference_image_edit_one_for_run_one = saving_reference_image_edit_factory(
        test_id=test_result_one_run_one.id,
        created_at=aware_now_in_utc() - datetime.timedelta(seconds=30),
    )
    reference_image_edit_two_for_run_one = saving_reference_image_edit_factory(
        test_id=test_result_one_run_one.id,
        created_at=aware_now_in_utc() - datetime.timedelta(seconds=20),
    )
    comparison_settings_edit_for_run_two = saving_reference_image_edit_factory(
        test_id=test_result_run_two.id,
        created_at=aware_now_in_utc() - datetime.timedelta(seconds=10),
    )
    return (
        comparison_settings_edit_two_for_test_result_one,
        comparison_settings_edit_two_for_test_result_two_run_one,
        reference_image_edit_two_for_run_one,
        run_one,
    )
