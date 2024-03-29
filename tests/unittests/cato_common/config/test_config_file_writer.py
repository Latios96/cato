from io import StringIO

from cato_common.config.config_file_parser import JsonConfigParser
from cato_common.config.config_file_writer import ConfigFileWriter
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.config import Config
from cato_common.domain.test import Test
from cato_common.domain.test_suite import TestSuite

test1 = Test("test1", "command", {"key": "value"}, ComparisonSettings.default())
test2 = Test("test2", "command", {}, ComparisonSettings.default())
test3 = Test("test3", "command", {}, ComparisonSettings.default())
suite1 = TestSuite(name="my_suite_1", tests=[test1])
suite2 = TestSuite(name="my_suite_2", tests=[test2, test3])

suites = [suite1, suite2]

CONFIG = Config(
    project_name="Example project",
    suites=suites,
    variables={"my_var": "value"},
)


def test_write_and_read_back_is_equal(object_mapper):
    config_file_writer = ConfigFileWriter(object_mapper)
    stream = StringIO()

    config_file_writer.write_to_stream(stream, CONFIG)
    str_result = stream.getvalue()

    config_file_parser = JsonConfigParser()
    parsed_result = config_file_parser.parse("test/my_path", StringIO(str_result))

    assert parsed_result == CONFIG


def test_write_to_dict_and_read_back_is_equal(object_mapper):
    config_file_writer = ConfigFileWriter(object_mapper)

    config_dict = config_file_writer.write_to_dict(CONFIG)

    config_file_parser = JsonConfigParser()
    parsed_result = config_file_parser.parse_dict(config_dict)

    assert parsed_result == CONFIG
