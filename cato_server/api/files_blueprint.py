from flask import Blueprint, jsonify, request

from cato.storage.abstract.abstract_file_storage import AbstractFileStorage


class FilesBlueprint(Blueprint):
    def __init__(self, file_storage: AbstractFileStorage):
        super(FilesBlueprint, self).__init__("files", __name__)
        self._file_storage = file_storage

        self.route("files", methods=["POST"])(self.upload_file)

    def upload_file(self):
        uploaded_file = request.files["file"]
        if not uploaded_file.filename:
            return jsonify({"file": "Filename can not be empty!"}), 400
        f = self._file_storage.save_stream(uploaded_file.filename, uploaded_file.stream)
        return jsonify(f), 201
