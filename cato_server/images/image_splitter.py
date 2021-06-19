import itertools
import logging
import os
import subprocess
from collections import defaultdict
from typing import List

logger = logging.getLogger(__name__)


class OiioBinariesDiscorvery:
    def get_iiinfo_executable(self) -> str:
        return "iinfo"

    def get_oiiotool_executable(self) -> str:
        return "oiiotool"


class ImageSplitter:
    def __init__(self, oiio_binaries_discovery: OiioBinariesDiscorvery):
        self._oiio_binaries_discovery = oiio_binaries_discovery

    def split_image_into_channels(self, image_path: str, work_folder: str) -> List[str]:
        channels = self._parse_channels(image_path)
        logger.info("Image has channels %s", channels)

        return self._extract_channels(image_path, channels, work_folder)

    def _parse_channels(self, image_path: str):
        logger.info("Parsing channels for image %s", image_path)
        command = (
            f"{self._oiio_binaries_discovery.get_iiinfo_executable()} -v {image_path}"
        )
        logger.debug("Running command %s", command)
        status, output = subprocess.getstatusoutput(command)

        if status != 0:
            raise Exception(
                f"Exit code f{status} when running command {command}: output was: {output}"
            )

        lines = output.split("\n")
        lines = map(lambda x: x.strip(), lines)
        lines = filter(lambda x: x.startswith("channel list"), lines)
        lines = map(lambda x: x.replace("channel list: ", ""), lines)
        lines_ = list(lines)
        matches = itertools.chain(*map(lambda x: x.split(", "), lines_))
        matches = map(lambda x: x.split(" ")[0], matches)
        channels = list(matches)

        return channels

    def _extract_channels(self, image_path: str, channels: List[str], work_folder: str):
        images_to_channels = defaultdict(list)
        for channel in channels:
            images_to_channels[self.__get_key(channel)].append(channel)

        channel_paths = []

        for image_suffix, channels in images_to_channels.items():
            logger.info("Extracting channel %s", image_suffix)
            name, ext = os.path.splitext(image_path)
            target_image = os.path.join(
                work_folder, f"{os.path.basename(name)}.{image_suffix}.png"
            )
            command = f"{self._oiio_binaries_discovery.get_oiiotool_executable()} {image_path} --ch {','.join(channels)} -o {target_image}"
            logger.debug("Running command %s", command)
            status, output = subprocess.getstatusoutput(command)
            if status != 0:
                raise Exception(
                    f"Exit code f{status} when running command {command}: output was: {output}"
                )

            channel_paths.append(target_image)

        return channel_paths

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
