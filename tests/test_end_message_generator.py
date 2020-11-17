import emoji

from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_result import TestStatus
from cato.domain.test_suite import TestSuite
from cato.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.reporter.end_message_generator import EndMessageGenerator


def test_generate_end_message():
    test = Test(name="my first test", command="dummy_command", variables={})
    test_suite = TestSuite(name="example", tests=[test])
    execution_result = TestExecutionResult(test, TestStatus.SUCCESS, [], 1, "this is a message")
    result = [
        TestSuiteExecutionResult(test_suite, TestStatus.SUCCESS, [execution_result])
    ]
    generator = EndMessageGenerator()

    message = generator.generate_end_message(result)

    assert message == emoji.emojize(
        """Result:
Ran {} tests
{}  succeded :white_check_mark:
{}  failed   :x:""".format(
            1, 1, 0
        ),
        use_aliases=True,
    )
