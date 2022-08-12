from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.image import Image
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.unified_test_status import UnifiedTestStatus


@dataclass
class TestResultDto:
    id: int
    suite_result_id: int
    test_name: str
    test_identifier: TestIdentifier
    test_command: str
    test_variables: Dict[str, str]
    machine_info: MachineInfo
    unified_test_status: UnifiedTestStatus
    seconds: float
    message: Optional[str]
    image_output: Optional[Image]
    reference_image: Optional[Image]
    diff_image: Optional[Image]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    comparison_settings: Optional[ComparisonSettings]
    error_value: Optional[float]
    thumbnail_file_id: Optional[int]
