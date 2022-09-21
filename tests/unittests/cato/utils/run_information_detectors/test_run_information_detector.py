from cato.utils.run_information_detectors.run_information_detector import (
    RunInformationDetector,
)
from cato.utils.run_information_detectors.local_run_information_detector import (
    LocalComputerRunInformationDetector,
)
from cato_common.domain.run_information import OS
from cato_common.dtos.create_full_run_dto import BasicRunInformationForRunCreation
from tests.utils import mock_safe


def test_should_detect_local_run_information():
    mock_local_computer_run_information_detector = mock_safe(
        LocalComputerRunInformationDetector
    )
    mock_local_computer_run_information_detector.detect.return_value = (
        BasicRunInformationForRunCreation(os=OS.WINDOWS, computer_name="cray")
    )
    run_information_detector = RunInformationDetector(
        mock_local_computer_run_information_detector
    )

    run_information = run_information_detector.detect()

    assert run_information == BasicRunInformationForRunCreation(
        os=OS.WINDOWS, computer_name="cray"
    )
