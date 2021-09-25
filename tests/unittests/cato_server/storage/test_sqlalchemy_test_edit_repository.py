import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.test_status import TestStatus
from cato_server.domain.test_edit import (
    AbstractTestEdit,
    EditTypes,
    ComparisonSettingsEdit,
    ComparisonSettingsEditValue,
    ReferenceImageEdit,
    ReferenceImageEditValue,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_edit_repository import (
    SqlAlchemyTestEditRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)


def test_save_comparison_settings_edit(
    test_result, sessionmaker_fixture, stored_image_factory
):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)
    test_edit = ComparisonSettingsEdit(
        id=0,
        test_id=test_result.id,
        created_at=datetime.datetime.now(),
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1.0
            ),
            status=TestStatus.SUCCESS,
            message=None,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
            status=TestStatus.FAILED,
            message="Failed",
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )

    saved_test_edit = repository.save(test_edit)
    test_edit.id = saved_test_edit.id

    assert test_edit == saved_test_edit


def test_save_reference_image_edit(
    test_result, sessionmaker_fixture, stored_image_factory
):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)
    test_edit = ReferenceImageEdit(
        id=0,
        test_id=test_result.id,
        created_at=datetime.datetime.now(),
        new_value=ReferenceImageEditValue(
            status=TestStatus.SUCCESS,
            message=None,
            reference_image_id=stored_image_factory().id,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ReferenceImageEditValue(
            status=TestStatus.FAILED,
            message="Failed",
            reference_image_id=stored_image_factory().id,
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )

    saved_test_edit = repository.save(test_edit)
    test_edit.id = saved_test_edit.id

    assert test_edit == saved_test_edit


def test_save_not_existing_test_result(sessionmaker_fixture, stored_image_factory):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)
    test_edit = ComparisonSettingsEdit(
        id=0,
        test_id=10,
        created_at=datetime.datetime.now(),
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1.0
            ),
            status=TestStatus.SUCCESS,
            message=None,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
            status=TestStatus.FAILED,
            message="Failed",
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )

    with pytest.raises(IntegrityError):
        repository.save(test_edit)


def test_find_by_test_id_should_find_empty_list(sessionmaker_fixture):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)

    result = repository.find_by_test_id(1)

    assert result == []


def test_find_by_test_id(sessionmaker_fixture, test_result, stored_image_factory):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)
    now = datetime.datetime.now()
    test_edits = [
        ComparisonSettingsEdit(
            id=0,
            test_id=test_result.id,
            created_at=now + datetime.timedelta(seconds=-1),
            new_value=ComparisonSettingsEditValue(
                comparison_settings=ComparisonSettings(
                    method=ComparisonMethod.SSIM, threshold=1.0
                ),
                status=TestStatus.SUCCESS,
                message=None,
                diff_image_id=stored_image_factory().id,
                error_value=1,
            ),
            old_value=ComparisonSettingsEditValue(
                comparison_settings=ComparisonSettings(
                    method=ComparisonMethod.SSIM, threshold=0.5
                ),
                status=TestStatus.FAILED,
                message="Failed",
                diff_image_id=stored_image_factory().id,
                error_value=0.5,
            ),
        )
        for _ in range(10)
    ]
    repository.insert_many(test_edits)
    test_result_id = test_result.id
    test_result.id = 0
    test_result = SqlAlchemyTestResultRepository(sessionmaker_fixture).save(test_result)
    repository.save(
        ComparisonSettingsEdit(
            id=0,
            test_id=test_result.id,
            created_at=now,
            new_value=ComparisonSettingsEditValue(
                comparison_settings=ComparisonSettings(
                    method=ComparisonMethod.SSIM, threshold=1.0
                ),
                status=TestStatus.SUCCESS,
                message=None,
                diff_image_id=stored_image_factory().id,
                error_value=1,
            ),
            old_value=ComparisonSettingsEditValue(
                comparison_settings=ComparisonSettings(
                    method=ComparisonMethod.SSIM, threshold=0.5
                ),
                status=TestStatus.FAILED,
                message="Failed",
                diff_image_id=stored_image_factory().id,
                error_value=0.5,
            ),
        )
    )

    results = repository.find_by_test_id(test_result_id)

    assert len(results) == 10
    for i, test_edit in enumerate(test_edits):
        test_edit.id = i + 1
        assert test_edit == results[i]


def test_find_by_test_id_should_return_all_test_edit_instances(
    sessionmaker_fixture, test_result, stored_image_factory
):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)
    now = datetime.datetime.now()
    comparison_settings_edit = ComparisonSettingsEdit(
        id=0,
        test_id=test_result.id,
        created_at=now,
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1.0
            ),
            status=TestStatus.SUCCESS,
            message=None,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
            status=TestStatus.FAILED,
            message="Failed",
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )
    reference_image_edit = ReferenceImageEdit(
        id=0,
        test_id=test_result.id,
        created_at=datetime.datetime.now(),
        new_value=ReferenceImageEditValue(
            status=TestStatus.SUCCESS,
            message=None,
            reference_image_id=stored_image_factory().id,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ReferenceImageEditValue(
            status=TestStatus.FAILED,
            message="Failed",
            reference_image_id=stored_image_factory().id,
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )
    comparison_settings_edit = repository.save(comparison_settings_edit)
    reference_image_edit = repository.save(reference_image_edit)

    results = repository.find_by_test_id(test_result.id)

    assert results == [reference_image_edit, comparison_settings_edit]


def test_find_by_test_id_with_edit_type(
    test_result, sessionmaker_fixture, stored_image_factory
):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)
    test_edit = ComparisonSettingsEdit(
        id=0,
        test_id=test_result.id,
        created_at=datetime.datetime.now(),
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1
            ),
            status=TestStatus.SUCCESS,
            message=None,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
            status=TestStatus.FAILED,
            message="Failed",
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )
    saved_test_edit = repository.save(test_edit)
    other_test_edit = ReferenceImageEdit(
        id=0,
        test_id=test_result.id,
        created_at=datetime.datetime.now(),
        new_value=ReferenceImageEditValue(
            status=TestStatus.SUCCESS,
            message=None,
            reference_image_id=stored_image_factory().id,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ReferenceImageEditValue(
            status=TestStatus.FAILED,
            message="Failed",
            reference_image_id=stored_image_factory().id,
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )
    repository.save(other_test_edit)

    results = repository.find_by_test_id(
        test_result.id, edit_type=EditTypes.COMPARISON_SETTINGS
    )

    assert results == [saved_test_edit]


def test_find_by_run_id_should_find_empty_list(sessionmaker_fixture, run):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)

    result = repository.find_by_run_id(run.id)

    assert result == []


def test_find_by_run_id_should_find(
    sessionmaker_fixture, run, test_result, stored_image_factory
):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)
    test_edit = ComparisonSettingsEdit(
        id=0,
        test_id=test_result.id,
        created_at=datetime.datetime.now(),
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1
            ),
            status=TestStatus.SUCCESS,
            message=None,
            diff_image_id=stored_image_factory().id,
            error_value=1,
        ),
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
            status=TestStatus.FAILED,
            message="Failed",
            diff_image_id=stored_image_factory().id,
            error_value=0.5,
        ),
    )
    saved_test_edit = repository.save(test_edit)

    result = repository.find_by_run_id(run.id)

    assert result == [saved_test_edit]
