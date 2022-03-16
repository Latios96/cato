from dataclasses import dataclass
from typing import Optional

from cato_common.domain.unified_test_status import UnifiedTestStatus


@dataclass
class TestResultShortSummaryDto:
    __test__ = False
    id: int
    name: str
    test_identifier: str  # todo we can use TestIdentifier type here, this will be handled by object mapper
    unified_test_status: UnifiedTestStatus
    thumbnail_file_id: Optional[int]
