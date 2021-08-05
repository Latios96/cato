from typing import Dict, TypeVar, Generic, List

T = TypeVar("T")


class AbstractClassMapper(Generic[T]):
    def map_from_dict(self, json_data: Dict) -> T:
        raise NotImplementedError()

    def map_to_dict(self, test_result: T) -> Dict:
        raise NotImplementedError()

    def map_many_from_dict(self, json_data: List[Dict]) -> List[T]:
        return list(map(self.map_from_dict, json_data))

    def map_many_to_dict(self, test_result: List[T]) -> List[Dict]:
        return list(map(self.map_to_dict, test_result))
