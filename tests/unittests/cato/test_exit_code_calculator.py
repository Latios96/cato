from cato.reporter.exit_code_calculator import ExitCodeCalculator
from cato.reporter.stats_calculator import StatsCalculator, Stats
from tests.utils import mock_safe


def test_no_failed_test_should_generate_exit_code_0():
    mock_gen_stats = mock_safe(StatsCalculator)
    mock_gen_stats.calculate.return_value = Stats(1, 1, 0)
    generator = ExitCodeCalculator(mock_gen_stats)

    exit_code = generator.generate_exit_code([])

    assert exit_code == 0


def test_failed_test_should_generate_exit_code_0():
    mock_gen_stats = mock_safe(StatsCalculator)
    mock_gen_stats.calculate.return_value = Stats(1, 0, 1)
    generator = ExitCodeCalculator(mock_gen_stats)

    exit_code = generator.generate_exit_code([])

    assert exit_code == 1
