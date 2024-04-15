import pytest

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.compare_image_result import CompareImageResult
from cato_common.domain.result_status import ResultStatus
from cato_server.images.store_image import StoreImage
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.task_queue.compare_image_task import (
    CompareImageTask,
    CompareImageParams,
)
from cato_server.usecases.compare_image import CompareImage
from tests.utils import mock_safe


@pytest.fixture
def test_context(object_mapper):
    class TestContext:
        def __init__(self):
            self.mock_compare_image = mock_safe(CompareImage)
            self.mock_file_storage = mock_safe(AbstractFileStorage)
            self.mock_store_image = mock_safe(StoreImage)
            self.compare_image_result = CompareImageResult(
                status=ResultStatus.SUCCESS,
                message="",
                reference_image_id=3,
                output_image_id=1,
                diff_image_id=2,
                error=1,
            )
            self.mock_compare_image.compare_image_from_db.return_value = (
                self.compare_image_result
            )
            self.compare_image_task = CompareImageTask(
                object_mapper,
                self.mock_file_storage,
                self.mock_store_image,
                self.mock_compare_image,
            )

    return TestContext()


def test_compare_images_successfully(
    test_context, stored_file_factory, stored_image_factory
):
    output_image_file = stored_file_factory(id=1)
    reference_image_file = stored_file_factory(id=2)
    test_context.mock_file_storage.find_by_id.side_effect = lambda x: (
        output_image_file if x == 1 else reference_image_file
    )
    output_image = stored_image_factory(id=1)
    reference_image = stored_image_factory(id=2)
    test_context.mock_store_image.store_image_from_file_entity.side_effect = lambda x: (
        output_image if x.id == output_image_file.id else reference_image
    )
    compare_image_settings = ComparisonSettings.default()
    compare_image_params = CompareImageParams(
        output_image_file.id, reference_image_file.id, compare_image_settings
    )

    compare_image_result = test_context.compare_image_task._execute(
        compare_image_params
    )

    assert compare_image_result == test_context.compare_image_result
    test_context.mock_compare_image.compare_image_from_db.assert_called_with(
        output_image, reference_image, compare_image_settings
    )
    test_context.mock_file_storage.find_by_id.assert_any_call(1)
    test_context.mock_file_storage.find_by_id.assert_any_call(2)


def test_no_output_image_in_db_should_fail(test_context, stored_file_factory):
    reference_image_file = stored_file_factory(id=2)
    test_context.mock_file_storage.find_by_id.side_effect = lambda x: (
        reference_image_file if x == 2 else None
    )
    compare_image_settings = ComparisonSettings.default()
    compare_image_params = CompareImageParams(
        1, reference_image_file.id, compare_image_settings
    )

    with pytest.raises(RuntimeError):
        test_context.compare_image_task._execute(compare_image_params)


def test_no_reference_image_in_db_should_fail(test_context, stored_file_factory):
    output_image_file = stored_file_factory(id=1)
    test_context.mock_file_storage.find_by_id.side_effect = lambda x: (
        output_image_file if x == 1 else None
    )
    compare_image_settings = ComparisonSettings.default()
    compare_image_params = CompareImageParams(
        output_image_file.id, 2, compare_image_settings
    )

    with pytest.raises(RuntimeError):
        test_context.compare_image_task._execute(compare_image_params)
