from dataclasses import dataclass


@dataclass
class TestIdentifier:
    suite_name: str
    test_name: str

    @staticmethod
    def from_string(string: str):
        suite_name, test_name = string.split("/")
        return TestIdentifier(suite_name, test_name)

    def __str__(self):
        return f"{self.suite_name}/{self.test_name}"

    __test__ = False
