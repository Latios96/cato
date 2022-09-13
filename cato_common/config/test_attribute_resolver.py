from typing import Dict, Optional, cast
from jsonpath_ng import parse  # type: ignore


class AttributeNotDefinedError(Exception):
    def __init__(self, attribute_path: str):
        super(AttributeNotDefinedError, self).__init__(
            f"Could not resolve attribute '{attribute_path}' for test, because it was not defined on project, suite or test level."
        )


class TestAttributeResolver:
    __test__ = False

    def __init__(
        self,
        project_data: Dict[str, str],
        suite_data: Dict[str, str],
        test_data: Dict[str, str],
    ):
        self._project_data = project_data
        self._suite_data = suite_data
        self._test_data = test_data

    def resolve_optional_attribute(self, attribute_path: str) -> Optional[str]:
        return self._resolve(attribute_path)

    def resolve_required_attribute(self, attribute_path: str) -> str:
        resolved_value = self._resolve(attribute_path)

        if resolved_value is not None:
            return resolved_value

        raise AttributeNotDefinedError(attribute_path)

    def _resolve(self, attribute_path: str) -> Optional[str]:
        resolved_value = None

        project_value = self._resolve_for_project(attribute_path)
        if project_value is not None:
            resolved_value = project_value

        suite_value = self._resolve_for_suite(attribute_path)
        if suite_value is not None:
            resolved_value = suite_value

        test_value = self._resolve_for_test(attribute_path)
        if test_value is not None:
            resolved_value = test_value

        return resolved_value

    def _resolve_for_project(self, attribute_path: str) -> Optional[str]:
        return self._access_attribute_by_path(self._project_data, attribute_path)

    def _resolve_for_suite(self, attribute_path: str) -> Optional[str]:
        return self._access_attribute_by_path(self._suite_data, attribute_path)

    def _resolve_for_test(self, attribute_path: str) -> Optional[str]:
        return self._access_attribute_by_path(self._test_data, attribute_path)

    def _access_attribute_by_path(
        self, data: Dict[str, str], attribute_path: str
    ) -> Optional[str]:
        if not attribute_path.startswith("$."):
            attribute_path = f"$.{attribute_path}"
        expr = parse(attribute_path)

        result = expr.find(data)
        if not result:
            return None
        return cast(str, result[0].value)
