from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.api.authentication.user_from_request import UserFromRequest


class AuthUserBlueprint(APIRouter):
    def __init__(self, user_from_request: UserFromRequest, object_mapper: ObjectMapper):
        super(AuthUserBlueprint, self).__init__()
        self._user_from_request = user_from_request
        self._object_mapper = object_mapper

        self.get("/users/whoami")(self.whoami)

    def whoami(self, request: Request):
        user = self._user_from_request.user_from_request(request)
        if not user:
            return Response(status_code=404)
        return JSONResponse(self._object_mapper.to_dict(user))
