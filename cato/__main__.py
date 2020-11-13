import pinject

from cato.config.config_file_parser import JsonConfigParser
from cato.reporter.end_message_generator import EndMessageGenerator
from cato.runners.test_suite_runner import TestSuiteRunner

if __name__ == "__main__":
    config_parser = JsonConfigParser()
    #path = r"M:\test\cato-test\testconfig.json"
    path = r"M:\workspace\cato\testconfig.json"
    config = config_parser.parse(path)

    obj_graph = pinject.new_object_graph()
    test_suite_runner = obj_graph.provide(TestSuiteRunner)

    result = test_suite_runner.run_test_suites(config)

    generator = EndMessageGenerator()
    print()
    print(generator.generate_end_message(result))

