import logging
import os
import sys
from typing import Optional, Callable

from cato.commands.run_command_interface import RunCommandInterface
from cato.config.config_file_parser import JsonConfigParser
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
)
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.submission_info import SubmissionInfo


class SubmitCommand(RunCommandInterface):
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
        super(SubmitCommand, self).__init__(
            json_config_parser,
            last_run_information_repository_factory,
            cato_api_client,
        )
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
    ) -> None:
        config = self._prepare_config(
            path, suite_name, test_identifier_str, only_failed
        )

        if not config.suites:
            raise ValueError("At least one TestSuite is required!")

        self._test_execution_reporter.start_execution(
            config.project_name, config.suites
        )

        submission_info = SubmissionInfo(
            id=0,
            config=config.to_config(),
            run_id=self._test_execution_reporter.run_id(),
            resource_path=os.path.join(config.resource_path),
            executable=sys.executable,
        )

        self._logger.info("Submitting to scheduler..")
        self._cato_api_client.submit_to_scheduler(submission_info)

        self._logger.info(
            f"Submitted {config.suite_count} suite{'s' if config.suite_count > 1 else ''} with {config.test_count} test{'s' if config.test_count > 1 else ''} to scheduler."
        )
