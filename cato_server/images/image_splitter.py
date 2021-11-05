import itertools
import logging
import os
import subprocess
from collections import defaultdict
from typing import List, Tuple, Iterable

from cato_server.images.oiio_binaries_discovery import OiioBinariesDiscovery
from cato_server.utils.commands_builder import CommandsBuilder

logger = logging.getLogger(__name__)


class NotAnImageException(Exception):
    def __init__(self, output):
        super(NotAnImageException, self).__init__(f"The file is not an Image! {output}")


class ImageSplitter:
    def __init__(self, oiio_binaries_discovery: OiioBinariesDiscovery):
        self._oiio_binaries_discovery = oiio_binaries_discovery

    def split_image_into_channels(
        self, image_path: str, work_folder: str
    ) -> List[Tuple[str, str]]:
        channels = self._parse_channels(image_path)
        logger.debug("Image has channels %s", channels)

        return self._extract_channels(image_path, channels, work_folder)

    def _parse_channels(self, image_path: str) -> List[str]:
        logger.debug("Parsing channels for image %s", image_path)
        command = (
            f'{self._oiio_binaries_discovery.get_iiinfo_executable()} -v "{image_path}"'
        )
        logger.debug("Running command %s", command)
        status, output = subprocess.getstatusoutput(command)
        self._handle_command_error(command, status, output)

        lines: Iterable[str] = output.split("\n")
        lines = map(lambda x: x.strip(), lines)
        lines = filter(lambda x: x.startswith("channel list"), lines)
        lines = map(lambda x: x.replace("channel list: ", ""), lines)
        lines_ = list(lines)
        matches = itertools.chain(*map(lambda x: x.split(", "), lines_))
        matches = map(lambda x: x.split(" ")[0], matches)
        channels = list(matches)

        return channels

    def _extract_channels(
        self, image_path: str, channels: List[str], work_folder: str
    ) -> List[Tuple[str, str]]:
        images_to_channels = defaultdict(list)
        for channel in channels:
            images_to_channels[self.__get_key(channel)].append(channel)

        channel_paths = []
        command_base = f"{self._oiio_binaries_discovery.get_oiiotool_executable()}"
        commands_builder = CommandsBuilder(command_base, 8000)

        for channel_name, channels in images_to_channels.items():
            logger.debug("Extracting channel %s", channel_name)
            name, ext = os.path.splitext(image_path)
            target_image = os.path.join(
                work_folder, f"{os.path.basename(name)}.{channel_name}.png"
            )
            channel_paths.append((channel_name, target_image))
            image_cmd_part = (
                f' -i "{image_path}" --ch {",".join(channels)} -o "{target_image}"'
            )
            commands_builder.push(image_cmd_part)

        commands = commands_builder.finalize()
        for command in commands:
            logger.info("Running command %s", command)
            status, output = subprocess.getstatusoutput(command)
            self._handle_command_error(command, status, output)

        return channel_paths

    def _run_cmd(self, command):
        logger.debug("Running command %s", command)
        status, output = subprocess.getstatusoutput(command)
        return command, status, output

    def __get_key(self, name):
        if name in ["R", "G", "B"]:
            key = "rgb"
        elif name == "A":
            key = "alpha"
        elif name == "Z":
            key = "depth"
        else:
            key = name.split(".")[0]
        return key

    def _handle_command_error(self, command, status, output):
        logger.debug(output)
        if not output.startswith("iinfo ERROR") and not output.startswith(
            "oiiotool ERROR"
        ):
            return
        is_not_an_image = any(
            message in output
            for message in [
                "OpenImageIO could not find a format reader",
                "Not a PNG file",
                "Empty file",
                "is not an OpenEXR file",
                "Cannot read TIFF header",
            ]
        )

        if is_not_an_image:
            raise NotAnImageException(output)

        if status == 0:
            return

        raise Exception(
            f"Exit code f{status} when running command {command}: output was: {output}"
        )
