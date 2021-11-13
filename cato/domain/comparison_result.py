from dataclasses import dataclass
from typing import Optional

from cato_common.domain.test_status import TestStatus


@dataclass
class ComparisonResult:
    status: TestStatus
    message: Optional[str]
    diff_image: Optional[str]
    error: float
