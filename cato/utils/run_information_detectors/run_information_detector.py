from cato.utils.run_information_detectors.github_actions_run_information_detector import (
    GithubActionsRunInformationDetector,
)
from cato.utils.run_information_detectors.local_run_information_detector import (
    LocalComputerRunInformationDetector,
)
from cato_common.dtos.create_full_run_dto import BasicRunInformationForRunCreation


class RunInformationDetector:
    def __init__(
        self,
        local_computer_run_information_detector: LocalComputerRunInformationDetector,
        github_actions_run_information_detector: GithubActionsRunInformationDetector,
    ):
        self._local_computer_run_information_detector = (
            local_computer_run_information_detector
        )
        self._github_actions_run_information_detector = (
            github_actions_run_information_detector
        )

    def detect(self) -> BasicRunInformationForRunCreation:
        if self._github_actions_run_information_detector.can_detect():
            return self._github_actions_run_information_detector.detect()
        return self._local_computer_run_information_detector.detect()
