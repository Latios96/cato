import argparse
import os

import pinject

from cato.config.config_file_parser import JsonConfigParser
from cato.config.config_template_generator import ConfigTemplateGenerator
from cato.reporter.end_message_generator import EndMessageGenerator
from cato.runners.test_suite_runner import TestSuiteRunner


def run(path: str):
    path = config_path(path)

    config_parser = JsonConfigParser()
    config = config_parser.parse(path)

    obj_graph = pinject.new_object_graph()
    test_suite_runner = obj_graph.provide(TestSuiteRunner)

    result = test_suite_runner.run_test_suites(config)

    generator = EndMessageGenerator()
    print()
    print(generator.generate_end_message(result))


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

    args = main_parser.parse_args()
    if args.command == "config-template":
        config_template(args.path)
    elif args.command == "run":
        run(args.path)
