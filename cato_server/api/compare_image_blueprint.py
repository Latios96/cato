from fastapi import APIRouter, UploadFile
from fastapi.params import File, Form
from starlette.responses import JSONResponse, Response

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.task_queue.cato_celery import CatoCelery
from cato_server.task_queue.task_result_factory import TaskResultFactory
from cato_server.usecases.compare_image import CompareImage

import logging

logger = logging.getLogger(__name__)


class CompareImagesBlueprint(APIRouter):
    def __init__(
        self,
        compare_image: CompareImage,
        object_mapper: ObjectMapper,
        file_storage: AbstractFileStorage,
        cato_celery: CatoCelery,
        task_result_factory: TaskResultFactory,
    ):
        super(CompareImagesBlueprint, self).__init__()
        self._compare_image = compare_image
        self._object_mapper = object_mapper
        self._file_storage = file_storage
        self._cato_celery = cato_celery
        self._task_result_factory = task_result_factory

        self.post("/compare_image")(self.do_image_comparison)

    def do_image_comparison(
        self,
        reference_image: UploadFile = File(...),
        output_image: UploadFile = File(...),
        comparison_settings: str = Form(...),
    ) -> Response:
        if not reference_image.filename:
            return JSONResponse(
                content={"referenceImage": "Filename can not be empty!"},
                status_code=400,
            )
        if not output_image.filename:
            return JSONResponse(
                content={"outputImage": "Filename can not be empty!"}, status_code=400
            )
        try:
            parsed_comparison_settings = self._object_mapper.from_json(
                comparison_settings, ComparisonSettings
            )
        except Exception as e:
            return JSONResponse(
                content={
                    "comparisonSettings": "Error when parsing comparison settings: {}".format(
                        e
                    )
                },
                status_code=400,
            )

        try:
            logger.info("Storing original reference_image file in db..")
            reference_image_file = self._file_storage.save_stream(
                reference_image.filename, reference_image.file
            )
            logger.info("Stored reference_image at %s", reference_image_file)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JSONResponse(
                content={"message": "Error when saving reference image"},
                status_code=400,
            )

        try:
            logger.info("Storing original output_image file in db..")
            output_image_file = self._file_storage.save_stream(
                output_image.filename, output_image.file
            )
            logger.info("Stored output_image at %s", output_image_file)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JSONResponse(
                content={"message": "Error when saving output image"},
                status_code=400,
            )

        async_result = self._cato_celery.launch_compare_image_task(
            output_image_file.id, output_image_file.id, parsed_comparison_settings
        )
        task_result = self._task_result_factory.from_async_result(async_result)
        return JSONResponse(
            content=self._object_mapper.to_dict(task_result), status_code=201
        )
