from http.client import BAD_REQUEST

from flask import Blueprint, jsonify, abort, request
from marshmallow import Schema, fields

from cato.domain.project import Project
from cato.storage.abstract.project_repository import ProjectRepository

name = __name__


class CreateProjectSchema(Schema):
    name = fields.Str(required=True)


class ProjectsBlueprint(Blueprint):
    def __init__(self, project_repository: ProjectRepository):
        super(ProjectsBlueprint, self).__init__("projects", __name__)
        self._project_repository = project_repository

        self.route("/api/v1/projects", methods=["GET"])(self.get_projects)
        self.route("/api/v1/projects/<project_id>", methods=["GET"])(self.get_project)
        self.route("/api/v1/projects", methods=["POST"])(self.create_project)

    def get_projects(self):
        projects = self._project_repository.find_all()
        return jsonify(projects)

    def get_project(self, project_id: int):
        project = self._project_repository.find_by_id(project_id)
        if not project:
            abort(404)
        return jsonify(project)

    def create_project(self):
        errors = CreateProjectSchema().validate(request.form)
        if errors:
            return jsonify(errors), BAD_REQUEST

        project = Project(id=0, name=request.form["name"])
        return jsonify(self._project_repository.save(project))
