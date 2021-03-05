from pathlib import Path
from typing import Optional

import pytest

from cato_server.configuration.storage_configuration import StorageConfiguration
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator


def test_db_migrator_sqlite():
    db_migrator = DbMigrator(
        StorageConfiguration(file_storage_url="", database_url="sqlite:///:memory:")
    )
    db_migrator.migrate()


def find_pg_ctl(ver: str) -> Optional[Path]:
    candidates = list(Path(f"/usr/lib/postgresql/{ver}/").glob("**/bin/pg_ctl"))
    if candidates:
        return candidates[0]


def can_not_launch_postgres():
    ctl = find_pg_ctl("12")
    if not ctl:
        return True
    return False


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
