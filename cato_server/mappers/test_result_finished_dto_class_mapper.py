from typing import Type

from cato_server.mappers.abstract_conjure_class_mapper import AbstractConjureClassMapper
from cato_api_models.catoapimodels import TestResultFinishedDto


class TestResultFinishedDtoClassMapper(
    AbstractConjureClassMapper[TestResultFinishedDto]
):
    def _conjure_type(self) -> Type[TestResultFinishedDto]:
        return TestResultFinishedDto
