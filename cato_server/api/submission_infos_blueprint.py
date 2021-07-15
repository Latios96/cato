from fastapi import APIRouter
from starlette.responses import JSONResponse, Response

from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.submission_info_repository import (
    SubmissionInfoRepository,
)


class SubmissionInfosBlueprint(APIRouter):
    def __init__(
        self,
        submission_info_repository: SubmissionInfoRepository,
        object_mapper: ObjectMapper,
    ):
        super(SubmissionInfosBlueprint, self).__init__()
        self._submission_info_repository = submission_info_repository
        self._object_mapper = object_mapper

        self.get("/submission_infos/{submission_info_id}")(
            self.get_submission_info_by_id
        )

    def get_submission_info_by_id(self, submission_info_id: int) -> Response:
        submission_info = self._submission_info_repository.find_by_id(
            submission_info_id
        )
        if not submission_info:
            return Response(status_code=404)
        return JSONResponse(content=self._object_mapper.to_dict(submission_info))
