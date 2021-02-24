import os
import subprocess

import pytest
from alembic import command
from alembic.config import Config

from cato_server.configuration.storage_configuration import StorageConfiguration
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator


def test_db_migrator():
    db_migrator = DbMigrator(
        StorageConfiguration(file_storage_url="", database_url="sqlite:///:memory:")
    )
    db_migrator.migrate()


def can_not_launch_postgres():
    try:
        return subprocess.call(["pg_ctl", "--version"]) != 0
    except Exception as e:
        return True


requires_postgres = pytest.mark.skipif(
    can_not_launch_postgres(), reason="No pg_ctl executable found"
)


@requires_postgres
def test_example_postgres(postgresql, test_resource_provider):
    connection = f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"

    config_path = test_resource_provider.resource_by_name(
        "alembic-config-for-tests.ini"
    )
    alembic_cfg = Config(config_path)
    alembic_cfg.set_section_option("alembic", "sqlalchemy.url", connection)
    alembic_cfg.set_section_option(
        "alembic",
        "script_location",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(config_path))),
            "cato_server",
            "storage",
            "sqlalchemy",
            "migrations",
            "alembic",
        ),
    )

    command.upgrade(alembic_cfg, "head")
