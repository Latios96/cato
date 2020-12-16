from typing import Type

from cato_api_models.catoapimodels import CreateFullRunDto
from cato_server.mappers.abstract_conjure_class_mapper import AbstractConjureClassMapper


class CreateFullRunDtoClassMapper(AbstractConjureClassMapper[CreateFullRunDto]):
    def _conjure_type(self) -> Type[CreateFullRunDto]:
        return CreateFullRunDto
