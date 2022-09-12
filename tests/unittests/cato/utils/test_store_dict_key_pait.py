import argparse

import pytest

from cato.utils.store_dict_key_pair import StoreDictKeyPair


@pytest.fixture
def testing_parser():
    test_parser = argparse.ArgumentParser()
    test_parser.add_argument(
        "--var",
        action=StoreDictKeyPair,
        nargs="+",
    )
    return test_parser


def test_parse_single(testing_parser):
    args = testing_parser.parse_args(["--var", "my_key=my_value"])

    assert args.var == {"my_key": "my_value"}


def test_parse_multiple(testing_parser):
    args = testing_parser.parse_args(
        ["--var", "my_key=my_value", "--var", "my_other_key=my_other_value"]
    )

    assert args.var == {"my_key": "my_value", "my_other_key": "my_other_value"}


def test_parse_failure(testing_parser):
    with pytest.raises(ValueError):
        testing_parser.parse_args(["--var", "my_key"])
