import argparse
import json
import os

import pinject

from cato.config.config_file_parser import JsonConfigParser
from cato.config.config_template_generator import ConfigTemplateGenerator
from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_suite import (
    iterate_suites_and_tests,
    count_tests,
    count_suites,
    filter_by_suite_name,
    filter_by_test_identifier,
)
from cato.reporter.end_message_generator import EndMessageGenerator
from cato.reporter.html_reporter import HtmlReporter
from cato.reporter.test_execution_db_reporter import TestExecutionDbReporter
from cato.reporter.timing_report_generator import TimingReportGenerator
from cato.runners.test_suite_runner import TestSuiteRunner
from cato.runners.update_missing_reference_images import UpdateMissingReferenceImages
from cato.runners.update_reference_images import UpdateReferenceImages
from cato.storage.sqlalchemy.sqlalchemy_config import SqlAlchemyConfig
from cato.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
)
from cato.storage.sqlalchemy.sqlalchemy_run_repository import SqlAlchemyRunRepository
from cato.storage.sqlalchemy.sqlalchemy_simple_file_storage import SqlAlchemySimpleFileStorage
from cato.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)

PATH_TO_CONFIG_FILE = "Path to config file"

config = SqlAlchemyConfig()


class TestExecutionReporterBindings(pinject.BindingSpec):
    def configure(self, bind):
        bind("test_execution_reporter", to_class=TestExecutionDbReporter)
        bind("project_repository", to_class=SqlAlchemyProjectRepository)
        bind("run_repository", to_class=SqlAlchemyRunRepository)
        bind("suite_result_repository", to_class=SqlAlchemySuiteResultRepository)
        bind("test_result_repository", to_class=SqlAlchemyTestResultRepository)
        bind("file_storage", to_class=SqlAlchemySimpleFileStorage)
        bind("root_path", to_instance=r"M:/test/cato-file-storage")
        bind("session_maker", to_instance=config.get_session_maker())


def run(path: str, suite_name: str, test_identifier_str: str, dump_report_json: bool):
    path = config_path(path)

    config_parser = JsonConfigParser()
    config = config_parser.parse(path)

    obj_graph = pinject.new_object_graph(
        binding_specs=[TestExecutionReporterBindings()]
    )
    test_suite_runner = obj_graph.provide(TestSuiteRunner)

    if suite_name:
        config.test_suites = filter_by_suite_name(config.test_suites, suite_name)
    if test_identifier_str:
        config.test_suites = filter_by_test_identifier(
            config.test_suites, TestIdentifier.from_string(test_identifier_str)
        )

    result = test_suite_runner.run_test_suites(config)

    timing_report_generator = TimingReportGenerator()
    print()
    print(timing_report_generator.generate(result))

    generator = obj_graph.provide(EndMessageGenerator)
    print()
    print(generator.generate_end_message(result))

    report_data = {"result": [x.to_dict() for x in result]}

    reporter = HtmlReporter()
    reporter.report(report_data, os.path.join(config.output_folder, "report"))

    if dump_report_json:
        with open("report.json", "w") as f:
            json.dump(report_data, f)


def update_missing_reference_images(path):
    path = config_path(path)

    config_parser = JsonConfigParser()
    config = config_parser.parse(path)

    obj_graph = pinject.new_object_graph()
    update_missing = obj_graph.provide(UpdateMissingReferenceImages)

    update_missing.update(config)


def list_tests(path):
    path = config_path(path)
    print(path)
    config_parser = JsonConfigParser()
    config = config_parser.parse(path)

    print(
        f"Found {count_tests(config.test_suites)} tests in {count_suites(config.test_suites)} suites:"
    )
    print()

    for suite, test in iterate_suites_and_tests(config.test_suites):
        print(f"{suite.name}/{test.name}")


def update_reference(path, test_identifier):
    path = config_path(path)

    config_parser = JsonConfigParser()
    config = config_parser.parse(path)

    obj_graph = pinject.new_object_graph()
    update_reference = obj_graph.provide(UpdateReferenceImages)

    update_reference.update(config, TestIdentifier.from_string(test_identifier))


def config_template(path: str):
    path = config_path(path)

    with open(path, "w") as f:
        ConfigTemplateGenerator().write(f)


def config_path(path):
    if not path:
        path = os.getcwd()
    path = os.path.abspath(path)
    if os.path.isdir(path):
        path = os.path.join(path, "cato.json")
    return path


if __name__ == "__main__":
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
    run_parser.add_argument(
        "--dump-report-json",
        action="store_true",
        help="Dump report data as json (usefull for debugging report generation)",
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
        run(args.path, args.suite, args.test_identifier, args.dump_report_json)
    elif args.command == "update-missing-reference-images":
        update_missing_reference_images(args.path)
    elif args.command == "list-tests":
        list_tests(args.path)
    elif args.command == "update-reference":
        print(args)
        update_reference(args.path, args.test_identifier)
    else:
        print(f"No method found to run command {args.command}")
