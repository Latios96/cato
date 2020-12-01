from flask import Blueprint, jsonify

name = __name__


class ProjectsBlueprint(Blueprint):
    def __init__(self, project_repository):
        super(ProjectsBlueprint, self).__init__("projects", __name__)
        self._project_repository = project_repository
        self.route("/api/v1/projects", methods=["GET"])(self.get_projects)

    def get_projects(self):
        project = self._project_repository.find_all()
        return jsonify(project)
