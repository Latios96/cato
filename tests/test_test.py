import pytest

from cato.domain.test import Test


def test_create_with_empty_name_should_fail():
    with pytest.raises(ValueError):
        Test(name="", command="", variables={})


@pytest.mark.parametrize("name", [" ", "", "/", ",", '"', "'", "\\"])
def test_create_with_unallowed_chars_should_fail(name):
    with pytest.raises(ValueError):
        Test(name=name, command="", variables={})
