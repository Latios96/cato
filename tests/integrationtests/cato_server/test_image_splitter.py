import os.path
from pathlib import Path

import pytest

from cato_server.images.image_splitter import ImageSplitter, NotAnImageException
from cato_server.images.oiio_binaries_discovery import OiioBinariesDiscovery


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
    image_splitter = ImageSplitter(OiioBinariesDiscovery())

    channels = image_splitter.split_image_into_channels(
        test_resource_provider.resource_by_name(
            os.path.join("sphere_test_images", image_name)
        ),
        str(tmp_path),
    )

    for i, channel_name in enumerate(expected_channel_names):
        assert channel_name == channels[i][0]

        rgb_channel_path = tmp_path.joinpath(
            f"{image_name_without_extension}.{channel_name}.png"
        )
        assert rgb_channel_path.exists()
        assert (channel_name, str(rgb_channel_path)) in channels


def test_split_non_image(tmp_path: Path):
    image_splitter = ImageSplitter(OiioBinariesDiscovery())

    with pytest.raises(NotAnImageException):
        image_splitter.split_image_into_channels(__file__, str(tmp_path))
