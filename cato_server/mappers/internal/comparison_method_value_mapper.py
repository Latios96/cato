from typing import Optional

from cato.domain.test_status import TestStatus
from cato_server.domain.comparison_method import ComparisonMethod
from cato_server.mappers.abstract_value_mapper import AbstractValueMapper


class ComparisonMethodValueMapper(AbstractValueMapper[ComparisonMethod, str]):
    def map_from(self, method: Optional[str]) -> Optional[ComparisonMethod]:
        if not method:
            return None
        values = {"SSIM": ComparisonMethod.SSIM}
        return values[method]

    def map_to(self, method: ComparisonMethod) -> str:
        return method.name
