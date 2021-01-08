import argparse
import logging
import os

import pinject
import cato
from cato import logger
from cato.commands.config_template_command import ConfigTemplateCommand
from cato.commands.list_tests_command import ListTestsCommand
from cato.commands.run_command import RunCommand
from cato.commands.update_missing_reference_image import UpdateReferenceImageCommand
from cato.commands.update_missing_reference_images_command import (
    UpdateMissingReferenceImagesCommand,
)
from cato.reporter.test_execution_db_reporter import TestExecutionDbReporter
from cato_api_client import cato_api_client, http_template
from cato_api_client.http_template import HttpTemplate
from cato_server.mappers.mapper_registry_factory import MapperRegistryFactory

PATH_TO_CONFIG_FILE = "Path to config file"
is_executed_as_module = __name__ != "__main__"
if is_executed_as_module:
    logger = logging.getLogger(__name__)  # noqa: F811


def create_object_graph():
    return pinject.new_object_graph(
        modules=[
            cato,
            cato.runners.test_runner,
            cato.runners.command_runner,
            cato.utils.machine_info_collector,
            cato.reporter.stats_calculator,
            cato_api_client,
            http_template,
            cato.commands.config_template_command,
            cato.commands.list_tests_command,
            cato.commands.run_command,
            cato.commands.update_missing_reference_images_command,
            cato.commands.update_missing_reference_image,
        ],
        binding_specs=[TestExecutionReporterBindings()],
    )


class TestExecutionReporterBindings(pinject.BindingSpec):
    def configure(self, bind):
        bind("test_execution_reporter", to_class=TestExecutionDbReporter)
        bind("http_template", to_class=HttpTemplate)
        bind("url", to_instance="http://127.0.0.1:5000")
        bind(
            "mapper_registry",
            to_instance=MapperRegistryFactory().create_mapper_registry(),
        )
        bind("logger", to_instance=logger)


def run(path: str, suite_name: str, test_identifier_str: str):
    obj_graph = create_object_graph()
    run_command = obj_graph.provide(RunCommand)

    run_command.run(path, suite_name, test_identifier_str)


def update_missing_reference_images(path):
    obj_graph = create_object_graph()
    update_missing_reference_images_command = obj_graph.provide(
        UpdateMissingReferenceImagesCommand
    )

    update_missing_reference_images_command.update(path)


def list_tests(path):
    obj_graph = create_object_graph()
    list_tests_command = obj_graph.provide(ListTestsCommand)

    list_tests_command.list_tests(path)


def update_reference(path, test_identifier):
    obj_graph = create_object_graph()
    update_reference_image_command = obj_graph.provide(UpdateReferenceImageCommand)

    update_reference_image_command.update(path, test_identifier)


def config_template(path: str):
    obj_graph = create_object_graph()
    config_template_command = obj_graph.provide(ConfigTemplateCommand)

    config_template_command.create_template(path)


def main():
    parent_parser = argparse.ArgumentParser(add_help=False)
    main_parser = argparse.ArgumentParser()
    commands_subparser = main_parser.add_subparsers(title="commands", dest="command")
    config_template_parser = commands_subparser.add_parser(
        "config-template", help="Create a template config file", parents=[parent_parser]
    )
    config_template_parser.add_argument(
        "path", help="folder where to create the config file"
    )
    run_parser = commands_subparser.add_parser(
        "run", help="Run a config file", parents=[parent_parser]
    )
    run_parser.add_argument("--path", help=PATH_TO_CONFIG_FILE)
    run_parser.add_argument("--suite", help="Suite to run")
    run_parser.add_argument(
        "--test-identifier",
        help="Identifier of test to run. Example: suite_name/test_name",
    )
    update_missing_parser = commands_subparser.add_parser(
        "update-missing-reference-images",
        help="Updates missing reference images after a test run",
        parents=[parent_parser],
    )
    update_missing_parser.add_argument("--path", help=PATH_TO_CONFIG_FILE)
    update_reference_parser = commands_subparser.add_parser(
        "update-reference",
        help="Updates reference images",
        parents=[parent_parser],
    )
    update_reference_parser.add_argument(
        "--test-identifier",
        help="Identifier of test to run. Example: suite_name/test_name",
    )
    update_reference_parser.add_argument("--path", help=PATH_TO_CONFIG_FILE)
    list_parser = commands_subparser.add_parser(
        "list-tests", help="Lists tests in config file", parents=[parent_parser]
    )
    list_parser.add_argument("--path", help=PATH_TO_CONFIG_FILE)

    args = main_parser.parse_args()

    if args.command == "config-template":
        config_template(args.path)
    elif args.command == "run":
        run(args.path, args.suite, args.test_identifier)
    elif args.command == "update-missing-reference-images":
        update_missing_reference_images(args.path)
    elif args.command == "list-tests":
        list_tests(args.path)
    elif args.command == "update-reference":
        update_reference(args.path, args.test_identifier)
    else:
        logger.error(f"No method found to run command {args.command}")


if __name__ == "__main__":
    main()
