from typing import Optional, Callable
import logging

from cato.commands.base_command import BaseCliCommand
from cato.config.config_file_parser import JsonConfigParser
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import (
    filter_by_suite_name,
    filter_by_test_identifier,
    filter_by_test_identifiers,
)
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
    LastRunInformation,
)
from cato.reporter.end_message_generator import EndMessageGenerator
from cato.reporter.reporter import Reporter
from cato.reporter.timing_report_generator import TimingReportGenerator
from cato.reporter.verbose_mode import VerboseMode
from cato.runners.test_suite_runner import TestSuiteRunner
from cato_api_client.cato_api_client import CatoApiClient
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
        last_run_information_repository_factory: Callable[
            [str], LastRunInformationRepository
        ],
        cato_api_client: CatoApiClient,
    ):
        self._json_config_parser = json_config_parser
        self._test_suite_runner = test_suite_runner
        self._timing_report_generator = timing_report_generator
        self._end_message_generator = end_message_generator
        self._logger = logger
        self._reporter = reporter
        self._last_run_information_repository_factory = (
            last_run_information_repository_factory
        )
        self._cato_api_client = cato_api_client

    def run(
        self,
        path: str,
        suite_name: Optional[str],
        test_identifier_str: Optional[str],
        only_failed: bool,
        verbose_mode: VerboseMode,
    ):
        self._reporter.set_verbose_mode(verbose_mode)
        path = self._config_path(path)

        config = self._json_config_parser.parse(path)

        last_run_information = None
        if only_failed:
            repo = self._last_run_information_repository_factory(config.output_folder)
            last_run_information = repo.read_last_run_information()

        if suite_name:
            config.test_suites = filter_by_suite_name(config.test_suites, suite_name)
        if test_identifier_str:
            config.test_suites = filter_by_test_identifier(
                config.test_suites, TestIdentifier.from_string(test_identifier_str)
            )

        if last_run_information:
            failed_test_identifiers = (
                self._cato_api_client.get_test_results_by_run_id_and_test_status(
                    last_run_information.last_run_id, TestStatus.FAILED
                )
            )
            config.test_suites = filter_by_test_identifiers(
                config.test_suites, failed_test_identifiers
            )

        result = self._test_suite_runner.run_test_suites(config)

        self._logger.info("")
        self._logger.info(self._timing_report_generator.generate(result))

        self._logger.info("")
        self._logger.info(self._end_message_generator.generate_end_message(result))
