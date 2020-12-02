import os

from cato.storage.sqlalchemy.sqlalchemy_simple_file_storage import (
    SqlAlchemySimpleFileStorage,
)

TEST_IMAGE_WHITE_PNG = "test_image_white.png"


def test_save_file(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemySimpleFileStorage(sessionmaker_fixture, str(tmp_path))

    f = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG)
    )

    assert f.id == 1
    assert f.name == TEST_IMAGE_WHITE_PNG
    assert f.hash


def test_save_files(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemySimpleFileStorage(sessionmaker_fixture, str(tmp_path))

    file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG)
    )
    file_storage.save_file(
        os.path.join(os.path.dirname(__file__), "test_image_black.png")
    )

    assert len(os.listdir(str(tmp_path))) == 2


def test_save_stream(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemySimpleFileStorage(sessionmaker_fixture, str(tmp_path))

    f = file_storage.save_stream(
        TEST_IMAGE_WHITE_PNG,
        open(os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG), "rb"),
    )

    assert f.id == 1
    assert f.name == TEST_IMAGE_WHITE_PNG
    assert f.hash


def test_get_stream(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemySimpleFileStorage(sessionmaker_fixture, str(tmp_path))
    f = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG)
    )

    stream = file_storage.get_read_stream(f)

    assert stream
    assert stream.readlines()


def test_get_path(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemySimpleFileStorage(sessionmaker_fixture, str(tmp_path))
    f = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG)
    )

    path = file_storage.get_path(f)

    assert path
    assert path == os.path.join(str(tmp_path), str(f.id), f.name)


def test_find_by_id(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemySimpleFileStorage(sessionmaker_fixture, str(tmp_path))

    f = file_storage.save_stream(
        TEST_IMAGE_WHITE_PNG,
        open(os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG), "rb"),
    )

    assert file_storage.find_by_id(f.id).id == f.id
