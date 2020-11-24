import os
from io import StringIO

from cato.config.config_file_parser import JsonConfigParser
from cato.config.config_file_writer import ConfigFileWriter
from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_suite import TestSuite


def test_write_and_read_back_is_equal():
    test1 = Test("test1", "command", {"key": "value"})
    test2 = Test("test2", "command", {})
    test3 = Test("test3", "command", {})
    suite1 = TestSuite(name="my_suite_1", tests=[test1])
    suite2 = TestSuite(name="my_suite_2", tests=[test2, test3])

    suites = [suite1, suite2]

    config = Config(
        path="test",
        test_suites=suites,
        output_folder=os.getcwd(),
        variables={"my_var": "value"},
    )
    config_file_writer = ConfigFileWriter()
    stream = StringIO()

    config_file_writer.write_to_stream(stream, config)
    str_result = stream.getvalue()

    config_file_parser = JsonConfigParser()
    parsed_result = config_file_parser.parse("test/my_path", StringIO(str_result))

    assert parsed_result == config
