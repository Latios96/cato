import os.path
import shutil
from pathlib import Path

import pytest

from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.images.image_splitter import ImageSplitter
from cato_server.images.oiio_command_executor import (
    NotAnImageException,
    OiioCommandExecutor,
)
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
def test_split_image(
    test_resource_provider, tmp_path: Path, image_name, expected_channel_names
):
    image_name_without_extension = os.path.splitext(image_name)[0]
    image_splitter = ImageSplitter(
        OiioBinariesDiscovery(),
        OiioCommandExecutor(),
        AppConfigurationDefaults().create(),
    )

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
    image_splitter = ImageSplitter(
        OiioBinariesDiscovery(),
        OiioCommandExecutor(),
        AppConfigurationDefaults().create(),
    )

    with pytest.raises(NotAnImageException):
        image_splitter.split_image_into_channels(__file__, str(tmp_path))


@pytest.mark.parametrize("extension", ["png", "jpeg", "exr", "tiff"])
def test_split_non_image_invalid_data(tmp_path: Path, extension):
    image_splitter = ImageSplitter(
        OiioBinariesDiscovery(),
        OiioCommandExecutor(),
        AppConfigurationDefaults().create(),
    )
    file_with_invalid_data = tmp_path.joinpath(f"not_a_{extension}_file.{extension}")
    file_with_invalid_data.touch()

    with pytest.raises(NotAnImageException):
        image_splitter.split_image_into_channels(
            str(file_with_invalid_data), str(tmp_path)
        )


def test_split_image_with_spaces_in_path(tmp_path: Path, test_resource_provider):
    image_splitter = ImageSplitter(
        OiioBinariesDiscovery(),
        OiioCommandExecutor(),
        AppConfigurationDefaults().create(),
    )
    test_image = test_resource_provider.resource_by_name(
        os.path.join("sphere_test_images", "png_8_bit.png")
    )
    test_image_path_with_spaces = tmp_path / "test image.png"
    shutil.copy(test_image, test_image_path_with_spaces)

    image_splitter.split_image_into_channels(
        str(test_image_path_with_spaces), str(tmp_path)
    )
