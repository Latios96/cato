from typing import Type

from cato_server.mappers.abstract_conjure_class_mapper import AbstractConjureClassMapper
from cato_api_models.catoapimodels import RunDto


class RunDtoClassMapper(AbstractConjureClassMapper[RunDto]):
    def _conjure_type(self) -> Type[RunDto]:
        return RunDto
