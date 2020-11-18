import argparse
import json
import os

import pinject

from cato.config.config_file_parser import JsonConfigParser
from cato.config.config_template_generator import ConfigTemplateGenerator
from cato.domain.test_suite import iterate_suites_and_tests, count_tests, count_suites
from cato.reporter.end_message_generator import EndMessageGenerator
from cato.reporter.html_reporter import HtmlReporter
from cato.reporter.timing_report_generator import TimingReportGenerator
from cato.runners.test_suite_runner import TestSuiteRunner
from cato.runners.update_missing_reference_images import UpdateMissingReferenceImages


def run(path: str):
    path = config_path(path)

    config_parser = JsonConfigParser()
    config = config_parser.parse(path)

    obj_graph = pinject.new_object_graph()
    test_suite_runner = obj_graph.provide(TestSuiteRunner)

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


def update_missing_reference_images(path):
    path = config_path(path)

    config_parser = JsonConfigParser()
    config = config_parser.parse(path)

    obj_graph = pinject.new_object_graph()
    update_missing = obj_graph.provide(UpdateMissingReferenceImages)

    update_missing.update(config)


def list_tests(path):
    path = config_path(path)

    config_parser = JsonConfigParser()
    config = config_parser.parse(path)

    print(
        f"Found {count_tests(config.test_suites)} tests in {count_suites(config.test_suites)} suites:"
    )
    print()

    for suite, test in iterate_suites_and_tests(config.test_suites):
        print(f"{suite.name}/{test.name}")


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
    run_parser.add_argument("--path", help="Path to config file")

    run_parser = commands_subparser.add_parser(
        "update-missing-reference-images",
        help="Updates missing reference images after a test run",
        parents=[parent_parser],
    )
    run_parser.add_argument("--path", help="Path to config file")

    list_parser = commands_subparser.add_parser(
        "list-tests", help="Lists tests in config file", parents=[parent_parser]
    )
    list_parser.add_argument("--path", help="Path to config file")

    args = main_parser.parse_args()
    if args.command == "config-template":
        config_template(args.path)
    elif args.command == "run":
        run(args.path)
    elif args.command == "update-missing-reference-images":
        update_missing_reference_images(args.path)
    elif args.command == "list-tests":
        list_tests(args.path)
