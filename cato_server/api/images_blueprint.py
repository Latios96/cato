import logging
import os
import tempfile

from flask import Blueprint, jsonify, request

from cato_server.images.store_image import StoreImage
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.abstract_image_repository import ImageRepository

logger = logging.getLogger(__name__)


class ImagesBlueprint(Blueprint):
    def __init__(
        self, file_storage: AbstractFileStorage, image_repository: ImageRepository
    ):
        super(ImagesBlueprint, self).__init__("images", __name__)
        self._file_storage = file_storage
        self._image_repository = image_repository

        self.route("images", methods=["POST"])(self.upload_file)

    def upload_file(self):
        uploaded_file = request.files["file"]
        if not uploaded_file.filename:
            return jsonify({"file": "Filename can not be empty!"}), 400

        store_image = StoreImage(self._file_storage, self._image_repository)

        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp_path = os.path.join(tmpdirname, uploaded_file.filename)
            uploaded_file.save(tmp_path)
            image = store_image.store_image(tmp_path)

            logger.info("Deleting tmpdir %s", tmpdirname)

        return jsonify(image), 201
