import datetime
from dataclasses import dataclass
from typing import List, Dict

from cato_server.mappers.abstract_class_mapper import AbstractClassMapper, T
from cato_server.mappers.generic_class_mapper import GenericClassMapper
from cato_server.mappers.internal.datetime_value_mapper import DateTimeValueMapper
from cato_server.mappers.mapper_registry import MapperRegistry


class TestMapToDict:
    def test_map_simple_dataclass(self):
        @dataclass
        class SimpleDataClass:
            my_int: int
            my_string: str

        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            SimpleDataClass(my_int=1, my_string="my_string")
        )

        assert result == {"my_int": 1, "my_string": "my_string"}

    def test_map_dataclass_with_simple_list(self):
        @dataclass
        class SimpleDataClass:
            my_int: int
            my_string_list: List[str]

        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            SimpleDataClass(my_int=1, my_string_list=["my", "string", "list"])
        )

        assert result == {"my_int": 1, "my_string_list": ["my", "string", "list"]}

    def test_map_dataclass_with_list_of_dataclasses(self):
        @dataclass
        class ListedClass:
            my_int: int
            my_string: str

        @dataclass
        class SimpleDataClass:
            my_int: int
            my_list: List[ListedClass]

        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            SimpleDataClass(
                my_int=1,
                my_list=[
                    ListedClass(my_int=1, my_string="my_string1"),
                    ListedClass(my_int=2, my_string="my_string2"),
                    ListedClass(my_int=3, my_string="my_string3"),
                ],
            )
        )

        assert result == {
            "my_int": 1,
            "my_list": [
                {"my_int": 1, "my_string": "my_string1"},
                {"my_int": 2, "my_string": "my_string2"},
                {"my_int": 3, "my_string": "my_string3"},
            ],
        }

    def test_map_dataclass_with_custom_value_mapper_for_datetime(self):
        @dataclass
        class DataClassWithDatetime:
            my_int: int
            my_datetime: datetime.datetime

        registry = MapperRegistry()
        registry.register_value_mapper(datetime.datetime, DateTimeValueMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_to_dict(
            DataClassWithDatetime(
                my_int=1, my_datetime=datetime.datetime(2021, 7, 31, 9, 31)
            )
        )

        assert result == {"my_datetime": "2021-07-31T09:31:00", "my_int": 1}

    def test_map_dataclass_with_custom_class_mapper_for_field(self):
        @dataclass
        class NestedClass:
            my_int: int
            my_string: str

        @dataclass
        class DataClassWithNestedClass:
            my_nested_class: NestedClass

        class CustomMapper(AbstractClassMapper[NestedClass]):
            def map_to_dict(self, test_result: NestedClass) -> Dict:
                return {"my_int": 42, "my_string": test_result.my_string}

        registry = MapperRegistry()
        registry.register_class_mapper(NestedClass, CustomMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_to_dict(
            DataClassWithNestedClass(
                my_nested_class=NestedClass(my_int=1, my_string="my_test")
            )
        )

        assert result == {"my_nested_class": {"my_int": 42, "my_string": "my_test"}}

    def test_map_dataclass_with_custom_mapper_for_dataclass(self):
        @dataclass
        class ClassWithCustomMapper:
            my_int: int
            my_string: str

        class CustomMapper(AbstractClassMapper[ClassWithCustomMapper]):
            def map_to_dict(self, test_result: ClassWithCustomMapper) -> Dict:
                return {"my_int": 42, "my_string": test_result.my_string}

        registry = MapperRegistry()
        registry.register_class_mapper(ClassWithCustomMapper, CustomMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_to_dict(
            ClassWithCustomMapper(my_int=1, my_string="my_test")
        )

        assert result == {"my_int": 42, "my_string": "my_test"}


# dataclass
# dataclass with simple list
# dataclass with list of dataclasses
# dataclass with nested dataclass
# dataclass with nested dataclass and custom mapper for nested
# class with custom mapper
# dataclass with optional simple field
# dataclass with optional nested class
# dataclass with optional nested class with custom mapper
# dataclass with nested class with nested optional field
# dataclass with list of optional values
