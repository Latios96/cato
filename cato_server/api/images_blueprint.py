import logging
import os
import shutil
import tempfile

from fastapi import APIRouter, UploadFile
from fastapi.params import File
from starlette.responses import JSONResponse, FileResponse, Response

from cato_server.images.store_image import StoreImage
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository

logger = logging.getLogger(__name__)


class ImagesBlueprint(APIRouter):
    def __init__(
        self,
        file_storage: AbstractFileStorage,
        image_repository: ImageRepository,
        object_mapper: ObjectMapper,
        store_image: StoreImage,
    ):
        super(ImagesBlueprint, self).__init__()
        self._file_storage = file_storage
        self._image_repository = image_repository
        self._object_mapper = object_mapper
        self._store_image = store_image

        self.post("/images")(self.upload_file)
        self.get("/images/original_file/{file_id}")(self.get_original_image_file)
        self.get("/images/{image_id}")(self.get_image)

    def upload_file(self, file: UploadFile = File(...)) -> Response:
        uploaded_file = file
        if not uploaded_file.filename:
            return JSONResponse(
                content={"file": "Filename can not be empty!"}, status_code=400
            )

        try:
            with tempfile.TemporaryDirectory() as tmpdirname:
                tmp_path = os.path.join(tmpdirname, uploaded_file.filename)
                with open(tmp_path, "wb") as tmp:
                    shutil.copyfileobj(uploaded_file.file, tmp)
                image = self._store_image.store_image(tmp_path)

                logger.info("Deleting tmpdir %s", tmpdirname)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JSONResponse(
                content={"message": "Error when saving image"}, status_code=400
            )

        return JSONResponse(content=self._object_mapper.to_dict(image), status_code=201)

    def get_original_image_file(self, file_id: int) -> Response:
        image = self._image_repository.find_by_id(file_id)
        file = self._file_storage.find_by_id(image.original_file_id)
        file_path = self._file_storage.get_path(file)
        if file and os.path.exists(file_path):
            return FileResponse(path=file_path, filename=file.name)
        return JSONResponse(content={"file_id": "No file found!"}, status_code=201)

    def get_image(self, image_id) -> Response:
        image = self._image_repository.find_by_id(image_id)
        if not image:
            return Response(status_code=404)
        return JSONResponse(content=self._object_mapper.to_dict(image), status_code=200)
