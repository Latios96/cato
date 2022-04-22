import os

from cato_server.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)

TEST_IMAGE_BLACK_PNG = "test_image_black.png"

TEST_IMAGE_WHITE_PNG = "test_image_white.png"


def test_save_file(sqlalchemy_deduplicating_storage, test_resource_provider):
    f = sqlalchemy_deduplicating_storage.save_file(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG)
    )

    assert f.id == 1
    assert f.name == TEST_IMAGE_WHITE_PNG
    assert f.hash


def test_save_files(sqlalchemy_deduplicating_storage, tmp_path, test_resource_provider):
    sqlalchemy_deduplicating_storage.save_file(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG)
    )
    sqlalchemy_deduplicating_storage.save_file(
        test_resource_provider.resource_by_name("test_image_black.png")
    )

    assert len(os.listdir(str(tmp_path))) == 2


def test_save_stream(sqlalchemy_deduplicating_storage, test_resource_provider):
    f = sqlalchemy_deduplicating_storage.save_stream(
        TEST_IMAGE_WHITE_PNG,
        open(test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG), "rb"),
    )

    assert f.id == 1
    assert f.name == TEST_IMAGE_WHITE_PNG
    assert f.hash


def test_get_stream(sqlalchemy_deduplicating_storage, test_resource_provider):
    f = sqlalchemy_deduplicating_storage.save_file(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG)
    )

    stream = sqlalchemy_deduplicating_storage.get_read_stream(f)

    assert stream
    assert stream.readlines()


def test_get_path(sqlalchemy_deduplicating_storage, tmp_path, test_resource_provider):
    f = sqlalchemy_deduplicating_storage.save_file(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG)
    )

    path = sqlalchemy_deduplicating_storage.get_path(f)

    assert path
    assert path == os.path.join(
        str(tmp_path),
        "7d",
        "9d",
        "64",
        "90",
        "22",
        "a6",
        "5f",
        "a9",
        str(f.hash),
        "0.png",
    )


def test_find_by_id(sqlalchemy_deduplicating_storage, test_resource_provider):
    f = sqlalchemy_deduplicating_storage.save_stream(
        TEST_IMAGE_WHITE_PNG,
        open(test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG), "rb"),
    )

    assert sqlalchemy_deduplicating_storage.find_by_id(f.id).id == f.id


def test_save_same_file_should_store_one_file_on_disk(
    sqlalchemy_deduplicating_storage, tmp_path, test_resource_provider
):
    f1 = sqlalchemy_deduplicating_storage.save_file(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG)
    )

    f2 = sqlalchemy_deduplicating_storage.save_file(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG)
    )
    assert f1.name
    assert f1.id != f2.id
    assert f1.hash == f2.hash

    assert os.listdir(
        os.path.join(str(tmp_path), "7d", "9d", "64", "90", "22", "a6", "5f", "a9")
    ) == [f1.hash]
    assert os.listdir(
        os.path.join(
            str(tmp_path), "7d", "9d", "64", "90", "22", "a6", "5f", "a9", f1.hash
        )
    ) == ["0.png"]


def test_save_different_files_should_store_two_files_on_disk(
    sqlalchemy_deduplicating_storage, tmp_path, test_resource_provider
):
    f1 = sqlalchemy_deduplicating_storage.save_file(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG)
    )

    f2 = sqlalchemy_deduplicating_storage.save_file(
        test_resource_provider.resource_by_name("test_image_black.png")
    )
    assert f1.id != f2.id
    assert f1.hash != f2.hash

    assert set(os.listdir(str(tmp_path))) == {f1.hash[0:2], f2.hash[0:2]}
    assert os.listdir(
        os.path.join(
            str(tmp_path), "7d", "9d", "64", "90", "22", "a6", "5f", "a9", f1.hash
        )
    ) == ["0.png"]
    assert os.listdir(
        os.path.join(
            str(tmp_path), "a3", "f9", "d3", "7f", "98", "64", "95", "73", f2.hash
        )
    ) == ["0.png"]


def test_hash_collision_should_store_into_next_value_counter(
    session_provider_with_session, tmp_path, test_resource_provider
):
    the_hash = "7d9d649022a65fa9cf18a7dcb3bf07de41e3fd1b8fc4e8bf3d79007ef3b705bt"

    class MockHashCalculator:
        def __init__(self, content):
            pass

        def hexdigest(self):
            return the_hash

    file_storage = SqlAlchemyDeduplicatingFileStorage(
        session_provider_with_session, str(tmp_path), hash_calculatur=MockHashCalculator
    )

    f1 = file_storage.save_file(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG)
    )

    f2 = file_storage.save_file(
        test_resource_provider.resource_by_name("test_image_black.png")
    )
    assert f1.id != f2.id
    assert f1.hash == f2.hash

    assert set(os.listdir(str(tmp_path))) == {f1.hash[0:2]}
    assert set(
        os.listdir(
            os.path.join(
                str(tmp_path), "7d", "9d", "64", "90", "22", "a6", "5f", "a9", f1.hash
            )
        )
    ) == {"0.png", "1.png"}
