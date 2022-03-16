from dataclasses import dataclass
from typing import Optional

from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.unified_test_status import UnifiedTestStatus


@dataclass
class FinishTestResultDto:
    id: int
    status: UnifiedTestStatus
    seconds: float
    message: str
    image_output: Optional[int]
    reference_image: Optional[int]
    diff_image: Optional[int]
    error_value: Optional[float]
    failure_reason: Optional[TestFailureReason]
