import argparse
import os

import cato_server.server_logging
from cato_server.admin_commands.config_template_command import ConfigTemplateCommand
from cato_server.backup.backup_creator import BackupCreator
from cato_server.backup.backup_mode import BackupMode
from cato_server.backup.create_db_backup import CreateDbBackup
from cato_server.backup.create_file_storage_backup import CreateFileStorageBackup
from cato_server.backup.pg_dump_path_resolver import PgDumpPathResolver
from cato_server.configuration.app_configuration_reader import AppConfigurationReader
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator

logger = cato_server.server_logging.logger


def config_template(path, try_out):
    if not path:
        path = "config.ini"

    config_template_command = ConfigTemplateCommand()
    config_template_command.create_config_template(path, try_out)


def migrate_db(path):
    if not path:
        path = "config.ini"
    app_config = AppConfigurationReader().read_file(path)

    db_migrator = DbMigrator(app_config.storage_configuration)
    db_migrator.migrate()


def create_backup(path, pg_dump_executable, mode_str):
    if not path:
        path = "config.ini"
    app_config = AppConfigurationReader().read_file(path)

    pg_dump_path_resolver = PgDumpPathResolver()
    pg_dump_path = pg_dump_path_resolver.resolve(pg_dump_executable)

    create_file_storage_backup = CreateFileStorageBackup(
        app_config.storage_configuration
    )
    create_db_backup = CreateDbBackup(app_config.storage_configuration, pg_dump_path)

    mode = BackupMode(mode_str) if mode_str else BackupMode.FULL

    backup_creator = BackupCreator(create_file_storage_backup, create_db_backup)
    backup_creator.create_backup(os.getcwd(), mode)


def main():
    parent_parser = argparse.ArgumentParser(add_help=False)
    main_parser = argparse.ArgumentParser()
    commands_subparser = main_parser.add_subparsers(title="commands", dest="command")

    config_template_parser = commands_subparser.add_parser(
        "config-template", help="Create a template config file", parents=[parent_parser]
    )
    config_template_parser.add_argument(
        "--path", help="folder where to create the config file"
    )
    config_template_parser.add_argument(
        "--try-out",
        default=False,
        action="store_true",
        help="Creates a config ready to use without any need for configuration for demonstration purposes",
    )

    migrate_db_parser = commands_subparser.add_parser(
        "migrate-db", help="Runs db migrations", parents=[parent_parser]
    )
    migrate_db_parser.add_argument("--config", help="path to config.ini")

    create_backup_parser = commands_subparser.add_parser(
        "create-backup",
        help="Creates a backup of the database and the file storage",
        parents=[parent_parser],
    )
    create_backup_parser.add_argument("--config", help="path to config.ini")
    create_backup_parser.add_argument(
        "--pg-dump-path", help="path to pg_dump executable"
    )
    create_backup_parser.add_argument(
        "--backup-mode",
        help="mode for backup. Possible values are FULL (default), ONLY_DATABASE, ONLY_FILESTORAGE",
    )

    args = main_parser.parse_args()

    if args.command == "config-template":
        config_template(args.path, args.try_out)
    elif args.command == "migrate-db":
        migrate_db(args.config)
    elif args.command == "create-backup":
        create_backup(args.config, args.pg_dump_path, args.backup_mode)
    else:
        logger.error(f"No method found to run command {args.command}")


if __name__ == "__main__":
    main()
