import argparse
import logging
import os.path
from typing import Optional, Dict

import pinject
from pinject.object_graph import ObjectGraph

import cato
import cato_api_client
import cato_common
from cato import logger
from cato.authentication.api_token_storage import ApiTokenStorage
from cato.commands.config_template_command import ConfigTemplateCommand
from cato.commands.list_tests_command import ListTestsCommand
from cato.commands.run_command import RunCommand
from cato.commands.submit_command import SubmitCommand
from cato.commands.sync_test_edits_command import SyncTestEditsCommand
from cato.commands.update_missing_reference_images_command import (
    UpdateMissingReferenceImagesCommand,
)
from cato.commands.update_reference_image_command import UpdateReferenceImageCommand
from cato.commands.worker_run_command import WorkerRunCommand
from cato.utils.config_utils import (
    read_url_from_config_path,
)
from cato.utils.store_dict_key_pair import StoreDictKeyPair
from cato_common.config.user_config.user_config_repository import UserConfigRepository
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
)
from cato.reporter.test_execution_db_reporter import TestExecutionDbReporter
from cato.reporter.verbose_mode import VerboseMode
from cato.utils.url_format import format_url
from cato_api_client.http_template import HttpTemplate
from cato_common.utils.bindings import imported_modules, provide_safe
from cato_common.mappers.mapper_registry_factory import MapperRegistryFactory

PATH_TO_CONFIG_FILE = "Path to config file"
is_executed_as_module = __name__ != "__main__"
if is_executed_as_module:
    logger = logging.getLogger(__name__)  # noqa: F811


def create_object_graph(
    path: Optional[str] = None, url: Optional[str] = None, require_url: bool = False
) -> ObjectGraph:
    if url:
        url = format_url(url)
    return pinject.new_object_graph(
        modules=[*imported_modules([cato, cato_api_client, cato_common])],
        binding_specs=[TestExecutionReporterBindings(path, url, require_url)],
    )


class TestExecutionReporterBindings(pinject.BindingSpec):
    def __init__(
        self, path: Optional[str], url: Optional[str], require_url: bool = False
    ):
        self._url = url
        if not url:
            self._url = read_url_from_config_path(path, require_url)

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
        bind(
            "api_token_provider",
            to_instance=lambda: ApiTokenStorage(
                self._url,
                UserConfigRepository(os.path.expanduser("~/.cato/config.json")),
            ).get_api_token(),
        )


def run(
    path: str,
    suite_name: str,
    test_identifier_str: str,
    only_failed: bool,
    verbose: int,
    url: str,
    variables: Dict[str, str],
) -> None:
    obj_graph = create_object_graph(path, url, require_url=True)
    run_command = provide_safe(obj_graph, RunCommand)

    verbose_mode = VerboseMode.in_range(verbose)

    exit_code = run_command.run(
        path,
        suite_name,
        test_identifier_str,
        bool(only_failed),
        verbose_mode,
        variables,
    )

    exit(exit_code)


def submit(
    path: str,
    suite_name: str,
    test_identifier_str: str,
    only_failed: bool,
    url: str,
    variables: Dict[str, str],
) -> None:
    obj_graph = create_object_graph(path, url, require_url=True)
    submit_command = provide_safe(obj_graph, SubmitCommand)

    submit_command.run(
        path, suite_name, test_identifier_str, bool(only_failed), variables
    )


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


def config_template(path: str) -> None:
    obj_graph = create_object_graph()
    config_template_command = obj_graph.provide(ConfigTemplateCommand)

    config_template_command.create_template(path)


def worker_run(
    url: str,
    submission_info_id: int,
    test_identifier_str: str,
) -> None:
    obj_graph = create_object_graph(url=url, require_url=True)
    worker_command = provide_safe(obj_graph, WorkerRunCommand)

    worker_command.execute(submission_info_id, test_identifier_str)


def sync_test_edits(path: str, url: str, run_id: int) -> None:
    obj_graph = create_object_graph(path, url, require_url=True)
    sync_test_edits_command = provide_safe(obj_graph, SyncTestEditsCommand)

    sync_test_edits_command.sync(path, run_id)


def _add_vars_option(run_parser):
    run_parser.add_argument(
        "--var",
        action=StoreDictKeyPair,
        nargs="+",
        help="Override project variables. Example: key=value",
    )


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
        "run", help="Execute tests from a config file", parents=[parent_parser]
    )
    run_parser.add_argument("--path", help=PATH_TO_CONFIG_FILE)
    run_parser.add_argument("--suite", help="Suite to run")
    run_parser.add_argument(
        "--test-identifier",
        help="Identifier of test to run. Example: suite_name/test_name",
    )
    run_parser.add_argument("-u", "--url", help="url to server")
    run_parser.add_argument("-v", "--verbose", action="count", default=1)
    run_parser.add_argument("--only-failed", action="store_true")
    _add_vars_option(run_parser)

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
    _add_vars_option(submit_parser)

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
        help="Run test in a distributed environment. Not for direct human use",
        parents=[parent_parser],
    )
    worker_execute_command_parser.add_argument(
        "-u", "--url", help="url to server", required=True
    )
    worker_execute_command_parser.add_argument(
        "-submission-info-id", required=True, type=int, help="run id to report to"
    )
    worker_execute_command_parser.add_argument(
        "-test-identifier", required=True, help="Identifier of the test to run"
    )

    sync_test_edits_command_parser = commands_subparser.add_parser(
        "sync-edits",
        help="Sync test edits from UI back locally",
        parents=[parent_parser],
    )
    sync_test_edits_command_parser.add_argument(
        "-u", "--url", help="url to server", required=True
    )
    sync_test_edits_command_parser.add_argument(
        "-run-id", required=True, type=int, help="run id to take edits to sync from"
    )
    sync_test_edits_command_parser.add_argument("--path", help=PATH_TO_CONFIG_FILE)

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
            args.var,
        )
    elif args.command == "submit":
        submit(
            args.path,
            args.suite,
            args.test_identifier,
            args.only_failed,
            args.url,
            args.var,
        )
    elif args.command == "update-missing-reference-images":
        update_missing_reference_images(args.path)
    elif args.command == "list-tests":
        list_tests(args.path)
    elif args.command == "update-reference":
        update_reference(args.path, args.test_identifier)
    elif args.command == "worker-run":
        worker_run(args.url, args.submission_info_id, args.test_identifier)
    elif args.command == "sync-edits":
        sync_test_edits(args.path, args.url, args.run_id)
    else:
        logger.error(f"No method found to run command {args.command}")


if __name__ == "__main__":
    main()
