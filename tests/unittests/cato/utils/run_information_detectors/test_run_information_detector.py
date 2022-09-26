from cato.utils.run_information_detectors.github_actions_run_information_detector import (
    GithubActionsRunInformationDetector,
)
from cato.utils.run_information_detectors.run_information_detector import (
    RunInformationDetector,
)
from cato.utils.run_information_detectors.local_run_information_detector import (
    LocalComputerRunInformationDetector,
)
from cato_common.domain.run_information import OS
from cato_common.dtos.create_full_run_dto import (
    BasicRunInformationForRunCreation,
    GithubActionsRunInformationForRunCreation,
)
from tests.utils import mock_safe


def test_should_detect_local_run_information():
    mock_local_computer_run_information_detector = mock_safe(
        LocalComputerRunInformationDetector
    )
    mock_github_actions_run_information_detector = mock_safe(
        GithubActionsRunInformationDetector
    )
    mock_github_actions_run_information_detector.can_detect.return_value = False
    mock_local_computer_run_information_detector.detect.return_value = (
        BasicRunInformationForRunCreation(os=OS.WINDOWS, computer_name="cray")
    )
    run_information_detector = RunInformationDetector(
        mock_local_computer_run_information_detector,
        mock_github_actions_run_information_detector,
    )

    run_information = run_information_detector.detect()

    assert run_information == BasicRunInformationForRunCreation(
        os=OS.WINDOWS, computer_name="cray"
    )


def test_should_detect_github_actions_run_information():
    mock_local_computer_run_information_detector = mock_safe(
        LocalComputerRunInformationDetector
    )
    mock_github_actions_run_information_detector = mock_safe(
        GithubActionsRunInformationDetector
    )
    mock_github_actions_run_information_detector.can_detect.return_value = True
    run_information = GithubActionsRunInformationForRunCreation(
        os=OS.WINDOWS,
        computer_name="cray",
        github_run_id=3052454707,
        html_url="https://github.com/owner/repo-name/actions/runs/3052454707/jobs/4921861789",
        job_name="build_ubuntu",
        actor="owner",
        attempt=1,
        run_number=2,
        github_url="https://github.com",
        github_api_url="https://api.github.com",
    )
    mock_github_actions_run_information_detector.detect.return_value = run_information
    run_information_detector = RunInformationDetector(
        mock_local_computer_run_information_detector,
        mock_github_actions_run_information_detector,
    )

    detected_run_information = run_information_detector.detect()

    assert detected_run_information == run_information
