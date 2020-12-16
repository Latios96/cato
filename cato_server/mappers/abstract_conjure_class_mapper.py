import json

from conjure_python_client import ConjureDecoder, ConjureEncoder
from typing import Dict, Type

from cato_server.mappers.abstract_class_mapper import AbstractClassMapper, T


class AbstractConjureClassMapper(AbstractClassMapper[T]):
    def map_from_dict(self, json_data: Dict) -> T:
        return ConjureDecoder().decode(json_data, self._conjure_type())

    def map_to_dict(self, test_result: T) -> Dict:
        return json.loads(ConjureEncoder().encode(test_result))

    def _conjure_type(self) -> Type[T]:
        raise NotImplementedError()
