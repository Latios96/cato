import argparse

import pinject
from pinject.object_graph import ObjectGraph

import cato_common
import cato_server.server_logging
from cato_common.utils.bindings import imported_modules, provide_safe
from cato_server.admin_commands.config_template_command import ConfigTemplateCommand
from cato_server.admin_commands.create_api_token_command import CreateApiTokenCommand
from cato_server.admin_commands.create_backup_command import CreateBackupCommand
from cato_server.admin_commands.migrate_db_command import MigrateDbCommand
from cato_server.admin_commands.wait_for_db_connection_command import (
    WaitForDbConnectionCommand,
)
from cato_server.configuration.app_configuration_reader import AppConfigurationReader
from cato_server.configuration.bindings_factory import BindingsFactory

logger = cato_server.server_logging.logger


def get_config_path(path):
    if not path:
        path = "config.ini"
    return path


def create_obj_graph(path: str) -> ObjectGraph:
    config = AppConfigurationReader().read_file(path)

    bindings_factory = BindingsFactory(config)
    bindings = bindings_factory.create_bindings()

    obj_graph = pinject.new_object_graph(
        modules=[*imported_modules([cato_common, cato_server])],
        binding_specs=[bindings],
    )
    return obj_graph


def config_template(path, try_out):
    path = get_config_path(path)

    config_template_command = ConfigTemplateCommand()
    config_template_command.create_config_template(path, try_out)


def migrate_db(path):
    path = get_config_path(path)

    migrate_db_command = MigrateDbCommand()
    migrate_db_command.migrate_db(path)


def create_backup(path, pg_dump_executable, mode_str):
    path = get_config_path(path)

    create_backup_command = CreateBackupCommand()
    create_backup_command.create_backup(path, pg_dump_executable, mode_str)


def create_api_token(path):
    path = get_config_path(path)
    obj_graph = create_obj_graph(path)

    create_api_token = provide_safe(obj_graph, CreateApiTokenCommand)
    create_api_token.create_api_token()


def wait_for_db_connection(path):
    path = get_config_path(path)
    obj_graph = create_obj_graph(path)

    wait_for_connection_command = provide_safe(obj_graph, WaitForDbConnectionCommand)
    wait_for_connection_command.wait_for_connection()


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

    create_api_token_parser = commands_subparser.add_parser(
        "create-api-token", help="Create a new api token", parents=[parent_parser]
    )
    create_api_token_parser.add_argument("--config", help="path to config.ini")

    wait_for_db_connection_parser = commands_subparser.add_parser(
        "wait-for-db-connection",
        help="Waits until the application can connect to the database",
        parents=[parent_parser],
    )
    wait_for_db_connection_parser.add_argument("--config", help="path to config.ini")

    args = main_parser.parse_args()

    if args.command == "config-template":
        config_template(args.path, args.try_out)
    elif args.command == "migrate-db":
        migrate_db(args.config)
    elif args.command == "create-backup":
        create_backup(args.config, args.pg_dump_path, args.backup_mode)
    elif args.command == "create-api-token":
        create_api_token(args.config)
    elif args.command == "wait-for-db-connection":
        wait_for_db_connection(args.config)
    else:
        logger.error(f"No method found to run command {args.command}")


if __name__ == "__main__":
    main()
