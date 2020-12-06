import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from cato.domain.machine_info import MachineInfo
from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_status import TestStatus
from cato.domain.execution_status import ExecutionStatus


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
    status: Optional[TestStatus] = None
    output: Optional[List[str]] = field(default_factory=list)
    seconds: Optional[float] = None
    message: Optional[str] = None
    image_output: Optional[int] = None
    reference_image: Optional[int] = None
    started_at: Optional[datetime.datetime] = None
    finished_at: Optional[datetime.datetime] = None
    __test__ = False
