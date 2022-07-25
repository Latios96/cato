from cato_server.configuration.parts.storage_configuration import StorageConfiguration
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator


def test_db_migrator(db_connection_string):
    db_migrator = DbMigrator(
        StorageConfiguration(file_storage_url="", database_url=db_connection_string)
    )
    db_migrator.migrate()
