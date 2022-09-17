from typing import Optional

from cato_common.domain.run_identifier import RunIdentifier
from cato_common.mappers.abstract_value_mapper import AbstractValueMapper


class RunIdentifierValueMapper(AbstractValueMapper[RunIdentifier, str]):
    def map_from(self, run_identifier: Optional[str]) -> Optional[RunIdentifier]:
        if not run_identifier:
            return None
        return RunIdentifier(run_identifier)

    def map_to(self, run_identifier: RunIdentifier) -> str:
        return str(run_identifier)
