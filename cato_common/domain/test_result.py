import datetime
from dataclasses import dataclass
from typing import Dict, Optional

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.unified_test_status import UnifiedTestStatus


@dataclass
class TestResult:
    id: int
    suite_result_id: int
    test_name: str
    test_identifier: TestIdentifier
    test_command: str
    test_variables: Dict[str, str]
    unified_test_status: UnifiedTestStatus
    machine_info: Optional[MachineInfo] = None
    seconds: Optional[float] = None
    message: Optional[str] = None
    image_output: Optional[int] = None
    reference_image: Optional[int] = None
    diff_image: Optional[int] = None
    started_at: Optional[datetime.datetime] = None
    finished_at: Optional[datetime.datetime] = None
    comparison_settings: Optional[ComparisonSettings] = None
    error_value: Optional[float] = None
    thumbnail_file_id: Optional[int] = None
    failure_reason: Optional[TestFailureReason] = None
    __test__ = False

    def __post_init__(self):
        if self.id is None:
            self.id = 0
