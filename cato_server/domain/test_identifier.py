import attr


@attr.s
class TestIdentifier:
    suite_name: str = attr.ib()
    test_name: str = attr.ib()

    @staticmethod
    def from_string(string: str):
        splitted_string = string.split("/")
        if len(splitted_string) != 2:
            raise ValueError(f"Invalid test identifier: {string}")
        suite_name, test_name = splitted_string
        return TestIdentifier(suite_name, test_name)

    def __str__(self):
        return f"{self.suite_name}/{self.test_name}"

    __test__ = False

    @suite_name.validator
    def _check_suite_name(self, attribute, value):
        self._validate_test_identifier_part("suite name", value)

    @test_name.validator
    def _check_test_name(self, attribute, value):
        self._validate_test_identifier_part("suite name", value)

    def _validate_test_identifier_part(self, part, value):
        if "/" in value:
            raise ValueError(r"Test Identifier {part} can not contain '/'")
