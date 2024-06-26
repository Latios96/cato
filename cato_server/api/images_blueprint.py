import logging
import os

from fastapi import APIRouter, UploadFile
from fastapi.params import File
from starlette.responses import JSONResponse, FileResponse, Response

from cato_server.images.store_image import StoreImage
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.task_queue.cato_celery import CatoCelery
from cato_server.task_queue.task_result_factory import TaskResultFactory

logger = logging.getLogger(__name__)


class ImagesBlueprint(APIRouter):
    def __init__(
        self,
        file_storage: AbstractFileStorage,
        image_repository: ImageRepository,
        object_mapper: ObjectMapper,
        store_image: StoreImage,
        cato_celery: CatoCelery,
        task_result_factory: TaskResultFactory,
    ):
        super(ImagesBlueprint, self).__init__()
        self._file_storage = file_storage
        self._image_repository = image_repository
        self._object_mapper = object_mapper
        self._store_image = store_image
        self._cato_celery = cato_celery
        self._task_result_factory = task_result_factory

        self.post("/images")(self.upload_image)
        self.get("/images/original_file/{image_id}")(self.get_original_image_file)
        self.get("/images/{image_id}")(self.get_image)

    def upload_image(self, file: UploadFile = File(...)) -> Response:
        uploaded_file = file
        if not uploaded_file.filename:
            return JSONResponse(
                content={"file": "Filename can not be empty!"}, status_code=400
            )

        try:
            logger.info("Storing original image file in db..")
            original_file = self._file_storage.save_stream(
                uploaded_file.filename, uploaded_file.file
            )
            logger.info("Stored original file at %s", original_file)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JSONResponse(
                content={"message": "Error when saving image"}, status_code=400
            )
        image = self._store_image.store_image_for_transcoding(original_file)
        self._cato_celery.launch_transcode_image_task(image.id)
        return JSONResponse(content=self._object_mapper.to_dict(image), status_code=201)

    def get_original_image_file(self, image_id: int) -> Response:
        image = self._image_repository.find_by_id(image_id)
        if not image:
            return Response(status_code=404)
        file = self._file_storage.find_by_id(image.original_file_id)
        if not file:
            return Response(status_code=404)
        file_path = self._file_storage.get_path(file)
        if file and os.path.exists(file_path):
            return FileResponse(path=file_path, filename=file.name)
        return JSONResponse(content={"file_id": "No file found!"}, status_code=201)

    def get_image(self, image_id) -> Response:
        image = self._image_repository.find_by_id(image_id)
        if not image:
            return Response(status_code=404)
        return JSONResponse(content=self._object_mapper.to_dict(image), status_code=200)
