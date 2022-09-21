from cato.utils.run_information_detectors.local_run_information_detector import (
    LocalComputerRunInformationDetector,
)
from cato_common.dtos.create_full_run_dto import BasicRunInformationForRunCreation


class RunInformationDetector:
    def __init__(
        self,
        local_computer_run_information_detector: LocalComputerRunInformationDetector,
    ):
        self._local_computer_run_information_detector = (
            local_computer_run_information_detector
        )

    def detect(self) -> BasicRunInformationForRunCreation:
        return self._local_computer_run_information_detector.detect()
