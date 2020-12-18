from typing import Type

from cato_server.mappers.abstract_conjure_class_mapper import AbstractConjureClassMapper
from cato_api_models.catoapimodels import RunSummaryDto


class RunSummaryDtoClassMapper(AbstractConjureClassMapper[RunSummaryDto]):
    def _conjure_type(self) -> Type[RunSummaryDto]:
        return RunSummaryDto
