from cato_common.domain.image import ImageChannel


def test_from_dict_with_id(object_mapper):
    result = object_mapper.from_dict(
        {"id": 1, "image_id": 2, "name": "test.exr", "file_id": 3}, ImageChannel
    )

    assert result == ImageChannel(id=1, image_id=2, name="test.exr", file_id=3)


def test_to_dict(object_mapper):
    result = object_mapper.to_dict(
        ImageChannel(id=1, image_id=2, name="test.exr", file_id=3)
    )

    assert result == {"id": 1, "image_id": 2, "name": "test.exr", "file_id": 3}
