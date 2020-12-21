import logging
import os
import tempfile

from flask import Blueprint, jsonify, request, send_file, abort

from cato_server.mappers.image_class_mapper import ImageClassMapper
from cato_server.images.store_image import StoreImage
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository

logger = logging.getLogger(__name__)


class ImagesBlueprint(Blueprint):
    def __init__(
        self, file_storage: AbstractFileStorage, image_repository: ImageRepository
    ):
        super(ImagesBlueprint, self).__init__("images", __name__)
        self._file_storage = file_storage
        self._image_repository = image_repository

        self.route("images", methods=["POST"])(self.upload_file)
        self.route("images/original_file/<int:file_id>", methods=["GET"])(
            self.get_original_image_file
        )
        self.route("images/<int:image_id>", methods=["GET"])(self.get_image)

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

    def get_original_image_file(self, file_id: int):
        image = self._image_repository.find_by_id(file_id)
        file = self._file_storage.find_by_id(image.original_file_id)
        file_path = self._file_storage.get_path(file)
        if file and os.path.exists(file_path):
            return send_file(file_path, attachment_filename=file.name)
        return jsonify({"file_id": "No file found!"}), 404

    def get_image(self, image_id):
        image = self._image_repository.find_by_id(image_id)
        if not image:
            abort(404)
        return jsonify(ImageClassMapper().map_to_dict(image)), 200
