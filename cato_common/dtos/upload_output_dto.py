from dataclasses import dataclass


@dataclass
class UploadOutputDto:
    test_result_id: int
    text: str
