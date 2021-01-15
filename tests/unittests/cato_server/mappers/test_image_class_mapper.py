from cato_server.domain.image import ImageChannel, Image
from cato_server.mappers.internal.image_class_mapper import ImageClassMapper


def test_from_dict_with_id():
    mapper = ImageClassMapper()

    result = mapper.map_from_dict(
        {
            "id": 1,
            "name": "test.exr",
            "original_file_id": 3,
            "channels": [{"id": 1, "image_id": 2, "name": "rgb", "file_id": 3}],
            "width": 100,
            "height": 100,
        }
    )

    assert result == Image(
        id=1,
        name="test.exr",
        original_file_id=3,
        channels=[ImageChannel(id=1, image_id=2, name="rgb", file_id=3)],
        width=100,
        height=100,
    )


def test_to_dict():
    mapper = ImageClassMapper()

    result = mapper.map_to_dict(
        Image(
            id=1,
            name="test.exr",
            original_file_id=3,
            channels=[ImageChannel(id=1, image_id=2, name="rgb", file_id=3)],
            width=100,
            height=100,
        )
    )

    assert result == {
        "id": 1,
        "name": "test.exr",
        "original_file_id": 3,
        "channels": [{"id": 1, "image_id": 2, "name": "rgb", "file_id": 3}],
        "width": 100,
        "height": 100,
    }
