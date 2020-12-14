from cato.domain.image import ImageChannel, Image
from cato.mappers.image_class_mapper import ImageClassMapper


def test_from_dict_with_id():
    mapper = ImageClassMapper()

    result = mapper.map_from_dict(
        {
            "id": 1,
            "name": "test.exr",
            "original_file_id": 3,
            "channels": [{"id": 1, "image_id": 2, "name": "rgb", "file_id": 3}],
        }
    )

    assert result == Image(
        id=1,
        name="test.exr",
        original_file_id=3,
        channels=[ImageChannel(id=1, image_id=2, name="rgb", file_id=3)],
    )


def test_to_dict():
    mapper = ImageClassMapper()

    result = mapper.map_to_dict(
        Image(
            id=1,
            name="test.exr",
            original_file_id=3,
            channels=[ImageChannel(id=1, image_id=2, name="rgb", file_id=3)],
        )
    )

    assert result == {
        "id": 1,
        "name": "test.exr",
        "original_file_id": 3,
        "channels": [{"id": 1, "image_id": 2, "name": "rgb", "file_id": 3}],
    }
