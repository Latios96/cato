import os

from cato_server.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)

TEST_IMAGE_BLACK_PNG = "test_image_black.png"

TEST_IMAGE_WHITE_PNG = "test_image_white.png"


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

    assert os.listdir(str(tmp_path)) == [f1.hash + ".png"]


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

    assert set(os.listdir(str(tmp_path))) == {f1.hash + ".png", f2.hash + ".png"}
