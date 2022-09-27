import pytest
from sqlalchemy.exc import IntegrityError

from cato_common.domain.image import Image, ImageChannel
from cato_server.storage.sqlalchemy.sqlalchemy_image_repository import (
    SqlAlchemyImageRepository,
)
from tests.unittests.cato_server.storage.conftest import sqltap_query_count_asserter


def test_should_save(sqlalchemy_image_repository, stored_file):
    image = sqlalchemy_image_repository.save(
        Image(
            id=0,
            name="test.exr",
            original_file_id=stored_file.id,
            channels=[],
            width=1920,
            height=1080,
        )
    )

    assert image == Image(
        id=1,
        name="test.exr",
        original_file_id=stored_file.id,
        channels=[],
        width=1920,
        height=1080,
    )


def test_save_should_fail_not_existing_file_id(
    sqlalchemy_image_repository, stored_file
):
    with pytest.raises(IntegrityError):
        sqlalchemy_image_repository.save(
            Image(
                id=0,
                name="test.exr",
                original_file_id=42,
                channels=[ImageChannel(id=0, image_id=0, name="rgb", file_id=2)],
                width=1920,
                height=1080,
            )
        )


def test_save_should_fail_not_existing_file_id_for_channel(
    sqlalchemy_image_repository, stored_file
):
    with pytest.raises(IntegrityError):
        sqlalchemy_image_repository.save(
            Image(
                id=0,
                name="test.exr",
                original_file_id=42,
                channels=[ImageChannel(id=0, image_id=0, name="rgb", file_id=42)],
                width=1920,
                height=1080,
            )
        )


def test_should_not_find(sqlalchemy_image_repository):
    assert not sqlalchemy_image_repository.find_by_id(42)


def test_should_find(sqlalchemy_image_repository, stored_file):
    image = sqlalchemy_image_repository.save(
        Image(
            id=0,
            name="test.exr",
            original_file_id=stored_file.id,
            channels=[
                ImageChannel(id=0, image_id=0, name="rgb", file_id=stored_file.id)
            ],
            width=1920,
            height=1080,
        )
    )

    with sqltap_query_count_asserter(1):
        image = sqlalchemy_image_repository.find_by_id(image.id)
        assert image == image
