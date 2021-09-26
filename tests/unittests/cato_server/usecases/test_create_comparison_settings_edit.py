import datetime

import pytest

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.test_status import TestStatus
from cato_common.domain.compare_image_result import CompareImageResult
from cato_common.domain.image import Image
from cato_common.domain.test_edit import (
    ComparisonSettingsEdit,
    ComparisonSettingsEditValue,
)
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.test_edit_repository import TestEditRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.compare_image import CompareImage
from cato_server.usecases.create_comparison_settings_edit import (
    CreateComparisonSettingsEdit,
)
from tests.utils import mock_safe


def test_create_edit_with_success(test_result_factory):
    mock_test_edit_repository = mock_safe(TestEditRepository)
    mock_test_edit_repository.save.side_effect = lambda x: x
    mock_test_result_repository = mock_safe(TestResultRepository)
    test_result = test_result_factory(
        id=5,
        comparison_settings=ComparisonSettings(
            method=ComparisonMethod.SSIM, threshold=0.5
        ),
        diff_image=3,
        reference_image=2,
        image_output=1,
        error_value=1,
    )
    mock_test_result_repository.find_by_id.return_value = test_result
    mock_compare_image = mock_safe(CompareImage)
    mock_compare_image.compare_image_from_db.return_value = CompareImageResult(
        status=TestStatus.SUCCESS,
        message="still success",
        reference_image_id=11,
        output_image_id=12,
        diff_image_id=13,
        error=0.1,
    )
    mock_image_repository = mock_safe(ImageRepository)
    mock_image_repository.find_by_id.side_effect = _create_image
    create_comparison_settings_edit = CreateComparisonSettingsEdit(
        mock_test_edit_repository,
        mock_test_result_repository,
        mock_compare_image,
        mock_image_repository,
    )
    created_at = datetime.datetime(year=2021, month=9, day=17)
    create_comparison_settings_edit._get_created_at = lambda: created_at

    edit_comparison_settings = ComparisonSettings(
        method=ComparisonMethod.SSIM, threshold=1
    )
    edit = create_comparison_settings_edit.create_edit(1, edit_comparison_settings)

    assert edit == ComparisonSettingsEdit(
        id=0,
        test_id=5,
        created_at=created_at,
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
            status=TestStatus.SUCCESS,
            message="success",
            diff_image_id=3,
            error_value=1,
        ),
        new_value=ComparisonSettingsEditValue(
            comparison_settings=edit_comparison_settings,
            status=TestStatus.SUCCESS,
            message="still success",
            diff_image_id=13,
            error_value=0.1,
        ),
    )
    mock_compare_image.compare_image_from_db.assert_called_with(
        _create_image(1), _create_image(2), edit_comparison_settings
    )
    mock_test_result_repository.save.assert_called_with(test_result)
    assert test_result.diff_image == 13
    assert test_result.status == TestStatus.SUCCESS
    assert test_result.message == "still success"
    assert test_result.comparison_settings == edit_comparison_settings


def _create_image(x):
    return Image(
        id=x,
        name="x.png",
        original_file_id=10,
        channels=[],
        width=1920,
        height=1080,
    )


def test_no_test_with_id_found():
    test_edit_repository = mock_safe(TestEditRepository)
    test_result_repository = mock_safe(TestResultRepository)
    test_result_repository.find_by_id.return_value = None
    mock_compare_image = mock_safe(CompareImage)
    mock_image_repository = mock_safe(ImageRepository)
    create_comparison_settings_edit = CreateComparisonSettingsEdit(
        test_edit_repository,
        test_result_repository,
        mock_compare_image,
        mock_image_repository,
    )

    with pytest.raises(ValueError):
        create_comparison_settings_edit.create_edit(
            1, ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
        )


def test_no_reference_image(test_result_factory):
    mock_test_edit_repository = mock_safe(TestEditRepository)
    mock_test_result_repository = mock_safe(TestResultRepository)
    mock_test_result_repository.find_by_id.return_value = test_result_factory(
        reference_image=1,
        image_output=2,
        comparison_settings=ComparisonSettings(
            method=ComparisonMethod.SSIM, threshold=0.5
        ),
    )
    mock_compare_image = mock_safe(CompareImage)
    mock_image_repository = mock_safe(ImageRepository)
    mock_image_repository.find_by_id.side_effect = lambda x: "image" if x == 1 else None
    create_comparison_settings_edit = CreateComparisonSettingsEdit(
        mock_test_edit_repository,
        mock_test_result_repository,
        mock_compare_image,
        mock_image_repository,
    )

    with pytest.raises(ValueError):
        create_comparison_settings_edit.create_edit(
            1, ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
        )
    mock_test_result_repository.save.assert_not_called()


def test_no_output_image(test_result_factory):
    mock_test_edit_repository = mock_safe(TestEditRepository)
    mock_test_result_repository = mock_safe(TestResultRepository)
    mock_test_result_repository.find_by_id.return_value = test_result_factory(
        reference_image=1,
        image_output=2,
        comparison_settings=ComparisonSettings(
            method=ComparisonMethod.SSIM, threshold=0.5
        ),
    )
    mock_compare_image = mock_safe(CompareImage)
    mock_image_repository = mock_safe(ImageRepository)
    mock_image_repository.find_by_id.side_effect = lambda x: "image" if x == 2 else None
    create_comparison_settings_edit = CreateComparisonSettingsEdit(
        mock_test_edit_repository,
        mock_test_result_repository,
        mock_compare_image,
        mock_image_repository,
    )

    with pytest.raises(ValueError):
        create_comparison_settings_edit.create_edit(
            1, ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
        )
    mock_test_result_repository.save.assert_not_called()
    mock_test_edit_repository.save.assert_not_called()


def test_test_with_no_comparison_settings(test_result_factory):
    mock_test_edit_repository = mock_safe(TestEditRepository)
    mock_test_result_repository = mock_safe(TestResultRepository)
    test_result = test_result_factory(id=5, comparison_settings=None)
    mock_test_result_repository.find_by_id.return_value = test_result
    mock_compare_image = mock_safe(CompareImage)
    mock_image_repository = mock_safe(ImageRepository)
    create_comparison_settings_edit = CreateComparisonSettingsEdit(
        mock_test_edit_repository,
        mock_test_result_repository,
        mock_compare_image,
        mock_image_repository,
    )

    with pytest.raises(ValueError):
        create_comparison_settings_edit.create_edit(
            1, ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
        )


def test_can_create_should_return_true(test_result_factory):
    mock_test_edit_repository = mock_safe(TestEditRepository)
    mock_test_result_repository = mock_safe(TestResultRepository)
    test_result = test_result_factory(
        id=5, comparison_settings=ComparisonSettings(ComparisonMethod.SSIM, 0.5)
    )
    mock_test_result_repository.find_by_id.return_value = test_result
    mock_compare_image = mock_safe(CompareImage)
    mock_image_repository = mock_safe(ImageRepository)
    create_comparison_settings_edit = CreateComparisonSettingsEdit(
        mock_test_edit_repository,
        mock_test_result_repository,
        mock_compare_image,
        mock_image_repository,
    )

    result = create_comparison_settings_edit.can_create_edit(5)

    assert result == (True, None)


def test_can_create_should_return_false(test_result_factory):
    mock_test_edit_repository = mock_safe(TestEditRepository)
    mock_test_result_repository = mock_safe(TestResultRepository)
    test_result = test_result_factory(
        id=5,
        comparison_settings=ComparisonSettings(ComparisonMethod.SSIM, 0.5),
        diff_image=None,
    )
    mock_test_result_repository.find_by_id.return_value = test_result
    mock_compare_image = mock_safe(CompareImage)
    mock_image_repository = mock_safe(ImageRepository)
    mock_image_repository.find_by_id.return_value = None
    create_comparison_settings_edit = CreateComparisonSettingsEdit(
        mock_test_edit_repository,
        mock_test_result_repository,
        mock_compare_image,
        mock_image_repository,
    )

    result = create_comparison_settings_edit.can_create_edit(5)

    assert result == (False, "Can not edit test result with no output image!")
