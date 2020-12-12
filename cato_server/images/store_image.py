import os
import tempfile
from collections import defaultdict
from typing import List

from oiio.OpenImageIO import ImageBuf, ImageBufAlgo

from cato.domain.image import Image, Channel
from cato.image_utils.image_conversion import ImageConversionError
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage

import logging

from cato_server.storage.abstract.abstract_image_repository import ImageRepository

logger = logging.getLogger(__name__)


class StoreImage:
    def __init__(
        self, file_storage: AbstractFileStorage, image_repository: ImageRepository
    ):
        self._file_storage = file_storage
        self._image_repository = image_repository

    def store_image(self, path: str) -> Image:
        logger.info("Storing original file %s in db..", path)
        original_file = self._file_storage.save_file(path)
        logger.info("Stored original file %s to %s", path, original_file)

        logger.info("Reading image %s", path)
        buf = ImageBuf(path)

        indices_and_name = self._channel_indices_and_name(buf.spec().channelnames)

        total_channel_number = len(indices_and_name.items())
        logger.info("Found %s channels in image", total_channel_number)

        channel_files = []

        with tempfile.TemporaryDirectory() as tmpdirname:
            for i, (name, indices) in enumerate(indices_and_name.items()):
                channel_buf = ImageBufAlgo.channels(buf, tuple(indices))
                target_path = os.path.join(
                    tmpdirname, self._channel_file_name(path, name)
                )
                logger.info(
                    "Writing channel %s (%s of %s) to %s",
                    name,
                    i + 1,
                    total_channel_number,
                    target_path,
                )
                ok = channel_buf.write(target_path)

                if not ok:
                    raise ImageConversionError(
                        "Error when writing channel {} to {}".format(name, target_path)
                    )

                logger.info("Saving channel %s to db..", name)
                channel_file = self._file_storage.save_file(target_path)
                logger.info("Saved channel %s to %s", name, channel_file)
                channel_files.append(Channel(name=name, file_id=channel_file.id))

            logger.info("Removing temporary directory..")

        image = Image(
            id=0,
            name=os.path.basename(path),
            original_file_id=original_file.id,
            channels=channel_files,
        )
        logger.info("Saving image %s to db..", image)
        image = self._image_repository.save(image)
        logger.info("Saved image with id %s", image.id)
        return image

    def _channel_indices_and_name(self, channelnames: List[str]):
        names_indices = defaultdict(list)
        for i, name in enumerate(channelnames):
            key = self.__get_key(name)
            names_indices[key].append(i)
        return names_indices

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

    def _channel_file_name(self, path, channel_name):
        basename, ext = os.path.splitext(os.path.basename(path))
        extension = f".{channel_name}.png" if channel_name else ".png"
        return basename + extension
