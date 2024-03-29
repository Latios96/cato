import os

from cato_server.storage.sqlalchemy.sqlalchemy_simple_file_storage import (
    SqlAlchemySimpleFileStorage,
)

TEST_IMAGE_WHITE_PNG = "test_image_white.png"


def test_save_file(sqlalchemy_simple_file_storage, test_resource_provider):
    f = sqlalchemy_simple_file_storage.save_file(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG)
    )

    assert f.id == 1
    assert f.name == TEST_IMAGE_WHITE_PNG
    assert f.hash


def test_save_files(sqlalchemy_simple_file_storage, tmp_path, test_resource_provider):
    sqlalchemy_simple_file_storage.save_file(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG)
    )
    sqlalchemy_simple_file_storage.save_file(
        test_resource_provider.resource_by_name("test_image_black.png")
    )

    assert len(os.listdir(str(tmp_path))) == 2


def test_save_stream(sqlalchemy_simple_file_storage, test_resource_provider):
    f = sqlalchemy_simple_file_storage.save_stream(
        TEST_IMAGE_WHITE_PNG,
        open(test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG), "rb"),
    )

    assert f.id == 1
    assert f.name == TEST_IMAGE_WHITE_PNG
    assert f.hash


def test_get_stream(sqlalchemy_simple_file_storage, test_resource_provider):
    f = sqlalchemy_simple_file_storage.save_file(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG)
    )

    stream = sqlalchemy_simple_file_storage.get_read_stream(f)

    assert stream
    assert stream.readlines()


def test_get_path(sqlalchemy_simple_file_storage, tmp_path, test_resource_provider):
    f = sqlalchemy_simple_file_storage.save_file(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG)
    )

    path = sqlalchemy_simple_file_storage.get_path(f)

    assert path
    assert path == os.path.join(str(tmp_path), str(f.id), f.name)


def test_find_by_id(sqlalchemy_simple_file_storage, test_resource_provider):
    f = sqlalchemy_simple_file_storage.save_stream(
        TEST_IMAGE_WHITE_PNG,
        open(test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG), "rb"),
    )

    assert sqlalchemy_simple_file_storage.find_by_id(f.id).id == f.id
