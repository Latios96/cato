from typing import Optional

from cato_common.domain.branch_name import BranchName
from cato_common.mappers.abstract_value_mapper import AbstractValueMapper


class BranchNameValueMapper(AbstractValueMapper[BranchName, str]):
    def map_from(self, test_identifier_str: Optional[str]) -> Optional[BranchName]:
        if not test_identifier_str:
            return None
        return BranchName(test_identifier_str)

    def map_to(self, test_identifier: BranchName) -> str:
        return str(test_identifier)
