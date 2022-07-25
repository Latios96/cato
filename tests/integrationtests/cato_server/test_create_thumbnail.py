import os
import shutil

from cato_common.domain.file import File
from cato_common.domain.image import Image
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.images.oiio_binaries_discovery import OiioBinariesDiscovery
from cato_server.images.oiio_command_executor import OiioCommandExecutor
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.create_thumbnail import CreateThumbnail
from tests.unittests.cato_server.images.test_advanced_image_comparator import (
    images_are_equal,
)
from tests.utils import mock_safe


def test_should_create_thumbnail(test_result_factory, tmp_path, test_resource_provider):
    test_result = test_result_factory(reference_image=1)
    image = Image(
        id=0,
        name="the_image.png",
        original_file_id=2,
        channels=[],
        width=1920,
        height=1080,
    )
    original_file = File(id=0, name="the_image.png", hash="hash", value_counter=0)
    saved_thumbnail_file = File(
        id=10, name="the_image.png", hash="hash", value_counter=0
    )
    saved_thumbnail_path = tmp_path / "saved_thumbnail.png"

    def save_thumbnail(path):
        shutil.copy(path, saved_thumbnail_path)
        return saved_thumbnail_file

    mock_image_repository = mock_safe(ImageRepository)
    mock_file_storage = mock_safe(AbstractFileStorage)
    mock_test_result_repository = mock_safe(TestResultRepository)
    mock_image_repository.find_by_id.return_value = image
    mock_file_storage.find_by_id.return_value = original_file
    mock_file_storage.save_file = save_thumbnail
    mock_file_storage.get_path.return_value = test_resource_provider.resource_by_name(
        os.path.join("sphere_test_images", "exr_multichannel_16_bit.exr")
    )
    create_thumbnail = CreateThumbnail(
        mock_image_repository,
        mock_file_storage,
        OiioBinariesDiscovery(),
        mock_test_result_repository,
        OiioCommandExecutor(),
        AppConfigurationDefaults().create(),
    )

    create_thumbnail.create_thumbnail(test_result)

    assert images_are_equal(
        saved_thumbnail_path,
        test_resource_provider.resource_by_name(
            os.path.join("sphere_test_images", "expected_thumbnail.png")
        ),
    )
