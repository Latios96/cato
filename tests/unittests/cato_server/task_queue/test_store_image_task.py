import pytest

from cato_common.dtos.store_image_result import StoreImageResult
from cato_server.images.store_image import StoreImage
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.task_queue.store_image_task import StoreImageTask, StoreImageParams
from tests.utils import mock_safe


@pytest.fixture
def test_context(object_mapper):
    class TestContext:
        def __init__(self):
            self.mock_file_storage = mock_safe(AbstractFileStorage)
            self.mock_store_image = mock_safe(StoreImage)
            self.store_image_task = StoreImageTask(
                object_mapper,
                self.mock_file_storage,
                self.mock_store_image,
            )

    return TestContext()


def test_should_call_store_image_successfully(
    test_context, stored_file_factory, stored_image_factory
):
    original_file = stored_file_factory()
    expected_stored_image = stored_image_factory()
    test_context.mock_file_storage.find_by_id.return_value = original_file
    test_context.mock_store_image.store_image_from_file_entity.return_value = (
        expected_stored_image
    )

    stored_image = test_context.store_image_task._execute(
        StoreImageParams(original_file_id=original_file.id)
    )

    assert stored_image == StoreImageResult(image=expected_stored_image)
    test_context.mock_store_image.store_image_from_file_entity.assert_called_with(
        original_file
    )
    test_context.mock_file_storage.find_by_id.assert_called_with(original_file.id)


def test_should_throw_if_original_file_not_found(test_context):
    test_context.mock_file_storage.find_by_id.return_value = None

    with pytest.raises(RuntimeError):
        test_context.store_image_task._execute(StoreImageParams(original_file_id=42))

    test_context.mock_file_storage.find_by_id.assert_called_with(42)
