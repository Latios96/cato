import os

from cato.storage.sqlalchemy.sqlalchemy_simple_file_storage import (
    SqlAlchemySimpleFileStorage,
)


def test_save_file(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemySimpleFileStorage(sessionmaker_fixture, str(tmp_path))

    f = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), "test_image_white.png")
    )

    assert f.id == 1
    assert f.name == "test_image_white.png"
    assert f.md5_hash


def test_save_files(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemySimpleFileStorage(sessionmaker_fixture, str(tmp_path))

    f = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), "test_image_white.png")
    )
    f = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), "test_image_black.png")
    )

    assert len(os.listdir(str(tmp_path))) == 2


def test_save_stream(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemySimpleFileStorage(sessionmaker_fixture, str(tmp_path))

    f = file_storage.save_stream(
        "test_image_white.png",
        open(os.path.join(os.path.dirname(__file__), "test_image_white.png"), "rb"),
    )

    assert f.id == 1
    assert f.name == "test_image_white.png"
    assert f.md5_hash


def test_get_stream(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemySimpleFileStorage(sessionmaker_fixture, str(tmp_path))
    f = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), "test_image_white.png")
    )

    stream = file_storage.get_read_stream(f)

    assert stream
    assert stream.readlines()


def test_get_path(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemySimpleFileStorage(sessionmaker_fixture, str(tmp_path))
    f = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), "test_image_white.png")
    )

    path = file_storage.get_path(f)

    assert path
    assert path == os.path.join(str(tmp_path), str(f.id), f.name)
