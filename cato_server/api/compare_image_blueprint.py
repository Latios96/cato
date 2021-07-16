from fastapi import APIRouter, UploadFile
from fastapi.params import File, Form
from starlette.responses import JSONResponse, Response

from cato_server.domain.comparison_settings import ComparisonSettings
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.usecases.compare_image import CompareImage

import logging

logger = logging.getLogger(__name__)


class CompareImagesBlueprint(APIRouter):
    def __init__(self, compare_image: CompareImage, object_mapper: ObjectMapper):
        super(CompareImagesBlueprint, self).__init__()
        self._compare_image = compare_image
        self._object_mapper = object_mapper

        self.post("/compare_image")(self.do_image_comparison)

    def do_image_comparison(
        self,
        reference_image: UploadFile = File(...),
        output_image: UploadFile = File(...),
        comparison_settings: str = Form(...),
    ) -> Response:
        if not reference_image.filename:
            return JSONResponse(
                content={"reference_image": "Filename can not be empty!"},
                status_code=400,
            )
        if not output_image.filename:
            return JSONResponse(
                content={"output_image": "Filename can not be empty!"}, status_code=400
            )
        try:
            parsed_comparison_settings = self._object_mapper.from_json(
                comparison_settings, ComparisonSettings
            )
        except Exception as e:
            return JSONResponse(
                content={
                    "comparison_settings": "Error when parsing comparison settings: {}".format(
                        e
                    )
                },
                status_code=400,
            )

        try:
            result = self._compare_image.compare_image(
                output_image.file,
                output_image.filename,
                reference_image.file,
                reference_image.filename,
                parsed_comparison_settings,
            )
        except Exception as e:
            logger.error("Error when comparing images")
            logger.error(e, exc_info=True)
            return JSONResponse(
                content={"error": "Error when comparing images: {}".format(e)},
                status_code=400,
            )

        return JSONResponse(
            content=self._object_mapper.to_dict(result), status_code=201
        )
