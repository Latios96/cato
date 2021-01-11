from typing import Optional
import logging

from cato.commands.base_command import BaseCliCommand
from cato.config.config_file_parser import JsonConfigParser
from cato.domain.test_suite import filter_by_suite_name, filter_by_test_identifier
from cato.reporter.end_message_generator import EndMessageGenerator
from cato.reporter.reporter import Reporter
from cato.reporter.timing_report_generator import TimingReportGenerator
from cato.reporter.verbose_mode import VerboseMode
from cato.runners.test_suite_runner import TestSuiteRunner
from cato_server.domain.test_identifier import TestIdentifier


class RunCommand(BaseCliCommand):
    def __init__(
        self,
        json_config_parser: JsonConfigParser,
        test_suite_runner: TestSuiteRunner,
        timing_report_generator: TimingReportGenerator,
        end_message_generator: EndMessageGenerator,
        logger: logging.Logger,
        reporter: Reporter,
    ):
        self._json_config_parser = json_config_parser
        self._test_suite_runner = test_suite_runner
        self._timing_report_generator = timing_report_generator
        self._end_message_generator = end_message_generator
        self._logger = logger
        self._reporter = reporter

    def run(
        self,
        path: str,
        suite_name: Optional[str],
        test_identifier_str: Optional[str],
        verbose_mode: VerboseMode,
    ):
        self._reporter.set_verbose_mode(verbose_mode)
        path = self._config_path(path)

        config = self._json_config_parser.parse(path)

        if suite_name:
            config.test_suites = filter_by_suite_name(config.test_suites, suite_name)
        if test_identifier_str:
            config.test_suites = filter_by_test_identifier(
                config.test_suites, TestIdentifier.from_string(test_identifier_str)
            )

        result = self._test_suite_runner.run_test_suites(config)

        self._logger.info("")
        self._logger.info(self._timing_report_generator.generate(result))

        self._logger.info("")
        self._logger.info(self._end_message_generator.generate_end_message(result))