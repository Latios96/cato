import emoji

from cato.reporter.end_message_generator import EndMessageGenerator
from cato.reporter.stats_calculator import StatsCalculator, Stats
from tests.utils import mock_safe


def test_generate_end_message_only_success():
    mock_gen_stats = mock_safe(StatsCalculator)
    mock_gen_stats.calculate.return_value = Stats(1, 1, 0)
    generator = EndMessageGenerator(mock_gen_stats)

    message = generator.generate_end_message([])

    assert message == emoji.emojize(
        """Result:
Ran {} tests
{}  succeded :white_check_mark:""".format(
            1, 1, 0
        ),
        use_aliases=True,
    )


def test_generate_end_message_only_failed():
    mock_gen_stats = mock_safe(StatsCalculator)
    mock_gen_stats.calculate.return_value = Stats(1, 0, 1)
    generator = EndMessageGenerator(mock_gen_stats)

    message = generator.generate_end_message([])

    assert message == emoji.emojize(
        """Result:
Ran {} tests
{}  failed   :x:""".format(
            1, 1
        ),
        use_aliases=True,
    )


def test_generate_end_message_both():
    mock_gen_stats = mock_safe(StatsCalculator)
    mock_gen_stats.calculate.return_value = Stats(2, 1, 1)
    generator = EndMessageGenerator(mock_gen_stats)

    message = generator.generate_end_message([])

    assert message == emoji.emojize(
        """Result:
Ran {} tests
{}  succeded :white_check_mark:
{}  failed   :x:""".format(
            2, 1, 1
        ),
        use_aliases=True,
    )
