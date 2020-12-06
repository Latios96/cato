from typing import Dict, TypeVar, Generic

T = TypeVar("T")


class AbstractClassMapper(Generic[T]):
    def map_from_dict(self, json_data: Dict) -> T:
        raise NotImplementedError()

    def map_to_dict(self, test_result: T) -> Dict:
        raise NotImplementedError()
