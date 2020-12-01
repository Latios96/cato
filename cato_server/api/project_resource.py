from flask import Blueprint, jsonify

from cato.storage.abstract.project_repository import ProjectRepository

name = __name__

class ProjectBluePrint(Blueprint):

    def __init__(self, project_repository: ProjectRepository):
        super(ProjectBluePrint, self).__init__('pro', name)
        self._project_repository = project_repository
        self.register_routes()

    def register_routes(self):
        self.route("/api/v1/blueprint/projects", methods=["GET"])(self.get_projects)

    def get_projects(self):
        return jsonify(self._project_repository.find_all())

