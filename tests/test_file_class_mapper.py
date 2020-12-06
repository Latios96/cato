from cato.mappers.file_class_mapper import FileClassMapper
from cato_server.storage.domain.File import File


def test_map_from_dict():
    mapper = FileClassMapper()

    result = mapper.map_from_dict({"id": 1, "name": "file_name", "hash": "the_hash"})

    assert result == File(id=1, name="file_name", hash="the_hash")


def test_map_to_dict():
    mapper = FileClassMapper()

    result = mapper.map_to_dict(File(id=1, name="file_name", hash="the_hash"))

    assert result == {"id": 1, "name": "file_name", "hash": "the_hash"}
