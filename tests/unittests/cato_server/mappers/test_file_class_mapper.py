from cato_server.mappers.internal.file_class_mapper import FileClassMapper
from cato_server.domain.file import File


def test_map_from_dict():
    mapper = FileClassMapper()

    result = mapper.map_from_dict(
        {"id": 1, "name": "file_name", "hash": "the_hash", "value_counter": 0}
    )

    assert result == File(id=1, name="file_name", hash="the_hash", value_counter=0)


def test_map_to_dict():
    mapper = FileClassMapper()

    result = mapper.map_to_dict(
        File(id=1, name="file_name", hash="the_hash", value_counter=0)
    )

    assert result == {
        "id": 1,
        "name": "file_name",
        "hash": "the_hash",
        "value_counter": 0,
    }