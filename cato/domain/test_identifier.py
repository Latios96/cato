from dataclasses import dataclass


@dataclass
class TestIdentifier:
    suite_name: str
    test_name: str

    @staticmethod
    def from_string(string: str):
        suite_name, test_name = string.split("/")
        return TestIdentifier(suite_name, test_name)
