import datetime

import pytest

from cato_common.domain.branch_name import BranchName
from cato_common.dtos.run_aggregate import RunProgress
from cato_common.dtos.run_batch_aggregate import RunBatchAggregate
from cato_server.domain.run_batch import RunBatch
from cato_server.domain.run_status import RunStatus
from cato_server.run_status_calculator import RunStatusCalculator
from cato_server.usecases.aggregate_run import AggregateRun
from cato_server.usecases.aggregate_run_batch import AggregateRunBatch
from tests.utils import mock_safe


@pytest.fixture
def test_context():
    class TestContext:
        def __init__(self):
            self.mock_aggregate_run = mock_safe(AggregateRun)
            self.mock_run_status_calculator = mock_safe(RunStatusCalculator)
            self.aggregate_run_batch = AggregateRunBatch(
                self.mock_aggregate_run, self.mock_run_status_calculator
            )

    return TestContext()


def test_aggregate_run_batch(
    test_context,
    run_batch_identifier,
    local_computer_run_information,
    run_factory,
    run_aggregate_factory,
):
    run_1_aggregate = run_aggregate_factory(
        id=1, duration=1, status=RunStatus.SUCCESS, suite_count=1, test_count=10
    )
    run_2_aggregate = run_aggregate_factory(
        id=2, duration=2, status=RunStatus.FAILED, suite_count=2, test_count=10
    )
    test_context.mock_aggregate_run.aggregate_runs_by_project_id.return_value = [
        run_1_aggregate,
        run_2_aggregate,
    ]
    test_context.mock_run_status_calculator.calculate.return_value = RunStatus.FAILED
    run_batch_runs = [
        run_factory(
            id=1,
            run_batch_id=1,
            started_at=datetime.datetime(year=2022, month=9, day=30),
        ),
        run_factory(
            id=2,
            run_batch_id=1,
            started_at=datetime.datetime(year=2022, month=9, day=30),
        ),
    ]
    run_batches = [
        RunBatch(
            id=1,
            run_batch_identifier=run_batch_identifier,
            project_id=1,
            created_at=datetime.datetime(year=2022, month=9, day=30),
            runs=run_batch_runs,
        )
    ]

    aggregated_run_batches = (
        test_context.aggregate_run_batch.aggregate_run_batches_by_project_id(
            1, run_batches
        )
    )

    assert aggregated_run_batches == [
        RunBatchAggregate(
            id=1,
            run_batch_identifier=run_batch_identifier,
            project_id=1,
            created_at=datetime.datetime(year=2022, month=9, day=30),
            runs=[run_1_aggregate, run_2_aggregate],
            status=RunStatus.FAILED,
            duration=3,
            branch_name=BranchName("main"),
            suite_count=3,
            test_count=20,
            progress=RunProgress(
                waiting_test_count=2,
                running_test_count=4,
                failed_test_count=6,
                succeeded_test_count=8,
                progress_percentage=0.9,
            ),
        )
    ]
    test_context.mock_aggregate_run.aggregate_runs_by_project_id.assert_called_with(
        1, run_batch_runs
    )
    test_context.mock_run_status_calculator.calculate.assert_called_with(
        {RunStatus.SUCCESS, RunStatus.FAILED}
    )


def test_aggregate_multiple_run_batches_should_have_correct_runs(
    test_context, run_batch_identifier, run_factory, run_aggregate_factory
):
    run_1_aggregate = run_aggregate_factory(
        id=1, duration=1, status=RunStatus.SUCCESS, suite_count=1, test_count=10
    )
    run_2_aggregate = run_aggregate_factory(
        id=2, duration=2, status=RunStatus.FAILED, suite_count=2, test_count=10
    )
    run_3_aggregate = run_aggregate_factory(
        id=3, duration=1, status=RunStatus.SUCCESS, suite_count=1, test_count=10
    )
    run_4_aggregate = run_aggregate_factory(
        id=4, duration=2, status=RunStatus.FAILED, suite_count=2, test_count=10
    )
    test_context.mock_aggregate_run.aggregate_runs_by_project_id.return_value = [
        run_1_aggregate,
        run_2_aggregate,
        run_3_aggregate,
        run_4_aggregate,
    ]
    test_context.mock_run_status_calculator.calculate.return_value = RunStatus.FAILED
    run_batch_1_runs = [
        run_factory(
            id=1,
            run_batch_id=1,
            started_at=datetime.datetime(year=2022, month=9, day=30),
        ),
        run_factory(
            id=2,
            run_batch_id=1,
            started_at=datetime.datetime(year=2022, month=9, day=30),
        ),
    ]
    run_batch_2_runs = [
        run_factory(
            id=3,
            run_batch_id=1,
            started_at=datetime.datetime(year=2022, month=9, day=30),
        ),
        run_factory(
            id=4,
            run_batch_id=1,
            started_at=datetime.datetime(year=2022, month=9, day=30),
        ),
    ]
    run_batches = [
        RunBatch(
            id=1,
            run_batch_identifier=run_batch_identifier,
            project_id=1,
            created_at=datetime.datetime(year=2022, month=9, day=30),
            runs=run_batch_1_runs,
        ),
        RunBatch(
            id=2,
            run_batch_identifier=run_batch_identifier,
            project_id=1,
            created_at=datetime.datetime(year=2022, month=9, day=30),
            runs=run_batch_2_runs,
        ),
    ]

    aggregated_run_batches = (
        test_context.aggregate_run_batch.aggregate_run_batches_by_project_id(
            1, run_batches
        )
    )
    run_ids = list(
        map(lambda batch: [x.id for x in batch.runs], aggregated_run_batches)
    )

    assert run_ids == [[1, 2], [3, 4]]
