import pinject

from cato.config.config_file_parser import JsonConfigParser
from cato.runners.test_suite_runner import TestSuiteRunner

if __name__ == "__main__":
    config_parser = JsonConfigParser()
    config = config_parser.parse('test', open(r'M:\workspace\cato\testconfig.json'))

    obj_graph = pinject.new_object_graph()
    test_suite_runner = obj_graph.provide(TestSuiteRunner)

    test_suite_runner.run_test_suites(config)
