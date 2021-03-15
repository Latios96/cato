import argparse
import logging

import pinject
from typing import Type, TypeVar, Optional

from pinject.object_graph import ObjectGraph

import cato
from cato import logger
from cato.commands.config_template_command import ConfigTemplateCommand
from cato.commands.list_tests_command import ListTestsCommand
from cato.commands.run_command import RunCommand
from cato.commands.submit_command import SubmitCommand
from cato.commands.update_missing_reference_image import UpdateReferenceImageCommand
from cato.commands.update_missing_reference_images_command import (
    UpdateMissingReferenceImagesCommand,
)
from cato.commands.worker_run_command import WorkerRunCommand
from cato.config.config_encoder import ConfigEncoder  # noqa: F401
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
)
from cato.reporter.test_execution_db_reporter import TestExecutionDbReporter
from cato.reporter.verbose_mode import VerboseMode
from cato_api_client import cato_api_client, http_template
from cato_api_client.http_template import HttpTemplate
from cato_server.mappers.mapper_registry_factory import MapperRegistryFactory

PATH_TO_CONFIG_FILE = "Path to config file"
is_executed_as_module = __name__ != "__main__"
if is_executed_as_module:
    logger = logging.getLogger(__name__)  # noqa: F811

T = TypeVar("T")


def provide_safe(obj_graph: ObjectGraph, cls: Type[T]) -> T:
    return obj_graph.provide(cls)


def create_object_graph(url: Optional[str] = None):
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
            cato.config.config_encoder,
            cato.config.config_file_parser,
        ],
        binding_specs=[TestExecutionReporterBindings(url)],
    )


class TestExecutionReporterBindings(pinject.BindingSpec):
    def __init__(self, url: Optional[str]):
        self._url = url if url else "<not given>"

    def configure(self, bind):
        bind("test_execution_reporter", to_class=TestExecutionDbReporter)
        bind("http_template", to_class=HttpTemplate)
        bind("url", to_instance=self._url)
        bind(
            "mapper_registry",
            to_instance=MapperRegistryFactory().create_mapper_registry(),
        )
        bind("logger", to_instance=logger)
        bind(
            "last_run_information_repository_factory",
            to_instance=lambda x: LastRunInformationRepository(x),
        )


def run(
    path: str,
    suite_name: str,
    test_identifier_str: str,
    only_failed: bool,
    verbose: int,
    url: str,
):
    obj_graph = create_object_graph(url)
    run_command = provide_safe(obj_graph, RunCommand)

    verbose_mode = VerboseMode.in_range(verbose)

    run_command.run(
        path, suite_name, test_identifier_str, bool(only_failed), verbose_mode
    )


def submit(
    path: str,
    suite_name: str,
    test_identifier_str: str,
    only_failed: bool,
    url: str,
):
    obj_graph = create_object_graph(url)
    submit_command = provide_safe(obj_graph, SubmitCommand)

    submit_command.run(path, suite_name, test_identifier_str, bool(only_failed))


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


def worker_run(
    url: str,
    encoded_config: str,
    test_identifier_str: str,
    run_id: int,
    resource_path: str,
):
    obj_graph = create_object_graph(url)
    worker_command = provide_safe(obj_graph, WorkerRunCommand)

    worker_command.execute(encoded_config, test_identifier_str, run_id, resource_path)


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
    run_parser.add_argument("-u", "--url", help="url to server", required=True)
    run_parser.add_argument("-v", "--verbose", action="count", default=1)
    run_parser.add_argument("--only-failed", action="store_true")

    submit_parser = commands_subparser.add_parser(
        "submit",
        help="Submit tests from a config file to scheduler",
        parents=[parent_parser],
    )
    submit_parser.add_argument("--path", help=PATH_TO_CONFIG_FILE)
    submit_parser.add_argument("--suite", help="Suite to run")
    submit_parser.add_argument(
        "--test-identifier",
        help="Identifier of test to run. Example: suite_name/test_name",
    )
    submit_parser.add_argument("-u", "--url", help="url to server", required=True)
    submit_parser.add_argument("--only-failed", action="store_true")

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

    worker_execute_command_parser = commands_subparser.add_parser(
        "worker-run",
        help="Tun test in a distributed environment. Not for direct human use",
        parents=[parent_parser],
    )
    worker_execute_command_parser.add_argument(
        "-u", "--url", help="url to server", required=True
    )
    worker_execute_command_parser.add_argument(
        "-config", required=True, help="base64 encoded config JSON"
    )
    worker_execute_command_parser.add_argument(
        "-test-identifier", required=True, help="Identifier of the test to run"
    )
    worker_execute_command_parser.add_argument(
        "-run-id", required=True, type=int, help="run id to report to"
    )
    worker_execute_command_parser.add_argument(
        "-resource-path",
        required=True,
        help="folder where tests resources (scenes etc) are located",
    )

    args = main_parser.parse_args()

    if args.command == "config-template":
        config_template(args.path)
    elif args.command == "run":
        run(
            args.path,
            args.suite,
            args.test_identifier,
            args.only_failed,
            args.verbose,
            args.url,
        )
    elif args.command == "submit":
        submit(
            args.path,
            args.suite,
            args.test_identifier,
            args.only_failed,
            args.url,
        )
    elif args.command == "update-missing-reference-images":
        update_missing_reference_images(args.path)
    elif args.command == "list-tests":
        list_tests(args.path)
    elif args.command == "update-reference":
        update_reference(args.path, args.test_identifier)
    elif args.command == "worker-run":
        worker_run(
            args.url, args.config, args.test_identifier, args.run_id, args.resource_path
        )
    else:
        logger.error(f"No method found to run command {args.command}")


if __name__ == "__main__":
    main()
