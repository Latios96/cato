import logging

from cato.commands.base_command import BaseCliCommand
from cato_common.config.config_file_parser import JsonConfigParser
from cato.runners.sync_test_edits import SyncTestEdits


class SyncTestEditsCommand(BaseCliCommand):
    def __init__(
        self,
        json_config_parser: JsonConfigParser,
        logger: logging.Logger,
        sync_test_edits: SyncTestEdits,
    ):
        super(SyncTestEditsCommand, self).__init__(json_config_parser)
        self._logger = logger
        self._sync_test_edits = sync_test_edits

    def sync(self, path: str, run_id: int) -> None:
        path = self._config_path(path)
        config = self._read_config(path)

        self._sync_test_edits.update(config, path, run_id)
