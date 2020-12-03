import logging

from flask import Blueprint, jsonify

from cato.storage.abstract.suite_result_repository import SuiteResultRepository

logger = logging.getLogger(__name__)


class SuiteResultsBlueprint(Blueprint):
    def __init__(self, suite_result_repository: SuiteResultRepository):
        super(SuiteResultsBlueprint, self).__init__("suite-results", __name__)
        self._suite_result_repository = suite_result_repository

        self.route("/suite_results/run/<run_id>", methods=["GET"])(
            self.suite_result_by_run
        )

    def suite_result_by_run(self, run_id):
        suite_results = self._suite_result_repository.find_by_run_id(run_id)
        return jsonify(suite_results)
