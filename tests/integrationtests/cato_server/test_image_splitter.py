import os.path
from pathlib import Path

import pytest

from cato_server.images.image_splitter import ImageSplitter, OiioBinariesDiscorvery


@pytest.mark.parametrize(
    "image_name,expected_channel_names",
    [
        ("exr_singlechannel_16_bit.exr", ["rgb", "alpha"]),
        ("jpeg.jpg", ["rgb"]),
        ("png_8_bit.png", ["rgb", "alpha"]),
        ("exr_multichannel_16_bit.exr", ["rgb", "alpha"]),
    ],
)
def test_split_exr_image(
    test_resource_provider, tmp_path: Path, image_name, expected_channel_names
):
    image_name_without_extension = os.path.splitext(image_name)[0]
    image_splitter = ImageSplitter(OiioBinariesDiscorvery())

    channel_paths = image_splitter.split_image_into_channels(
        test_resource_provider.resource_by_name(
            os.path.join("sphere_test_images", image_name)
        ),
        str(tmp_path),
    )

    for channel_name in expected_channel_names:
        rgb_channel_path = tmp_path.joinpath(
            f"{image_name_without_extension}.{channel_name}.png"
        )
        assert rgb_channel_path.exists()
        assert str(rgb_channel_path) in channel_paths
