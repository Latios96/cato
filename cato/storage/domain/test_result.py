import datetime
from dataclasses import dataclass, field
from typing import Dict, List

from cato.domain.machine_info import MachineInfo
from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_result import TestStatus
from cato.storage.domain.execution_status import ExecutionStatus


@dataclass
class TestResult:
    id: int
    suite_result_id: int
    test_name: str
    test_identifier: TestIdentifier
    test_command: str
    test_variables: Dict[str, str]
    machine_info: MachineInfo
    execution_status: ExecutionStatus = ExecutionStatus.NOT_STARTED
    status: TestStatus = None
    output: List[str] = field(default_factory=list)
    seconds: float = 0
    message: str = ""
    image_output: int = ""
    reference_image: int = ""
    started_at: datetime.datetime = None
    finished_at: datetime.datetime = None
