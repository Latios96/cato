from typing import Optional

from cato_common.domain.run_name import RunName
from cato_common.mappers.abstract_value_mapper import AbstractValueMapper


class RunNameValueMapper(AbstractValueMapper[RunName, str]):
    def map_from(self, run_name: Optional[str]) -> Optional[RunName]:
        if not run_name:
            return None
        return RunName(run_name)

    def map_to(self, run_name: RunName) -> str:
        return str(run_name)
