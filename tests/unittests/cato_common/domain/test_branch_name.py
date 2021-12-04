import pytest

from cato_common.domain.branch_name import BranchName


def test_create_success():
    assert BranchName("main")


def test_should_throw_exception_for_invalid_branch_name():
    with pytest.raises(ValueError):
        BranchName("")
