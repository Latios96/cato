from dataclasses import dataclass
from typing import Optional

from cato.domain.test_status import TestStatus


@dataclass
class ComparisonResult:
    status: TestStatus
    message: Optional[str]
    diff_image: Optional[str]
