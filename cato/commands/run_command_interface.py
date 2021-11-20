from typing import Optional, Callable

from cato.commands.base_command import BaseCliCommand
from cato.config.config_file_parser import JsonConfigParser
from cato.domain.config import RunConfig
from cato_common.domain.result_status import ResultStatus
from cato.domain.test_suite import (
    filter_by_suite_name,
    filter_by_test_identifier,
    filter_by_test_identifiers,
)
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
)
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.unified_test_status import UnifiedTestStatus


class RunCommandInterface(BaseCliCommand):
    def __init__(
        self,
        json_config_parser: JsonConfigParser,
        last_run_information_repository_factory: Callable[
            [str], LastRunInformationRepository
        ],
        cato_api_client: CatoApiClient,
    ):
        super(RunCommandInterface, self).__init__(json_config_parser)
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
    ) -> RunConfig:
        path = self._config_path(path)
        config = self._read_config(path)

        last_run_information = None
        if only_failed:
            repo = self._last_run_information_repository_factory(config.output_folder)
            last_run_information = repo.read_last_run_information()

        if suite_name:
            config.suites = filter_by_suite_name(config.suites, suite_name)
        if test_identifier_str:
            config.suites = filter_by_test_identifier(
                config.suites, TestIdentifier.from_string(test_identifier_str)
            )

        if last_run_information:
            failed_test_identifiers = (
                self._cato_api_client.get_test_results_by_run_id_and_test_status(
                    last_run_information.last_run_id, UnifiedTestStatus.FAILED
                )
            )
            if not failed_test_identifiers:
                failed_test_identifiers = []
            config.suites = filter_by_test_identifiers(
                config.suites, failed_test_identifiers
            )

        return config
