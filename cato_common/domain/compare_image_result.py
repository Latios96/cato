from dataclasses import dataclass
from typing import Optional

from cato_common.domain.test_status import TestStatus


@dataclass
class CompareImageResult:
    status: TestStatus
    message: Optional[str]
    reference_image_id: int
    output_image_id: int
    diff_image_id: int
    error: float
