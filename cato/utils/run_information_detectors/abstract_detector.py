import os
import socket
from typing import Mapping

from cato_common.domain.run_information import OS
from cato_common.dtos.create_full_run_dto import BasicRunInformationForRunCreation


class AbstractDetector:
    def __init__(self, environment=os.environ):
        self._environment: Mapping[str, str] = environment

    def can_detect(self) -> bool:
        raise NotImplementedError()

    def detect(self) -> BasicRunInformationForRunCreation:
        return BasicRunInformationForRunCreation(
            os=OS.get_current_os(), computer_name=socket.gethostname()
        )
