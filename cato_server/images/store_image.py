import logging
import os
import tempfile

from PIL import Image as PillowImage

from cato_common.domain.file import File
from cato_common.domain.image import Image, ImageChannel, ImageTranscodingState
from cato_server.images.image_splitter import ImageSplitter
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository

logger = logging.getLogger(__name__)


class StoreImage:
    def __init__(
        self,
        file_storage: AbstractFileStorage,
        image_repository: ImageRepository,
        image_splitter: ImageSplitter,
    ):
        self._file_storage = file_storage
        self._image_repository = image_repository
        self._image_splitter = image_splitter

    def store_image(self, path: str) -> Image:
        if not os.path.exists(path):
            raise ValueError(f"Image {path} does not exist!")
        logger.info("Storing original file %s in db..", path)
        original_file = self._file_storage.save_file(path)
        logger.info("Stored original file %s to %s", path, original_file)

        return self.store_image_from_file_entity(original_file)

    def store_image_from_file_entity(self, original_file: File) -> Image:
        image = self.store_image_for_transcoding(original_file)
        image = self.transcode_image(image)
        return image

    def store_image_for_transcoding(self, original_file: File) -> Image:
        image = Image(
            id=0,
            name=original_file.name,
            original_file_id=original_file.id,
            channels=[],
            width=0,
            height=0,
            transcoding_state=ImageTranscodingState.WAITING_FOR_TRANSCODING,
        )
        logger.info("Saving image %s to db..", image)
        image = self._image_repository.save(image)
        logger.info("Saved image with id %s", image.id)
        return image

    def transcode_image(self, image: Image) -> Image:
        try:
            self._transcode(image)
        except Exception as e:
            logger.error(e)
            logger.error("Image will be saved as UNABLE_TO_TRANSCODE")
            image.transcoding_state = ImageTranscodingState.UNABLE_TO_TRANSCODE
            self._image_repository.save(image)
            raise e

        image = self._image_repository.save(image)
        logger.info("Updated image with id %s", image.id)

        return image

    def _transcode(self, image):
        original_file = self._file_storage.find_by_id(image.original_file_id)
        if not original_file:
            raise RuntimeError(
                f"Did not expect to not find an Image with id {image.id} in the db.",
            )

        logger.info("Splitting image into channels..")
        channel_files = []
        with tempfile.TemporaryDirectory() as tmpdirname:
            channels = self._image_splitter.split_image_into_channels(
                self._file_storage.get_path(original_file), tmpdirname
            )
            logger.debug("Image has channels %s", channels)
            for channel_name, channel_path in channels:
                logger.debug("Saving channel %s to db..", channel_name)
                channel_file = self._file_storage.save_file(channel_path)
                logger.debug("Saved channel %s to %s", channel_name, channel_file)
                channel_files.append(
                    ImageChannel(
                        id=0,
                        image_id=image.id,
                        name=channel_name,
                        file_id=channel_file.id,
                    )
                )

            width, height = self._get_image_resolution(channels)

            logger.debug("Removing temporary directory..")
        image.channels = channel_files
        image.width = width
        image.height = height
        image.transcoding_state = ImageTranscodingState.TRANSCODED

    def _get_image_resolution(self, channels):
        for channel_name, channel_path in channels:
            if channel_name == "rgb":
                im = PillowImage.open(channel_path)
                return im.size
