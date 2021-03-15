import logging
from typing import Optional, Callable

from cato.commands.run_command_interface import RunCommandInterface
from cato.config.config_file_parser import JsonConfigParser
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
)
from cato.reporter.end_message_generator import EndMessageGenerator
from cato.reporter.reporter import Reporter
from cato.reporter.timing_report_generator import TimingReportGenerator
from cato.reporter.verbose_mode import VerboseMode
from cato.runners.test_suite_runner import TestSuiteRunner
from cato_api_client.cato_api_client import CatoApiClient


class RunCommand(RunCommandInterface):
    def __init__(
        self,
        json_config_parser: JsonConfigParser,
        test_suite_runner: TestSuiteRunner,
        timing_report_generator: TimingReportGenerator,
        end_message_generator: EndMessageGenerator,
        logger: logging.Logger,
        reporter: Reporter,
        last_run_information_repository_factory: Callable[
            [str], LastRunInformationRepository
        ],
        cato_api_client: CatoApiClient,
    ):
        super(RunCommand, self).__init__(
            json_config_parser,
            last_run_information_repository_factory,
            cato_api_client,
        )
        self._reporter = reporter
        self._test_suite_runner = test_suite_runner
        self._timing_report_generator = timing_report_generator
        self._end_message_generator = end_message_generator
        self._logger = logger

    def run(
        self,
        path: str,
        suite_name: Optional[str],
        test_identifier_str: Optional[str],
        only_failed: bool,
        verbose_mode: VerboseMode,
    ):
        self._reporter.set_verbose_mode(verbose_mode)
        config = self._prepare_config(
            path, suite_name, test_identifier_str, only_failed
        )

        result = self._test_suite_runner.run_test_suites(config)

        self._logger.info("")
        self._logger.info(self._timing_report_generator.generate(result))

        self._logger.info("")
        self._logger.info(self._end_message_generator.generate_end_message(result))
