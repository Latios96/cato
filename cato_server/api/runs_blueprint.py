import logging
from dateutil.parser import parse
from http.client import BAD_REQUEST

from flask import Blueprint, jsonify, request

from cato.domain.run import Run
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.api.validators.run_validators import CreateRunValidator

logger = logging.getLogger(__name__)


class RunsBlueprint(Blueprint):
    def __init__(
        self, run_repository: RunRepository, project_repository: ProjectRepository
    ):
        super(RunsBlueprint, self).__init__("runs", __name__)
        self._run_repository = run_repository
        self._project_repository = project_repository

        self.route("/runs/project/<project_id>", methods=["GET"])(self.run_by_project)
        self.route("/runs", methods=["POST"])(self.create_run)

    def run_by_project(self, project_id):
        runs = self._run_repository.find_by_project_id(project_id)
        return jsonify(runs)

    def create_run(self):
        request_json = request.get_json()
        errors = CreateRunValidator(self._project_repository).validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

        run = Run(
            id=0,
            project_id=request_json["project_id"],
            started_at=parse(request_json["started_at"]),
        )
        run = self._run_repository.save(run)
        logger.info("Created run %s", run)
        return jsonify(run), 201
