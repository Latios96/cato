from cato_common.domain.image import ImageChannel, Image, ImageTranscodingState


def test_from_dict_with_id(object_mapper):
    result = object_mapper.from_dict(
        {
            "id": 1,
            "name": "test.exr",
            "originalFileId": 3,
            "channels": [{"id": 1, "imageId": 2, "name": "rgb", "fileId": 3}],
            "width": 100,
            "height": 100,
            "transcodingState": "TRANSCODED",
        },
        Image,
    )

    assert result == Image(
        id=1,
        name="test.exr",
        original_file_id=3,
        channels=[ImageChannel(id=1, image_id=2, name="rgb", file_id=3)],
        width=100,
        height=100,
        transcoding_state=ImageTranscodingState.TRANSCODED,
    )


def test_to_dict(object_mapper):
    result = object_mapper.to_dict(
        Image(
            id=1,
            name="test.exr",
            original_file_id=3,
            channels=[ImageChannel(id=1, image_id=2, name="rgb", file_id=3)],
            width=100,
            height=100,
            transcoding_state=ImageTranscodingState.TRANSCODED,
        )
    )

    assert result == {
        "id": 1,
        "name": "test.exr",
        "originalFileId": 3,
        "channels": [{"id": 1, "imageId": 2, "name": "rgb", "fileId": 3}],
        "width": 100,
        "height": 100,
        "transcodingState": "TRANSCODED",
    }
