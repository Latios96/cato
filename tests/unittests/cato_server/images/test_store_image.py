import pytest
from cato_common.domain.image import ImageChannel, Image
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
from cato_server.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)
from cato_server.storage.sqlalchemy.sqlalchemy_image_repository import (
    SqlAlchemyImageRepository,
)


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
