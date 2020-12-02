import os

from flask import Blueprint, jsonify, request, send_file

from cato.storage.abstract.abstract_file_storage import AbstractFileStorage


class FilesBlueprint(Blueprint):
    def __init__(self, file_storage: AbstractFileStorage):
        super(FilesBlueprint, self).__init__("files", __name__)
        self._file_storage = file_storage

        self.route("/files/<int:file_id>", methods=["GET"])(self.get_file)
        # self.route("/files/<int:file_id>/web-representation", methods=["GET"])(self.get_web_representation)
        self.route("files", methods=["POST"])(self.upload_file)

    def upload_file(self):
        uploaded_file = request.files["file"]
        if not uploaded_file.filename:
            return jsonify({"file": "Filename can not be empty!"}), 400
        f = self._file_storage.save_stream(uploaded_file.filename, uploaded_file.stream)
        return jsonify(f), 201

    def get_file(self, file_id: int):
        file = self._file_storage.find_by_id(file_id)
        file_path = self._file_storage.get_path(file)
        if file and os.path.exists(file_path):
            return send_file(file_path, attachment_filename=file.name)
        return jsonify({"file_id": "No file found!"}), 404
