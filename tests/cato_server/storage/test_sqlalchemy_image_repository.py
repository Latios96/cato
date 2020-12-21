import pytest
from sqlalchemy.exc import IntegrityError

from cato_server.domain.image import Image, ImageChannel
from cato_server.storage.sqlalchemy.sqlalchemy_image_repository import (
    SqlAlchemyImageRepository,
)


def test_should_save(sessionmaker_fixture, stored_file):
    image_repository = SqlAlchemyImageRepository(sessionmaker_fixture)

    image = image_repository.save(
        Image(
            id=0,
            name="test.exr",
            original_file_id=stored_file.id,
            channels=[],
        )
    )

    assert image == Image(
        id=1,
        name="test.exr",
        original_file_id=stored_file.id,
        channels=[],
    )


def test_save_should_fail_not_existing_file_id(sessionmaker_fixture, stored_file):
    image_repository = SqlAlchemyImageRepository(sessionmaker_fixture)

    with pytest.raises(IntegrityError):
        image_repository.save(
            Image(
                id=0,
                name="test.exr",
                original_file_id=42,
                channels=[ImageChannel(id=0, image_id=0, name="rgb", file_id=2)],
            )
        )


def test_save_should_fail_not_existing_file_id_for_channel(
    sessionmaker_fixture, stored_file
):
    image_repository = SqlAlchemyImageRepository(sessionmaker_fixture)

    with pytest.raises(IntegrityError):
        image_repository.save(
            Image(
                id=0,
                name="test.exr",
                original_file_id=42,
                channels=[ImageChannel(id=0, image_id=0, name="rgb", file_id=42)],
            )
        )


def test_should_not_find(sessionmaker_fixture):
    image_repository = SqlAlchemyImageRepository(sessionmaker_fixture)

    assert not image_repository.find_by_id(42)


def test_should_find(sessionmaker_fixture, stored_file):
    image_repository = SqlAlchemyImageRepository(sessionmaker_fixture)

    image = image_repository.save(
        Image(
            id=0,
            name="test.exr",
            original_file_id=stored_file.id,
            channels=[
                ImageChannel(id=0, image_id=0, name="rgb", file_id=stored_file.id)
            ],
        )
    )

    assert image_repository.find_by_id(image.id) == image
