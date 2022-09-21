import getpass

from cato.utils.run_information_detectors.abstract_detector import AbstractDetector
from cato_common.dtos.create_full_run_dto import (
    BasicRunInformationForRunCreation,
    LocalComputerRunInformationForRunCreation,
)


class LocalComputerRunInformationDetector(AbstractDetector):
    def can_detect(self) -> bool:
        return True

    def detect(self) -> BasicRunInformationForRunCreation:
        basic_run = super(LocalComputerRunInformationDetector, self).detect()
        return LocalComputerRunInformationForRunCreation.from_basic_run(
            basic_run, local_username=getpass.getuser()
        )
