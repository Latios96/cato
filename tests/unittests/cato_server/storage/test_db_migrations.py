import os

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


@pytest.mark.skip
def test_example_postgres(postgresql, test_resource_provider):
    # requires pytest-postgresql
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
            os.path.dirname(os.path.dirname(os.path.dirname(config_path))), "alembic"
        ),
    )

    command.upgrade(alembic_cfg, "head")
