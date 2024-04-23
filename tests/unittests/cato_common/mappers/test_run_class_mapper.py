from cato_common.domain.branch_name import BranchName
from cato_common.domain.run import Run
from cato_common.domain.run_information import OS, LocalComputerRunInformation
from cato_common.utils.datetime_utils import aware_now_in_utc


def test_map_from_dict(object_mapper):
    started_at = aware_now_in_utc()

    result = object_mapper.from_dict(
        {
            "id": 1,
            "projectId": 1,
            "runBatchId": 1,
            "createdAt": started_at.isoformat(),
            "branchName": "default",
            "previousRunId": None,
            "runInformation": {
                "id": 0,
                "runId": 0,
                "os": "WINDOWS",
                "computerName": "cray",
                "localUsername": "username",
                "runInformationType": "LOCAL_COMPUTER",
            },
            "performanceTraceId": None,
        },
        Run,
    )

    assert result == Run(
        id=1,
        project_id=1,
        run_batch_id=1,
        created_at=started_at,
        branch_name=BranchName("default"),
        previous_run_id=None,
        run_information=LocalComputerRunInformation(
            id=0,
            run_id=0,
            os=OS.WINDOWS,
            computer_name="cray",
            local_username="username",
        ),
        performance_trace_id=None,
    )


def test_map_to_dict(object_mapper):
    started_at = aware_now_in_utc()

    result = object_mapper.to_dict(
        Run(
            id=1,
            project_id=1,
            run_batch_id=1,
            created_at=started_at,
            branch_name=BranchName("default"),
            previous_run_id=None,
            run_information=LocalComputerRunInformation(
                id=0,
                run_id=0,
                os=OS.WINDOWS,
                computer_name="cray",
                local_username="username",
            ),
            performance_trace_id=None,
        )
    )

    assert result == {
        "id": 1,
        "projectId": 1,
        "runBatchId": 1,
        "createdAt": started_at.isoformat(),
        "branchName": "default",
        "previousRunId": None,
        "runInformation": {
            "id": 0,
            "runId": 0,
            "os": "WINDOWS",
            "computerName": "cray",
            "localUsername": "username",
            "runInformationType": "LOCAL_COMPUTER",
        },
        "performanceTraceId": None,
    }
