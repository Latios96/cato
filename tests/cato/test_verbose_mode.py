import pytest

from cato.reporter.verbose_mode import VerboseMode


@pytest.mark.parametrize(
    "mode1,mode2",
    [
        (VerboseMode.DEFAULT, VerboseMode.DEFAULT),
        (VerboseMode.VERBOSE, VerboseMode.DEFAULT),
        (VerboseMode.VERY_VERBOSE, VerboseMode.DEFAULT),
        (VerboseMode.VERY_VERBOSE, VerboseMode.VERBOSE),
    ],
)
def test_includes(mode1, mode2):
    assert mode1.includes(mode2)


@pytest.mark.parametrize(
    "mode1,mode2",
    [
        (VerboseMode.DEFAULT, VerboseMode.VERBOSE),
        (VerboseMode.VERBOSE, VerboseMode.VERY_VERBOSE),
        (VerboseMode.DEFAULT, VerboseMode.VERY_VERBOSE),
    ],
)
def test_not_includes(mode1, mode2):
    assert not mode1.includes(mode2)
