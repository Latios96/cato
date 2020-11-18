import emoji

from cato.reporter.end_message_generator import EndMessageGenerator
from cato.reporter.stats_calculator import StatsCalculator, Stats
from tests.utils import mock_safe


def test_generate_end_message():
    mock_gen_stats = mock_safe(StatsCalculator)
    mock_gen_stats.calculate.return_value = Stats(1, 1, 0)
    generator = EndMessageGenerator(mock_gen_stats)

    message = generator.generate_end_message([])

    assert message == emoji.emojize(
        """Result:
Ran {} tests
{}  succeded :white_check_mark:
{}  failed   :x:""".format(
            1, 1, 0
        ),
        use_aliases=True,
    )
