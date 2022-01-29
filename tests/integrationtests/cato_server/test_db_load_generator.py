import os
import subprocess
import sys
import datetime

import humanfriendly

from cato_server import db_load_generator
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.app_configuration_writer import AppConfigurationWriter
from cato_server.configuration.logging_configuration import LoggingConfiguration
from cato_server.configuration.scheduler_configuration import SchedulerConfiguration
from cato_server.configuration.sentry_configuration import SentryConfiguration
from cato_server.configuration.session_configuration import SessionConfiguration
from cato_server.configuration.storage_configuration import StorageConfiguration
from tests.conftest import random_port
from cato_common.utils.change_cwd import change_cwd


def test_run_db_load_test(tmp_path, snapshot):
    config = AppConfiguration(
        port=random_port(),
        debug=True,
        storage_configuration=StorageConfiguration(
            database_url="sqlite:///:memory:", file_storage_url=str(tmp_path)
        ),
        logging_configuration=LoggingConfiguration(
            "log.txt", False, humanfriendly.parse_size("10mb"), 10
        ),
        scheduler_configuration=SchedulerConfiguration(),
        sentry_configuration=SentryConfiguration(url=None),
        session_configuration=SessionConfiguration(
            lifetime=datetime.timedelta(hours=2)
        ),
    )
    config_path = os.path.join(str(tmp_path), "config.ini")
    AppConfigurationWriter().write_file(config, config_path)

    with change_cwd(str(tmp_path)):
        output = subprocess.check_output(
            [sys.executable, db_load_generator.__file__],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding="utf-8",
        )

        assert (
            "cato_server - INFO - Generating total 1 projects, 10 runs, 50 suites and 750 test results.."
            in output
        )
        assert "Inserted 50 suite results" in output
