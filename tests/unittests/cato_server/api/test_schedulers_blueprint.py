from cato.config.config_file_parser import JsonConfigParser
from cato_common.domain.submission_info import SubmissionInfo
from tests.unittests.cato.test_config_file_parser import VALID_CONFIG


def test_success(client_with_session, run, mocked_scheduler_submitter):
    response = client_with_session.post(
        "/api/v1/schedulers/submit",
        json={
            "config": VALID_CONFIG,  # todo extract to own fixture
            "runId": run.id,
            "resourcePath": "some/path",
            "executable": "some/path",
        },
    )

    assert response.json() == {"success": True}
    assert response.status_code == 200
    expected_info = SubmissionInfo(
        id=1,
        config=JsonConfigParser().parse_dict(VALID_CONFIG),
        run_id=run.id,
        resource_path="some/path",
        executable="some/path",
    )
    mocked_scheduler_submitter.submit_tests.assert_called_with(expected_info)


def test_invalid_run_id_should_return_400(
    client_with_session, mocked_scheduler_submitter
):
    response = client_with_session.post(
        "/api/v1/schedulers/submit",
        json={
            "config": VALID_CONFIG,  # todo extract to own fixture
            "runId": 3,
            "resourcePath": "some/path",
            "executable": "some/path",
        },
    )

    assert response.json() == {"runId": ["No run exists for id 3."]}
    assert response.status_code == 400
    mocked_scheduler_submitter.submit_tests.assert_not_called()
