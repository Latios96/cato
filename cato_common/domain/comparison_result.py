from dataclasses import dataclass
from typing import Optional

from cato_common.domain.result_status import ResultStatus


@dataclass
class ComparisonResult:
    status: ResultStatus
    message: Optional[str]
    diff_image: Optional[str]
    error: float
