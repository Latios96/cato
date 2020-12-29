from typing import Type

from cato_server.mappers.abstract_conjure_class_mapper import AbstractConjureClassMapper
from cato_api_models.catoapimodels import FinishTestResultDto


class FinishTestResultDtoClassMapper(AbstractConjureClassMapper[FinishTestResultDto]):
    def _conjure_type(self) -> Type[FinishTestResultDto]:
        return FinishTestResultDto
