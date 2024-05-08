from unittest import mock

import pytest
from cato_common.domain.image import ImageChannel, Image, ImageTranscodingState
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.images.image_splitter import ImageSplitter
from cato_server.images.oiio_command_executor import (
    NotAnImageException,
    OiioCommandExecutor,
)
from cato_server.images.oiio_binaries_discovery import OiioBinariesDiscovery

from cato_server.images.store_image import StoreImage
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)
from cato_server.storage.sqlalchemy.sqlalchemy_image_repository import (
    SqlAlchemyImageRepository,
)
from tests.utils import mock_safe


def test_store_rgb_jpeg(
    sqlalchemy_deduplicating_storage,
    sqlalchemy_image_repository,
    tmp_path,
    test_resource_provider,
):
    store_image = StoreImage(
        sqlalchemy_deduplicating_storage,
        sqlalchemy_image_repository,
        ImageSplitter(
            OiioBinariesDiscovery(),
            OiioCommandExecutor(),
            AppConfigurationDefaults().create(),
        ),
    )

    image = store_image.store_image(
        test_resource_provider.resource_by_name("test_image_white.jpg")
    )

    assert image == Image(
        id=1,
        name="test_image_white.jpg",
        original_file_id=1,
        channels=[ImageChannel(id=1, image_id=1, name="rgb", file_id=2)],
        width=100,
        height=100,
        transcoding_state=ImageTranscodingState.TRANSCODED,
    )


def test_store_rgb_png(
    sqlalchemy_deduplicating_storage,
    sqlalchemy_image_repository,
    tmp_path,
    test_resource_provider,
):
    store_image = StoreImage(
        sqlalchemy_deduplicating_storage,
        sqlalchemy_image_repository,
        ImageSplitter(
            OiioBinariesDiscovery(),
            OiioCommandExecutor(),
            AppConfigurationDefaults().create(),
        ),
    )

    image = store_image.store_image(
        test_resource_provider.resource_by_name("test_image_white.png")
    )

    assert image == Image(
        id=1,
        name="test_image_white.png",
        original_file_id=1,
        channels=[ImageChannel(id=1, image_id=1, name="rgb", file_id=2)],
        width=220,
        height=224,
        transcoding_state=ImageTranscodingState.TRANSCODED,
    )


def test_store_multichannel_exr(
    sqlalchemy_deduplicating_storage,
    sqlalchemy_image_repository,
    tmp_path,
    test_resource_provider,
):
    store_image = StoreImage(
        sqlalchemy_deduplicating_storage,
        sqlalchemy_image_repository,
        ImageSplitter(
            OiioBinariesDiscovery(),
            OiioCommandExecutor(),
            AppConfigurationDefaults().create(),
        ),
    )

    image = store_image.store_image(
        test_resource_provider.resource_by_name("test_image_multichannel_exr.exr")
    )

    assert image == Image(
        id=1,
        name="test_image_multichannel_exr.exr",
        original_file_id=1,
        channels=[
            ImageChannel(id=1, image_id=1, name="rgb", file_id=2),
            ImageChannel(id=2, image_id=1, name="alpha", file_id=3),
            ImageChannel(id=3, image_id=1, name="depth", file_id=4),
            ImageChannel(id=4, image_id=1, name="normals", file_id=5),
            ImageChannel(id=5, image_id=1, name="samplerInfo", file_id=6),
            ImageChannel(id=6, image_id=1, name="velocity", file_id=7),
        ],
        width=960,
        height=540,
        transcoding_state=ImageTranscodingState.TRANSCODED,
    )


def test_store_not_existing_image(
    sqlalchemy_deduplicating_storage, sqlalchemy_image_repository, tmp_path
):
    store_image = StoreImage(
        sqlalchemy_deduplicating_storage,
        sqlalchemy_image_repository,
        ImageSplitter(
            OiioBinariesDiscovery(),
            OiioCommandExecutor(),
            AppConfigurationDefaults().create(),
        ),
    )

    with pytest.raises(ValueError):
        store_image.store_image("not_existing")


def test_store_no_image(
    sqlalchemy_deduplicating_storage, sqlalchemy_image_repository, tmp_path
):
    store_image = StoreImage(
        sqlalchemy_deduplicating_storage,
        sqlalchemy_image_repository,
        ImageSplitter(
            OiioBinariesDiscovery(),
            OiioCommandExecutor(),
            AppConfigurationDefaults().create(),
        ),
    )

    with pytest.raises(NotAnImageException):
        store_image.store_image(__file__)


def test_store_image_for_transcoding(
    sqlalchemy_deduplicating_storage,
    sqlalchemy_image_repository,
    tmp_path,
    test_resource_provider,
    stored_file,
):
    store_image = StoreImage(
        sqlalchemy_deduplicating_storage,
        sqlalchemy_image_repository,
        ImageSplitter(
            OiioBinariesDiscovery(),
            OiioCommandExecutor(),
            AppConfigurationDefaults().create(),
        ),
    )

    image = store_image.store_image_for_transcoding(stored_file)

    assert image == Image(
        id=1,
        name="test.exr",
        original_file_id=1,
        channels=[],
        width=0,
        height=0,
        transcoding_state=ImageTranscodingState.WAITING_FOR_TRANSCODING,
    )


def test_transcode_image(
    sqlalchemy_deduplicating_storage,
    sqlalchemy_image_repository,
    tmp_path,
    test_resource_provider,
):
    store_image = StoreImage(
        sqlalchemy_deduplicating_storage,
        sqlalchemy_image_repository,
        ImageSplitter(
            OiioBinariesDiscovery(),
            OiioCommandExecutor(),
            AppConfigurationDefaults().create(),
        ),
    )

    original_file = sqlalchemy_deduplicating_storage.save_file(
        test_resource_provider.resource_by_name("test_image_white.png")
    )
    image = store_image.store_image_for_transcoding(original_file)
    transcoded_image = store_image.transcode_image(image)

    assert transcoded_image == Image(
        id=1,
        name="test_image_white.png",
        original_file_id=1,
        channels=[ImageChannel(id=1, image_id=1, name="rgb", file_id=2)],
        width=220,
        height=224,
        transcoding_state=ImageTranscodingState.TRANSCODED,
    )


def test_transcode_should_fail_original_file_not_found():
    mock_file_storage = mock_safe(AbstractFileStorage)
    mock_file_storage.find_by_id.return_value = None
    mock_image_repository = mock_safe(ImageRepository)
    mock_image_splitter = mock_safe(ImageSplitter)
    store_image = StoreImage(
        mock_file_storage, mock_image_repository, mock_image_splitter
    )
    image = Image(
        0,
        name="test.exr",
        original_file_id=42,
        channels=[],
        width=0,
        height=0,
        transcoding_state=ImageTranscodingState.WAITING_FOR_TRANSCODING,
    )

    with pytest.raises(RuntimeError):
        store_image.transcode_image(image)

    mock_image_repository.save.assert_called_with(image)
    assert image.transcoding_state == ImageTranscodingState.UNABLE_TO_TRANSCODE


def test_storing_image_unable_to_transcode_should_store_unable_to_transcode():
    mock_file_storage = mock_safe(AbstractFileStorage)
    mock_file_storage.find_by_id.return_value = None
    mock_image_repository = mock_safe(ImageRepository)
    mock_image_splitter = mock_safe(ImageSplitter)
    store_image = StoreImage(
        mock_file_storage, mock_image_repository, mock_image_splitter
    )
    image = Image(
        0,
        name="test.exr",
        original_file_id=42,
        channels=[],
        width=0,
        height=0,
        transcoding_state=ImageTranscodingState.WAITING_FOR_TRANSCODING,
    )

    with mock.patch(
        "cato_server.images.store_image.StoreImage._transcode"
    ) as patch_transcode:
        patch_transcode.side_effect = Exception("Something went wrong")
        with pytest.raises(Exception):
            store_image.transcode_image(image)

    mock_image_repository.save.assert_called_with(image)
    assert image.transcoding_state == ImageTranscodingState.UNABLE_TO_TRANSCODE
