from fastapi import APIRouter
from starlette.responses import JSONResponse

from cato_common.mappers.object_mapper import ObjectMapper
from cato_common.dtos.api_success import ApiSuccess


class ApiTokenBlueprint(APIRouter):
    def __init__(self, object_mapper: ObjectMapper):
        super(ApiTokenBlueprint, self).__init__()
        self._object_mapper = object_mapper

        self.get("/api_tokens/is_valid")(self.is_valid)

    def is_valid(self):
        return JSONResponse(content=self._object_mapper.to_dict(ApiSuccess.ok()))
