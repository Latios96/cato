import logging
import os

from fastapi import APIRouter, UploadFile
from fastapi.params import File
from starlette.responses import FileResponse, JSONResponse, Response

from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage

logger = logging.getLogger(__name__)


class FilesBlueprint(APIRouter):
    def __init__(self, file_storage: AbstractFileStorage, object_mapper: ObjectMapper):
        super(FilesBlueprint, self).__init__()
        self._file_storage = file_storage
        self._object_mapper = object_mapper

        self.get("/files/{file_id}")(self.get_file)
        self.post("/files")(self.upload_file)

    def upload_file(self, file: UploadFile = File(...)) -> Response:
        uploaded_file = file
        if not uploaded_file.filename:
            return JSONResponse(
                content={"file": "Filename can not be empty!"}, status_code=400
            )

        f = self._file_storage.save_stream(uploaded_file.filename, uploaded_file.file)
        logger.info("Saved file %s to %s", uploaded_file.filename, f)
        return JSONResponse(content=self._object_mapper.to_dict(f), status_code=201)

    def get_file(self, file_id: int) -> Response:
        file = self._file_storage.find_by_id(file_id)
        file_path = self._file_storage.get_path(file)
        if file and os.path.exists(file_path):
            return FileResponse(path=file_path, filename=file.name)
        return JSONResponse(content={"file_id": "No file found!"}, status_code=404)
