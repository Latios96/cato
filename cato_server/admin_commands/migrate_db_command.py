from cato_server.configuration.app_configuration_reader import AppConfigurationReader
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator


class MigrateDbCommand:
    def migrate_db(self, config_path: str) -> None:
        app_config = AppConfigurationReader().read_file(config_path)
        db_migrator = DbMigrator(app_config.storage_configuration)
        db_migrator.migrate()
