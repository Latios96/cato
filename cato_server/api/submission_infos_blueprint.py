from flask import Blueprint, abort

from cato_server.api.base_blueprint import BaseBlueprint
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.submission_info_repository import (
    SubmissionInfoRepository,
)


class SubmissionInfosBlueprint(BaseBlueprint):
    def __init__(
        self,
        submission_info_repository: SubmissionInfoRepository,
        object_mapper: ObjectMapper,
    ):
        super(SubmissionInfosBlueprint, self).__init__("submission_infos", __name__)
        self._submission_info_repository = submission_info_repository
        self._object_mapper = object_mapper

        self.route("/submission_infos/<int:submission_info_id>", methods=["GET"])(
            self.get_submission_info_by_id
        )

    def get_submission_info_by_id(self, submission_info_id):
        submission_info = self._submission_info_repository.find_by_id(
            submission_info_id
        )
        if not submission_info:
            abort(404)
        return self.json_response(self._object_mapper.to_json(submission_info))
