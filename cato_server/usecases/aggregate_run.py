from typing import List

from cato_common.domain.run import Run
from cato_common.dtos.run_aggregate import RunAggregate, RunProgress
from cato_server.domain.test_result_status_information import (
    TestResultStatusInformation,
)
from cato_server.run_status_calculator import RunStatusCalculator
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository


class AggregateRun:
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        suite_result_repository: SuiteResultRepository,
        run_status_calculator: RunStatusCalculator,
    ):
        self._test_result_repository = test_result_repository
        self._suite_result_repository = suite_result_repository
        self._run_status_calculator = run_status_calculator

    def aggregate_runs_by_project_id(
        self, project_id: int, runs: List[Run]
    ) -> List[RunAggregate]:
        status_by_run_id = self._test_result_repository.find_status_by_project_id(
            project_id
        )
        run_ids = {run.id for run in runs}
        duration_by_run_id = self._test_result_repository.duration_by_run_ids(run_ids)
        suite_count_by_run_id = self._suite_result_repository.suite_count_by_run_ids(
            run_ids
        )
        test_count_by_run_id = self._test_result_repository.test_count_by_run_ids(
            run_ids
        )
        test_result_status_information_by_run_id = (
            self._test_result_repository.status_information_by_run_ids(run_ids)
        )

        aggregates = []
        for run in runs:
            status = self._run_status_calculator.calculate(
                status_by_run_id.get(run.id, set())
            )
            test_result_status_information = test_result_status_information_by_run_id[
                run.id
            ]
            aggregates.append(
                RunAggregate(
                    id=run.id,
                    project_id=run.id,
                    started_at=run.started_at,
                    status=status,
                    duration=duration_by_run_id[run.id],
                    branch_name=run.branch_name,
                    run_information=run.run_information,
                    suite_count=suite_count_by_run_id[run.id],
                    test_count=test_count_by_run_id[run.id],
                    progress=self._aggregate_progress(
                        test_count_by_run_id[run.id], test_result_status_information
                    ),
                )
            )

        return aggregates

    def _aggregate_progress(
        self,
        test_count: int,
        test_result_status_information: TestResultStatusInformation,
    ) -> RunProgress:
        progress = self._calculate_progress(test_count, test_result_status_information)
        return RunProgress(
            waiting_test_count=test_result_status_information.not_started,
            running_test_count=test_result_status_information.running,
            failed_test_count=test_result_status_information.failed,
            succeeded_test_count=test_result_status_information.success,
            progress_percentage=progress,
        )

    def _calculate_progress(
        self,
        test_count: int,
        test_result_status_information: TestResultStatusInformation,
    ):
        executed_tests = (
            test_result_status_information.running
            + test_result_status_information.failed
            + test_result_status_information.success
        )
        if not test_count:
            return 0
        return float(executed_tests) / float(test_count) * 100
