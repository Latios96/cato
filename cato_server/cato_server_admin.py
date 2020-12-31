import argparse

from sqlalchemy.testing.config import Config

import cato_server.server_logging
from cato_server.configuration.app_configuration_reader import AppConfigurationReader
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator

logger = cato_server.server_logging.logger

from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.configuration.app_configuration_writer import AppConfigurationWriter


def config_template(path):
    if not path:
        path = "config.ini"

    config = AppConfigurationDefaults().create()
    logger.info("Write config to %s", path)
    AppConfigurationWriter().write_file(config, path)


def migrate_db(path):
    if not path:
        path = "config.ini"
    app_config = AppConfigurationReader().read_file(path)

    db_migrator = DbMigrator(app_config.storage_configuration)
    db_migrator.migrate()


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

    migrate_db_parser = commands_subparser.add_parser(
        "migrate-db", help="Runs db migrations", parents=[parent_parser]
    )
    migrate_db_parser.add_argument(
        "--path", help="folder where to create the config file"
    )

    args = main_parser.parse_args()

    if args.command == "config-template":
        config_template(args.path)
    elif args.command == "migrate-db":
        migrate_db(args.path)
    else:
        logger.error(f"No method found to run command {args.command}")


if __name__ == "__main__":
    main()
