import pytest

from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.test import Test


def test_create_with_empty_name_should_fail():
    with pytest.raises(ValueError):
        Test(
            name="",
            command="",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )


# test legal: "test test"


@pytest.mark.parametrize(
    "name",
    [
        "",
        "test/test",
        "test\\test",
        "tes:test",
        "test*test",
        "test?",
        "<test",
        "test>",
        "test|test",
    ],
)
def test_create_with_unallowed_chars_should_fail(name):
    with pytest.raises(ValueError):
        Test(
            name=name,
            command="",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )
