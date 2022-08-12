from cato_common.domain.branch_name import BranchName
from cato_common.domain.run import Run
from cato_common.utils.datetime_utils import aware_now_in_utc


def test_map_from_dict(object_mapper):
    started_at = aware_now_in_utc()

    result = object_mapper.from_dict(
        {
            "id": 1,
            "projectId": 1,
            "startedAt": started_at.isoformat(),
            "branchName": "default",
            "previousRunId": None,
        },
        Run,
    )

    assert result == Run(
        id=1,
        project_id=1,
        started_at=started_at,
        branch_name=BranchName("default"),
        previous_run_id=None,
    )


def test_map_to_dict(object_mapper):
    started_at = aware_now_in_utc()

    result = object_mapper.to_dict(
        Run(
            id=1,
            project_id=1,
            started_at=started_at,
            branch_name=BranchName("default"),
            previous_run_id=None,
        )
    )

    assert result == {
        "id": 1,
        "projectId": 1,
        "startedAt": started_at.isoformat(),
        "branchName": "default",
        "previousRunId": None,
    }
