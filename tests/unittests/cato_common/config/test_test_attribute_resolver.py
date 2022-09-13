import pytest

from cato_common.config.test_attribute_resolver import (
    TestAttributeResolver,
    AttributeNotDefinedError,
)


def test_resolve_required_should_fail_because_no_data_was_defined():
    resolver = TestAttributeResolver(project_data={}, suite_data={}, test_data={})

    with pytest.raises(AttributeNotDefinedError):
        resolver.resolve_required_attribute("command")


def test_resolve_optional_should_return_none_because_no_data_was_defined():
    resolver = TestAttributeResolver(project_data={}, suite_data={}, test_data={})

    resolved_value = resolver.resolve_optional_attribute("command")

    assert resolved_value is None


def test_resolve_should_take_project_value():
    resolver = TestAttributeResolver(
        project_data={"command": "project_command"}, suite_data={}, test_data={}
    )

    resolved_value = resolver.resolve_required_attribute("command")

    assert resolved_value == "project_command"


def test_resolve_should_take_suite_value():
    resolver = TestAttributeResolver(
        project_data={}, suite_data={"command": "suite_command"}, test_data={}
    )

    resolved_value = resolver.resolve_required_attribute("command")

    assert resolved_value == "suite_command"


def test_resolve_should_take_suite_value_instead_of_project_value():
    resolver = TestAttributeResolver(
        project_data={"command": "project_command"},
        suite_data={"command": "suite_command"},
        test_data={},
    )

    resolved_value = resolver.resolve_required_attribute("command")

    assert resolved_value == "suite_command"


def test_resolve_should_take_test_value():
    resolver = TestAttributeResolver(
        project_data={}, suite_data={}, test_data={"command": "test_command"}
    )

    resolved_value = resolver.resolve_required_attribute("command")

    assert resolved_value == "test_command"


def test_resolve_should_take_test_value_instead_of_suite_value():
    resolver = TestAttributeResolver(
        project_data={},
        suite_data={"command": "suite_command"},
        test_data={"command": "test_command"},
    )

    resolved_value = resolver.resolve_required_attribute("command")

    assert resolved_value == "test_command"


def test_resolve_should_take_test_value_instead_of_project_value():
    resolver = TestAttributeResolver(
        project_data={"command": "project_command"},
        suite_data={},
        test_data={"command": "test_command"},
    )

    resolved_value = resolver.resolve_required_attribute("command")

    assert resolved_value == "test_command"


def test_resolve_should_take_test_value_instead_of_project_or_suite_value():
    resolver = TestAttributeResolver(
        project_data={"command": "project_command"},
        suite_data={"command": "suite_command"},
        test_data={"command": "test_command"},
    )

    resolved_value = resolver.resolve_required_attribute("command")

    assert resolved_value == "test_command"


def test_resolve_should_take_nested_project_value():
    resolver = TestAttributeResolver(
        project_data={"comparison_settings": {"method": "SSIM"}},
        suite_data={},
        test_data={},
    )

    resolved_value = resolver.resolve_required_attribute("comparison_settings.method")

    assert resolved_value == "SSIM"
