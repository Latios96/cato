import logging
from http.client import BAD_REQUEST

from flask import Blueprint, jsonify, abort, request
from marshmallow import Schema, fields
from marshmallow.validate import Length, Regexp

from cato.domain.project import Project
from cato.storage.abstract.project_repository import ProjectRepository

logger = logging.getLogger(__name__)


class CreateProjectSchema(Schema):
    name = fields.Str(
        required=True, validate=[Length(min=1), Regexp(r"^[A-Za-z0-9_\-]+$")]
    )


class ProjectsBlueprint(Blueprint):
    def __init__(self, project_repository: ProjectRepository):
        super(ProjectsBlueprint, self).__init__("projects", __name__)
        self._project_repository = project_repository

        self.route("/projects", methods=["GET"])(self.get_projects)
        self.route("/projects/<project_id>", methods=["GET"])(self.get_project)
        self.route("/projects/name/<project_name>", methods=["GET"])(
            self.get_project_by_name
        )
        self.route("/projects", methods=["POST"])(self.create_project)

    def get_projects(self):
        projects = self._project_repository.find_all()
        return jsonify(projects)

    def get_project(self, project_id: int):
        project = self._project_repository.find_by_id(project_id)
        if not project:
            abort(404)
        return jsonify(project)

    def create_project(self):
        request_json = request.get_json()
        errors = CreateProjectSchema().validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

        project_name = request_json["name"]

        if self._project_repository.find_by_name(project_name):
            return (
                jsonify(
                    {"name": f'Project with name "{project_name}" already exists!'}
                ),
                BAD_REQUEST,
            )

        project = Project(id=0, name=project_name)
        project = self._project_repository.save(project)
        logger.info("Created project %s", project)
        return jsonify(project), 201

    def get_project_by_name(self, project_name: str):
        project = self._project_repository.find_by_name(project_name)
        if not project:
            abort(404)
        return jsonify(project)
