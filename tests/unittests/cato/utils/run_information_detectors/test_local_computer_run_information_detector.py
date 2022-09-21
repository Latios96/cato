from unittest import mock

from cato.utils.run_information_detectors.local_run_information_detector import (
    LocalComputerRunInformationDetector,
)
from cato_common.domain.run_information import OS
from cato_common.dtos.create_full_run_dto import (
    LocalComputerRunInformationForRunCreation,
)


@mock.patch("cato_common.domain.run_information.OS.get_current_os")
@mock.patch("socket.gethostname")
@mock.patch("getpass.getuser")
def test_should_detect_local_run_information(
    mock_getuser, mock_gethostname, mock_get_current_os
):
    mock_get_current_os.return_value = OS.WINDOWS
    mock_gethostname.return_value = "cray"
    mock_getuser.return_value = "username"
    detector = LocalComputerRunInformationDetector()

    run_information = detector.detect()

    assert run_information == LocalComputerRunInformationForRunCreation(
        os=OS.WINDOWS, computer_name="cray", local_username="username"
    )
