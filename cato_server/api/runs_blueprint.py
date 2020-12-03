import logging

from flask import Blueprint, jsonify

from cato.storage.abstract.run_repository import RunRepository

logger = logging.getLogger(__name__)


class RunsBlueprint(Blueprint):
    def __init__(self, run_repository: RunRepository):
        super(RunsBlueprint, self).__init__("runs", __name__)
        self._run_repository = run_repository

        self.route("/runs/project/<project_id>", methods=["GET"])(self.run_by_project)

    def run_by_project(self, project_id):
        runs = self._run_repository.find_by_project_id(project_id)
        return jsonify(runs)
