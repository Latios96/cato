from pathlib import Path

import pytest

from cato_common.domain.file import File
from cato_common.domain.image import Image, ImageTranscodingState
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.images.oiio_binaries_discovery import OiioBinariesDiscovery
from cato_server.images.oiio_command_executor import OiioCommandExecutor
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.create_thumbnail import CreateThumbnail
from tests.utils import mock_safe


def _touch_output_file(command):
    path = command.split("-o ")[1]
    Path(path).touch()


@pytest.fixture
def test_context(test_result_factory):
    class TestContext:
        def __init__(self):
            self.test_result = test_result_factory()
            self.image = Image(
                id=0,
                name="the_image.png",
                original_file_id=2,
                channels=[],
                width=1920,
                height=1080,
                transcoding_state=ImageTranscodingState.TRANSCODED,
            )
            self.original_file = File(
                id=0, name="the_image.png", hash="hash", value_counter=0
            )
            self.saved_thumbnail_file = File(
                id=10, name="the_image.png", hash="hash", value_counter=0
            )
            self.mock_image_repository = mock_safe(ImageRepository)
            self.mock_file_storage = mock_safe(AbstractFileStorage)
            self.mock_test_result_repository = mock_safe(TestResultRepository)
            self.mock_oiio_command_executor = mock_safe(OiioCommandExecutor)
            self.mock_image_repository.find_by_id.return_value = self.image
            self.mock_file_storage.find_by_id.return_value = self.original_file
            self.mock_file_storage.save_file.return_value = self.saved_thumbnail_file
            self.mock_oiio_command_executor.execute_command = _touch_output_file
            self.create_thumbnail = CreateThumbnail(
                self.mock_image_repository,
                self.mock_file_storage,
                OiioBinariesDiscovery(),
                self.mock_test_result_repository,
                self.mock_oiio_command_executor,
                AppConfigurationDefaults().create(),
            )

    return TestContext()


def test_should_create_thumbnail_with_success(test_context):
    test_context.test_result.reference_image = 20
    test_context.create_thumbnail.create_thumbnail(test_context.test_result)

    test_context.mock_test_result_repository.save.assert_called_with(
        test_context.test_result
    )
    assert test_context.test_result.thumbnail_file_id == 10
    test_context.mock_file_storage.save_file.assert_called_once()


def test_should_resolve_image_id_to_reference_image(test_context):
    test_context.test_result.reference_image = 20

    test_context.create_thumbnail.create_thumbnail(test_context.test_result)

    test_context.mock_image_repository.find_by_id.assert_called_with(20)


def test_should_resolve_image_id_to_output_image(test_context):
    test_context.test_result.reference_image = None
    test_context.test_result.image_output = 30

    test_context.create_thumbnail.create_thumbnail(test_context.test_result)

    test_context.mock_image_repository.find_by_id.assert_called_with(30)


def test_should_resolve_image_id_to_None(test_context):
    test_context.test_result.reference_image = None
    test_context.test_result.image_output = None

    with pytest.raises(ValueError):
        test_context.create_thumbnail.create_thumbnail(test_context.test_result)

    test_context.mock_image_repository.find_by_id.assert_not_called()


def test_image_not_found_should_throw_exception(test_context):
    test_context.mock_image_repository.find_by_id.return_value = None

    with pytest.raises(ValueError):
        test_context.create_thumbnail.create_thumbnail(test_context.test_result)


def test_file_not_found_should_throw_exception(test_context):
    test_context.mock_file_storage.find_by_id.return_value = None

    with pytest.raises(ValueError):
        test_context.create_thumbnail.create_thumbnail(test_context.test_result)


def test_thumbnail_file_not_written_should_throw_exception(test_context):
    test_context.test_result.reference_image = 20
    test_context.mock_oiio_command_executor.execute_command = lambda x: x

    with pytest.raises(RuntimeError):
        test_context.create_thumbnail.create_thumbnail(test_context.test_result)
