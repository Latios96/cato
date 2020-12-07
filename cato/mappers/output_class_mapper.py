from typing import Dict

from cato.domain.output import Output
from cato.mappers.abstract_class_mapper import AbstractClassMapper


class OutputClassMapper(AbstractClassMapper[Output]):
    def map_from_dict(self, the_dict: Dict) -> Output:
        return Output(
            id=the_dict.get("id") or 0,
            test_result_id=the_dict["test_result_id"],
            text=the_dict["text"],
        )

    def map_to_dict(self, output: Output) -> Dict:
        return {
            "id": output.id,
            "test_result_id": output.test_result_id,
            "text": output.text,
        }
