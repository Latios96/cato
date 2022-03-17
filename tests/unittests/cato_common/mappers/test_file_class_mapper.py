from cato_common.domain.file import File


def test_map_from_dict(object_mapper):
    result = object_mapper.from_dict(
        {"id": 1, "name": "file_name", "hash": "the_hash", "value_counter": 0}, File
    )

    assert result == File(id=1, name="file_name", hash="the_hash", value_counter=0)


def test_map_to_dict(object_mapper):
    result = object_mapper.to_dict(
        File(id=1, name="file_name", hash="the_hash", value_counter=0)
    )

    assert result == {
        "id": 1,
        "name": "file_name",
        "hash": "the_hash",
        "valueCounter": 0,
    }
