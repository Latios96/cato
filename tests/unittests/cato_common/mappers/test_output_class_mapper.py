from cato_common.domain.output import Output


def test_from_dict_with_id(object_mapper):
    result = object_mapper.from_dict(
        {"id": 1, "test_result_id": 2, "text": "my text"}, Output
    )

    assert result == Output(id=1, test_result_id=2, text="my text")


def test_from_dict_without_id(object_mapper):
    result = object_mapper.from_dict({"test_result_id": 2, "text": "my text"}, Output)

    assert result == Output(id=0, test_result_id=2, text="my text")


def test_to_dict(object_mapper):
    result = object_mapper.to_dict(Output(id=1, test_result_id=2, text="my text"))

    assert result == {"id": 1, "test_result_id": 2, "text": "my text"}
