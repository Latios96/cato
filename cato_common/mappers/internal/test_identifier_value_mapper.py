from typing import Optional

from cato_common.domain.test_identifier import TestIdentifier
from cato_common.mappers.abstract_value_mapper import AbstractValueMapper


class TestIdentifierValueMapper(AbstractValueMapper[TestIdentifier, str]):
    def map_from(self, test_identifier_str: Optional[str]) -> Optional[TestIdentifier]:
        if not test_identifier_str:
            return None
        return TestIdentifier.from_string(test_identifier_str)

    def map_to(self, test_identifier: TestIdentifier) -> str:
        return str(test_identifier)
