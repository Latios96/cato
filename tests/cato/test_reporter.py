from cato.reporter.reporter import Reporter
from cato.reporter.verbose_mode import VerboseMode


def test_should_create_with_default_verbode_mode():
    reporter = Reporter()

    assert reporter._verbose_mode == VerboseMode.DEFAULT


def test_should_set_verbode_mode():
    reporter = Reporter()

    reporter.set_verbose_mode(VerboseMode.VERBOSE)

    assert reporter._verbose_mode == VerboseMode.VERBOSE
