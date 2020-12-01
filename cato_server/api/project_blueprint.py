import flask
from flask import Blueprint, jsonify

name = __name__


class ProjectsBlueprint(Blueprint):
    def __init__(self, project_repository):
        super(ProjectsBlueprint, self).__init__("projects", __name__)
        self._project_repository = project_repository
        self.route("/api/v1/projects", methods=["GET"])(self.get_projects)
        self.route("/api/v1/projects/<project_id>", methods=["GET"])(self.get_project)

    def get_projects(self):
        projects = self._project_repository.find_all()
        return jsonify(projects)

    def get_project(self, project_id: int):
        project = self._project_repository.find_by_id(project_id)
        if not project:
            flask.abort(404)
        return jsonify(project)
