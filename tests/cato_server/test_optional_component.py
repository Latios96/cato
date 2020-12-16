import pytest

from cato_server.configuration.optional_component import OptionalComponent


def test_create_empty():
    optional_component = OptionalComponent.empty()

    assert optional_component.component == None


def test_is_available_should_return_false():
    optional_component = OptionalComponent.empty()

    assert not optional_component.is_available()


@pytest.mark.parametrize("value", ["", "test"])
def test_is_available_should_return_true(value):
    optional_component = OptionalComponent(value)

    assert optional_component.is_available()
