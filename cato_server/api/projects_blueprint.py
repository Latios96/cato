import logging
from http.client import BAD_REQUEST

from flask import Blueprint, jsonify, abort, request

from cato_server.api.base_blueprint import BaseBlueprint
from cato_server.domain.project import Project
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.api.validators.project_validators import CreateProjectValidator

logger = logging.getLogger(__name__)


class ProjectsBlueprint(BaseBlueprint):
    def __init__(
        self, project_repository: ProjectRepository, object_mapper: ObjectMapper
    ):
        super(ProjectsBlueprint, self).__init__("projects", __name__)
        self._project_repository = project_repository
        self._object_mapper = object_mapper

        self.route("/projects", methods=["GET"])(self.get_projects)
        self.route("/projects/<project_id>", methods=["GET"])(self.get_project)
        self.route("/projects/name/<project_name>", methods=["GET"])(
            self.get_project_by_name
        )
        self.route("/projects", methods=["POST"])(self.create_project)

    def get_projects(self):
        projects = self._project_repository.find_all()
        return self.json_response(self._object_mapper.many_to_json(projects))

    def get_project(self, project_id: int):
        project = self._project_repository.find_by_id(project_id)
        if not project:
            abort(404)
        return self.json_response(self._object_mapper.to_json(project))

    def create_project(self):
        request_json = request.get_json()
        errors = CreateProjectValidator(self._project_repository).validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

        project_name = request_json["name"]

        project = Project(id=0, name=project_name)
        project = self._project_repository.save(project)
        logger.info("Created project %s", project)
        return self.json_response(self._object_mapper.to_json(project)), 201

    def get_project_by_name(self, project_name: str):
        project = self._project_repository.find_by_name(project_name)
        if not project:
            abort(404)
        return self.json_response(self._object_mapper.to_json(project))
