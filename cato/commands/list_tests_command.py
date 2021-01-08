import logging

from cato.commands.base_command import BaseCliCommand
from cato.config.config_file_parser import JsonConfigParser
from cato.domain.test_suite import count_tests, count_suites, iterate_suites_and_tests


class ListTestsCommand(BaseCliCommand):
    def __init__(
        self,
        json_config_parser: JsonConfigParser,
        logger: logging.Logger,
    ):
        self._json_config_parser = json_config_parser
        self._logger = logger

    def list_tests(self, path: str):
        path = self._config_path(path)
        config = self._json_config_parser.parse(path)
        self._logger.info(
            f"Found {count_tests(config.test_suites)} tests in {count_suites(config.test_suites)} suites:"
        )
        self._logger.info("")

        for suite, test in iterate_suites_and_tests(config.test_suites):
            self._logger.info(f"{suite.name}/{test.name}")
