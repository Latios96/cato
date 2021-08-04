import datetime
from dataclasses import dataclass
from typing import Dict, Optional

from cato_server.domain.execution_status import ExecutionStatus
from cato_server.domain.machine_info import MachineInfo
from cato_server.domain.test_identifier import TestIdentifier
from cato.domain.test_status import TestStatus


@dataclass
class TestResult:
    id: int
    suite_result_id: int
    test_name: str
    test_identifier: TestIdentifier
    test_command: str
    test_variables: Dict[str, str]
    machine_info: Optional[MachineInfo] = None
    execution_status: ExecutionStatus = ExecutionStatus.NOT_STARTED
    status: Optional[TestStatus] = None
    seconds: Optional[float] = None
    message: Optional[str] = None
    image_output: Optional[int] = None
    reference_image: Optional[int] = None
    diff_image: Optional[int] = None
    started_at: Optional[datetime.datetime] = None
    finished_at: Optional[datetime.datetime] = None
    __test__ = False

    def __post_init__(self):
        if self.id is None:
            self.id = 0
