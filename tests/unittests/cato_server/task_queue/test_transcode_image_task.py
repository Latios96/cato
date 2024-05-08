import pytest

from cato_server.images.store_image import StoreImage
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.task_queue.task import Void
from cato_server.task_queue.transcode_image_task import (
    TranscodeImageTask,
    TranscodeImageParams,
)
from tests.utils import mock_safe


@pytest.fixture
def test_context(object_mapper):
    class TestContext:
        def __init__(self):
            self.mock_file_storage = mock_safe(AbstractFileStorage)
            self.mock_image_repository = mock_safe(ImageRepository)
            self.mock_store_image = mock_safe(StoreImage)
            self.transcode_image_task = TranscodeImageTask(
                object_mapper,
                self.mock_image_repository,
                self.mock_store_image,
            )

    return TestContext()


def test_should_call_transcode_image_successfully(
    test_context, stored_file_factory, stored_image_factory
):
    image_to_transcode = stored_image_factory()
    test_context.mock_image_repository.find_by_id.return_value = image_to_transcode
    test_context.mock_store_image.transcode_image.return_value = Void()

    stored_image = test_context.transcode_image_task._execute(
        TranscodeImageParams(image_id=image_to_transcode.id)
    )

    assert stored_image == Void()
    test_context.mock_store_image.transcode_image.assert_called_with(image_to_transcode)
    test_context.mock_image_repository.find_by_id.assert_called_with(
        image_to_transcode.id
    )


def test_should_throw_if_image_not_found(test_context):
    test_context.mock_image_repository.find_by_id.return_value = None

    with pytest.raises(RuntimeError):
        test_context.transcode_image_task._execute(TranscodeImageParams(image_id=42))

    test_context.mock_image_repository.find_by_id.assert_called_with(42)
