import pytest

from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.task_queue.create_thumbnail_task import (
    CreateThumbnailTask,
    CreateThumbnailParams,
)
from cato_server.usecases.create_thumbnail import CreateThumbnail
from tests.utils import mock_safe


@pytest.fixture
def test_context(object_mapper):
    class TestContext:
        def __init__(self):
            self.mock_test_result_repository = mock_safe(TestResultRepository)
            self.mock_create_thumbnail = mock_safe(CreateThumbnail)
            self.create_thumbnail_task = CreateThumbnailTask(
                object_mapper,
                self.mock_test_result_repository,
                self.mock_create_thumbnail,
            )

    return TestContext()


def test_should_call_create_thumbnail_successfully(test_context, test_result_factory):
    test_result = test_result_factory(id=42)
    test_context.mock_test_result_repository.find_by_id.return_value = test_result

    test_context.create_thumbnail_task._execute(
        CreateThumbnailParams(test_result_id=test_result.id)
    )

    test_context.mock_create_thumbnail.create_thumbnail.assert_called_with(test_result)


def test_should_throw_if_test_result_not_found(test_context):
    test_context.mock_test_result_repository.find_by_id.return_value = None

    with pytest.raises(RuntimeError):
        test_context.create_thumbnail_task._execute(
            CreateThumbnailParams(test_result_id=42)
        )
