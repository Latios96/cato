import datetime

from cato_common.domain.can_be_edited import CanBeEdited
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.compare_image_result import CompareImageResult
from cato_common.domain.image import Image
from cato_common.domain.test_edit import ReferenceImageEdit, ReferenceImageEditValue
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.test_edit_repository import TestEditRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.compare_image import CompareImage
from cato_server.usecases.create_reference_image_edit import CreateReferenceImageEdit
from tests.utils import mock_safe

original_reference_image_id = 9


def test_can_be_edited_should_return_ok(test_result_factory):
    image = Image(
        id=1, name="test.png", original_file_id=1, channels=[], width=1920, height=1080
    )
    mock_test_edit_repository = mock_safe(TestEditRepository)
    mock_test_result_repository = mock_safe(TestResultRepository)
    mock_test_result_repository.find_by_id.return_value = test_result_factory(
        image_output=1, comparison_settings=ComparisonSettings.default()
    )
    mock_compare_image = mock_safe(CompareImage)
    mock_image_repository = mock_safe(ImageRepository)
    mock_image_repository.find_by_id.return_value = image
    create_reference_image_edit = CreateReferenceImageEdit(
        mock_test_edit_repository,
        mock_test_result_repository,
        mock_compare_image,
        mock_image_repository,
    )

    result = create_reference_image_edit.can_be_edited(1)

    assert result == CanBeEdited.yes()


def test_can_be_edited_should_return_not_ok_no_test_result_found():
    mock_test_edit_repository = mock_safe(TestEditRepository)
    mock_test_result_repository = mock_safe(TestResultRepository)
    mock_test_result_repository.find_by_id.return_value = None
    mock_compare_image = mock_safe(CompareImage)
    mock_image_repository = mock_safe(ImageRepository)
    create_reference_image_edit = CreateReferenceImageEdit(
        mock_test_edit_repository,
        mock_test_result_repository,
        mock_compare_image,
        mock_image_repository,
    )

    result = create_reference_image_edit.can_be_edited(1)

    assert result == CanBeEdited(False, "Could not find a test result with id 1")


def test_can_be_edited_should_return_not_ok_no_image_output(test_result_factory):
    mock_test_edit_repository = mock_safe(TestEditRepository)
    mock_test_result_repository = mock_safe(TestResultRepository)
    mock_test_result_repository.find_by_id.return_value = test_result_factory(
        image_output=None
    )
    mock_compare_image = mock_safe(CompareImage)
    mock_image_repository = mock_safe(ImageRepository)
    create_reference_image_edit = CreateReferenceImageEdit(
        mock_test_edit_repository,
        mock_test_result_repository,
        mock_compare_image,
        mock_image_repository,
    )

    result = create_reference_image_edit.can_be_edited(1)

    assert result == CanBeEdited(
        False, "Can't edit a test result which has no image_output!"
    )


def test_can_be_edited_should_return_not_ok_no_comparison_settings(
    test_result_factory,
):
    mock_test_edit_repository = mock_safe(TestEditRepository)
    mock_test_result_repository = mock_safe(TestResultRepository)
    mock_test_result_repository.find_by_id.return_value = test_result_factory(
        image_output=1
    )
    mock_compare_image = mock_safe(CompareImage)
    mock_image_repository = mock_safe(ImageRepository)
    create_reference_image_edit = CreateReferenceImageEdit(
        mock_test_edit_repository,
        mock_test_result_repository,
        mock_compare_image,
        mock_image_repository,
    )

    result = create_reference_image_edit.can_be_edited(1)

    assert result == CanBeEdited(
        False, "Can't edit a test result which has no comparison settings!"
    )


def test_create_reference_image_edit_with_success(test_result_factory):
    mock_test_edit_repository = mock_safe(TestEditRepository)
    mock_test_edit_repository.save.side_effect = lambda x: x
    mock_test_result_repository = mock_safe(TestResultRepository)
    original_output_image_id = 10
    mock_test_result_repository.find_by_id.return_value = test_result_factory(
        id=5,
        image_output=original_output_image_id,
        unified_test_status=UnifiedTestStatus.SUCCESS,
        message="success",
        diff_image=3,
        reference_image=original_reference_image_id,
        error_value=1,
        comparison_settings=ComparisonSettings.default(),
    )
    mock_compare_image = mock_safe(CompareImage)
    mock_compare_image.compare_image_from_db.return_value = CompareImageResult(
        status=ResultStatus.SUCCESS,
        message="still success",
        reference_image_id=11,
        output_image_id=12,
        diff_image_id=13,
        error=0.1,
    )
    mock_image_repository = mock_safe(ImageRepository)
    mock_image_repository.find_by_id.side_effect = _create_image
    create_reference_image_edit = CreateReferenceImageEdit(
        mock_test_edit_repository,
        mock_test_result_repository,
        mock_compare_image,
        mock_image_repository,
    )
    created_at = datetime.datetime(year=2021, month=original_reference_image_id, day=17)
    create_reference_image_edit._get_created_at = lambda: created_at

    reference_image_edit = create_reference_image_edit.create_edit(5)

    assert reference_image_edit == ReferenceImageEdit(
        id=0,
        test_id=5,
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test_name"),
        created_at=created_at,
        old_value=ReferenceImageEditValue(
            status=ResultStatus.SUCCESS,
            message="success",
            diff_image_id=3,
            reference_image_id=original_reference_image_id,
            error_value=1,
        ),
        new_value=ReferenceImageEditValue(
            status=ResultStatus.SUCCESS,
            message="still success",
            diff_image_id=13,
            reference_image_id=original_output_image_id,
            error_value=0.1,
        ),
    )


def _create_image(x):
    return Image(
        id=x,
        name="x.png",
        original_file_id=10,
        channels=[],
        width=1920,
        height=1080,
    )
