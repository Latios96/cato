from cato_server.domain.output import Output
from cato_server.mappers.output_class_mapper import OutputClassMapper


def test_from_dict_with_id():
    mapper = OutputClassMapper()

    result = mapper.map_from_dict({"id": 1, "test_result_id": 2, "text": "my text"})

    assert result == Output(id=1, test_result_id=2, text="my text")


def test_from_dict_without_id():
    mapper = OutputClassMapper()

    result = mapper.map_from_dict({"test_result_id": 2, "text": "my text"})

    assert result == Output(id=0, test_result_id=2, text="my text")


def test_to_dict():
    mapper = OutputClassMapper()

    result = mapper.map_to_dict(Output(id=1, test_result_id=2, text="my text"))

    assert result == {"id": 1, "test_result_id": 2, "text": "my text"}
