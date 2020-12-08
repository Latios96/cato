import logging
import os
import tempfile

from flask import Blueprint, jsonify, request, send_file

from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from oiio.OpenImageIO import ImageBuf

logger = logging.getLogger(__name__)


class FilesBlueprint(Blueprint):
    def __init__(self, file_storage: AbstractFileStorage):
        super(FilesBlueprint, self).__init__("files", __name__)
        self._file_storage = file_storage

        self.route("/files/<int:file_id>", methods=["GET"])(self.get_file)
        self.route("files", methods=["POST"])(self.upload_file)

    def upload_file(self):
        uploaded_file = request.files["file"]
        if not uploaded_file.filename:
            return jsonify({"file": "Filename can not be empty!"}), 400

        extension = os.path.splitext(uploaded_file.filename)[1].lower()
        if extension not in [".png", ".jpg", "jpeg"] and extension:
            f = self._convert_and_save(uploaded_file)
        else:
            f = self._file_storage.save_stream(
                uploaded_file.filename, uploaded_file.stream
            )
        logger.info("Saved file %s to %s", uploaded_file.filename, f)
        return jsonify(f), 201

    def _convert_and_save(self, uploaded_file):
        logger.info("Converting image %s to png", uploaded_file.filename)
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp_path = os.path.join(tmpdirname, uploaded_file.filename)
            uploaded_file.save(tmp_path)
            target_path = os.path.splitext(tmp_path)[0] + ".png"

            buf = ImageBuf(tmp_path)
            buf.write(target_path)

            f = self._file_storage.save_file(target_path)

            logger.info("Cleaning up temporary directory %s", tmpdirname)

        return f

    def get_file(self, file_id: int):
        file = self._file_storage.find_by_id(file_id)
        file_path = self._file_storage.get_path(file)
        if file and os.path.exists(file_path):
            return send_file(file_path, attachment_filename=file.name)
        return jsonify({"file_id": "No file found!"}), 404
