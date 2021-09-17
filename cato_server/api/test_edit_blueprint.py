from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.test_edit_repository import TestEditRepository


class TestEditBlueprint(APIRouter):
    def __init__(
        self, test_edit_repository: TestEditRepository, object_mapper: ObjectMapper
    ):
        super(TestEditBlueprint, self).__init__()
        self._test_edit_repository = test_edit_repository
        self._object_mapper = object_mapper

        self.get("/test_edits/{test_result_id}")(self.test_edits_by_test_result_id)
        self.get("/test_edits/runs/{run_id}")(self.test_edits_by_run_id)

    def test_edits_by_test_result_id(
        self, test_result_id: int, request: Request
    ) -> Response:
        edits = self._test_edit_repository.find_by_test_id(test_result_id)

        return JSONResponse(content=self._object_mapper.many_to_dict(edits))

    def test_edits_by_run_id(self, run_id: int, request: Request) -> Response:
        edits = self._test_edit_repository.find_by_run_id(run_id)

        return JSONResponse(content=self._object_mapper.many_to_dict(edits))
