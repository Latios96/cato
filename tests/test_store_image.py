import os

from cato.domain.image import Channel, Image
from cato_server.images.store_image import StoreImage
from cato_server.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)
from cato_server.storage.sqlalchemy.sqlalchemy_image_repository import (
    SqlAlchemyImageRepository,
)


def test_store_rgb_jpeg(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemyDeduplicatingFileStorage(
        sessionmaker_fixture, str(tmp_path)
    )
    mock_image_repository = SqlAlchemyImageRepository(sessionmaker_fixture)
    store_image = StoreImage(file_storage, mock_image_repository)

    image = store_image.store_image(
        os.path.join(os.path.dirname(__file__), "test_image_white.jpg")
    )

    assert image == Image(
        id=1,
        name="test_image_white.jpg",
        original_file_id=1,
        channels=[Channel(name="rgb", file_id=2)],
    )


def test_store_rgb_png(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemyDeduplicatingFileStorage(
        sessionmaker_fixture, str(tmp_path)
    )
    mock_image_repository = SqlAlchemyImageRepository(sessionmaker_fixture)
    store_image = StoreImage(file_storage, mock_image_repository)

    image = store_image.store_image(
        os.path.join(os.path.dirname(__file__), "test_image_white.png")
    )

    assert image == Image(
        id=1,
        name="test_image_white.png",
        original_file_id=1,
        channels=[Channel(name="rgb", file_id=2)],
    )


def test_store_multichannel_exr(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemyDeduplicatingFileStorage(
        sessionmaker_fixture, str(tmp_path)
    )
    mock_image_repository = SqlAlchemyImageRepository(sessionmaker_fixture)
    store_image = StoreImage(file_storage, mock_image_repository)

    image = store_image.store_image(
        os.path.join(os.path.dirname(__file__), "test_image_multichannel_exr.exr")
    )

    assert image == Image(
        id=1,
        name="test_image_multichannel_exr.exr",
        original_file_id=1,
        channels=[
            Channel(name="rgb", file_id=2),
            Channel(name="alpha", file_id=3),
            Channel(name="depth", file_id=4),
            Channel(name="normals", file_id=5),
            Channel(name="samplerInfo", file_id=6),
            Channel(name="velocity", file_id=7),
        ],
    )
