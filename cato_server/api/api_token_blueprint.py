from fastapi import APIRouter
from starlette.responses import Response


class ApiTokenBlueprint(APIRouter):
    def __init__(self):
        super(ApiTokenBlueprint, self).__init__()

        self.get("/api_tokens/is_valid")(self.is_valid)

    def is_valid(self):
        return Response(status_code=200)
