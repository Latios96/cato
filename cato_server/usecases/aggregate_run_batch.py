from itertools import chain
from typing import List

from cato_common.dtos.run_aggregate import RunProgress
from cato_common.dtos.run_batch_aggregate import RunBatchAggregate
from cato_server.domain.run_batch import RunBatch
from cato_server.run_status_calculator import RunStatusCalculator
from cato_server.usecases.aggregate_run import AggregateRun


class AggregateRunBatch:
    def __init__(
        self,
        aggregate_run: AggregateRun,
        run_status_calculator: RunStatusCalculator,
    ):
        self._aggregate_run = aggregate_run
        self._run_status_calculator = run_status_calculator

    def aggregate_run_batches_by_project_id(
        self, project_id: int, run_batches: List[RunBatch]
    ) -> List[RunBatchAggregate]:
        runs = list(chain(*[run_batch.runs for run_batch in run_batches]))
        run_aggregates = self._aggregate_run.aggregate_runs_by_project_id(
            project_id, runs
        )

        run_batch_aggregates = []
        for run_batch in run_batches:
            runs = run_aggregates[0 : len(run_batch.runs)]
            run_batch_aggregate = self._aggregate_run_batch(run_batch, runs)
            run_batch_aggregates.append(run_batch_aggregate)

        return run_batch_aggregates

    def _aggregate_run_batch(self, run_batch, runs):
        status = self._run_status_calculator.calculate({x.status for x in runs})
        duration = sum(map(lambda x: x.duration, runs))
        suite_count = sum(map(lambda x: x.suite_count, runs))
        test_count = sum(map(lambda x: x.test_count, runs))
        run_progressions = list(map(lambda x: x.progress, runs))
        progress = self._aggregate_progress(test_count, run_progressions)

        return RunBatchAggregate(
            id=run_batch.id,
            run_batch_identifier=run_batch.run_batch_identifier,
            project_id=run_batch.project_id,
            created_at=run_batch.created_at,
            runs=runs,
            status=status,
            duration=duration,
            branch_name=runs[0].branch_name,
            suite_count=suite_count,
            test_count=test_count,
            progress=progress,
        )

    def _aggregate_progress(
        self,
        test_count: int,
        run_progressions: List[RunProgress],
    ):
        waiting = sum(map(lambda x: x.waiting_test_count, run_progressions))
        running = sum(map(lambda x: x.running_test_count, run_progressions))
        failed = sum(map(lambda x: x.failed_test_count, run_progressions))
        success = sum(map(lambda x: x.succeeded_test_count, run_progressions))

        executed_tests = running + failed + success

        progress = 0
        if test_count:
            progress = float(executed_tests) / float(test_count)

        return RunProgress(
            waiting_test_count=waiting,
            running_test_count=running,
            failed_test_count=failed,
            succeeded_test_count=success,
            progress_percentage=progress,
        )
