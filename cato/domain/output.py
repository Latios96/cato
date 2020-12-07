from dataclasses import dataclass


@dataclass
class Output:
    id: int
    test_result_id: int
    text: str
