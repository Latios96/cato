from dataclasses import dataclass


@dataclass
class TestIdentifier:
    suite_name: str
    test_name: str

    def __post_init__(self):
        self._validate_test_identifier_part("suite name", self.suite_name)
        self._validate_test_identifier_part("test_name", self.test_name)

    @staticmethod
    def from_string(string):
        # type: (str) -> TestIdentifier
        splitted_string = string.split("/")
        if len(splitted_string) != 2:
            raise ValueError(f"Invalid test identifier: {string}")
        suite_name, test_name = splitted_string
        return TestIdentifier(suite_name, test_name)

    def __str__(self):
        return f"{self.suite_name}/{self.test_name}"

    __test__ = False

    def _validate_test_identifier_part(self, part, value):
        if "/" in value:
            raise ValueError(r"Test Identifier {part} can not contain '/'")
