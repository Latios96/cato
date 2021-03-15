import logging
import os
import sys
from typing import Optional, Callable

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
)
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato_api_client.cato_api_client import CatoApiClient
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.schedulers.submission_info import SubmissionInfo


class SubmitCommand(BaseCliCommand):
    def __init__(
        self,
        json_config_parser: JsonConfigParser,
        logger: logging.Logger,
        last_run_information_repository_factory: Callable[
            [str], LastRunInformationRepository
        ],
        cato_api_client: CatoApiClient,
        test_execution_reporter: TestExecutionReporter,
    ):
        self._json_config_parser = json_config_parser
        self._logger = logger
        self._last_run_information_repository_factory = (
            last_run_information_repository_factory
        )
        self._cato_api_client = cato_api_client
        self._test_execution_reporter = test_execution_reporter

    def run(
        self,
        path: str,
        suite_name: Optional[str],
        test_identifier_str: Optional[str],
        only_failed: bool,
    ):
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

        if not config.test_suites:
            raise ValueError("At least one TestSuite is required!")

        self._test_execution_reporter.start_execution(
            config.project_name, config.test_suites
        )

        submission_info = SubmissionInfo(
            config=config,
            run_id=self._test_execution_reporter.run_id(),
            resource_path=os.path.join(config.path, "config.ini"),
            executable=sys.executable,
        )

        self._cato_api_client.submit_to_scheduler(submission_info)
