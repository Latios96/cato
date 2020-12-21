from cato_server.domain.image import ImageChannel
from cato_server.mappers.image_channel_class_mapper import ImageChannelClassMapper


def test_from_dict_with_id():
    mapper = ImageChannelClassMapper()

    result = mapper.map_from_dict(
        {"id": 1, "image_id": 2, "name": "test.exr", "file_id": 3}
    )

    assert result == ImageChannel(id=1, image_id=2, name="test.exr", file_id=3)


def test_to_dict():
    mapper = ImageChannelClassMapper()

    result = mapper.map_to_dict(
        ImageChannel(id=1, image_id=2, name="test.exr", file_id=3)
    )

    assert result == {"id": 1, "image_id": 2, "name": "test.exr", "file_id": 3}
