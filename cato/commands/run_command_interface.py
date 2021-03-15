import logging
from typing import Optional, Callable

from cato.commands.base_command import BaseCliCommand
from cato.config.config_file_parser import JsonConfigParser
from cato.domain.config import Config
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import (
    filter_by_suite_name,
    filter_by_test_identifier,
    filter_by_test_identifiers,
)
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
)
from cato.reporter.end_message_generator import EndMessageGenerator
from cato.reporter.reporter import Reporter
from cato.reporter.timing_report_generator import TimingReportGenerator
from cato.reporter.verbose_mode import VerboseMode
from cato.runners.test_suite_runner import TestSuiteRunner
from cato_api_client.cato_api_client import CatoApiClient
from cato_server.domain.test_identifier import TestIdentifier


class RunCommandInterface(BaseCliCommand):
    def __init__(
        self,
        json_config_parser: JsonConfigParser,
        last_run_information_repository_factory: Callable[
            [str], LastRunInformationRepository
        ],
        cato_api_client: CatoApiClient,
    ):
        self._json_config_parser = json_config_parser
        self._last_run_information_repository_factory = (
            last_run_information_repository_factory
        )
        self._cato_api_client = cato_api_client

    def _prepare_config(
        self,
        path: str,
        suite_name: Optional[str],
        test_identifier_str: Optional[str],
        only_failed: bool,
    ) -> Config:
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

        return config
