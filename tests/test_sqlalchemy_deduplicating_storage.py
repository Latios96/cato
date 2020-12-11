import os

from cato_server.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)

TEST_IMAGE_BLACK_PNG = "test_image_black.png"

TEST_IMAGE_WHITE_PNG = "test_image_white.png"


def test_save_file(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemyDeduplicatingFileStorage(
        sessionmaker_fixture, str(tmp_path)
    )

    f = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG)
    )

    assert f.id == 1
    assert f.name == TEST_IMAGE_WHITE_PNG
    assert f.hash


def test_save_files(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemyDeduplicatingFileStorage(
        sessionmaker_fixture, str(tmp_path)
    )

    file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG)
    )
    file_storage.save_file(
        os.path.join(os.path.dirname(__file__), "test_image_black.png")
    )

    assert len(os.listdir(str(tmp_path))) == 2


def test_save_stream(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemyDeduplicatingFileStorage(
        sessionmaker_fixture, str(tmp_path)
    )

    f = file_storage.save_stream(
        TEST_IMAGE_WHITE_PNG,
        open(os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG), "rb"),
    )

    assert f.id == 1
    assert f.name == TEST_IMAGE_WHITE_PNG
    assert f.hash


def test_get_stream(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemyDeduplicatingFileStorage(
        sessionmaker_fixture, str(tmp_path)
    )
    f = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG)
    )

    stream = file_storage.get_read_stream(f)

    assert stream
    assert stream.readlines()


def test_get_path(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemyDeduplicatingFileStorage(
        sessionmaker_fixture, str(tmp_path)
    )
    f = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG)
    )

    path = file_storage.get_path(f)

    assert path
    assert path == os.path.join(str(tmp_path), str(f.hash), "0.png")


def test_find_by_id(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemyDeduplicatingFileStorage(
        sessionmaker_fixture, str(tmp_path)
    )

    f = file_storage.save_stream(
        TEST_IMAGE_WHITE_PNG,
        open(os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG), "rb"),
    )

    assert file_storage.find_by_id(f.id).id == f.id


def test_save_same_file_should_store_one_file_on_disk(sessionmaker_fixture, tmp_path):
    file_storage = SqlAlchemyDeduplicatingFileStorage(
        sessionmaker_fixture, str(tmp_path)
    )

    f1 = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG)
    )

    f2 = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG)
    )
    assert f1.name
    assert f1.id != f2.id
    assert f1.hash == f2.hash

    assert os.listdir(str(tmp_path)) == [f1.hash]
    assert os.listdir(os.path.join(str(tmp_path), f1.hash)) == ["0.png"]


def test_save_different_files_should_store_two_files_on_disk(
    sessionmaker_fixture, tmp_path
):
    file_storage = SqlAlchemyDeduplicatingFileStorage(
        sessionmaker_fixture, str(tmp_path)
    )

    f1 = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG)
    )

    f2 = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_BLACK_PNG)
    )
    assert f1.id != f2.id
    assert f1.hash != f2.hash

    assert set(os.listdir(str(tmp_path))) == {f1.hash, f2.hash}
    assert os.listdir(os.path.join(str(tmp_path), f1.hash)) == ["0.png"]
    assert os.listdir(os.path.join(str(tmp_path), f2.hash)) == ["0.png"]


def test_hash_collision_should_store_into_next_value_counter(
    sessionmaker_fixture, tmp_path
):
    the_hash = "7d9d649022a65fa9cf18a7dcb3bf07de41e3fd1b8fc4e8bf3d79007ef3b705bt"

    class MockHashCalculator:
        def __init__(self, content):
            pass

        def hexdigest(self):
            return the_hash

    file_storage = SqlAlchemyDeduplicatingFileStorage(
        sessionmaker_fixture, str(tmp_path), hash_calculatur=MockHashCalculator
    )

    f1 = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_WHITE_PNG)
    )

    f2 = file_storage.save_file(
        os.path.join(os.path.dirname(__file__), TEST_IMAGE_BLACK_PNG)
    )
    assert f1.id != f2.id
    assert f1.hash == f2.hash

    assert set(os.listdir(str(tmp_path))) == {f1.hash}
    assert set(os.listdir(os.path.join(str(tmp_path), f1.hash))) == {"0.png", "1.png"}
