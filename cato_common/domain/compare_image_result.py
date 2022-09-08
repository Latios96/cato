from dataclasses import dataclass
from typing import Optional

from cato_common.domain.result_status import ResultStatus


@dataclass
class CompareImageResult:
    status: ResultStatus
    message: Optional[str]
    reference_image_id: int
    output_image_id: int
    diff_image_id: Optional[int]
    error: float
