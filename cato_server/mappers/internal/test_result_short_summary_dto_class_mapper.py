from typing import Type

from cato_server.mappers.abstract_conjure_class_mapper import AbstractConjureClassMapper
from cato_api_models.catoapimodels import TestResultShortSummaryDto


class TestResultShortSummaryDtoClassMapper(
    AbstractConjureClassMapper[TestResultShortSummaryDto]
):
    def _conjure_type(self) -> Type[TestResultShortSummaryDto]:
        return TestResultShortSummaryDto
