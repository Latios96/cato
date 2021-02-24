import subprocess

import pytest

from cato_server.configuration.storage_configuration import StorageConfiguration
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator


def test_db_migrator_sqlite():
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
def test_db_migrator_postgresql(postgresql):
    connection = f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"
    db_migrator = DbMigrator(
        StorageConfiguration(file_storage_url="", database_url=connection)
    )
    db_migrator.migrate()
