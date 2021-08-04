import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

import pytest

from cato_server.mappers.abstract_class_mapper import AbstractClassMapper, T
from cato_server.mappers.generic_class_mapper import GenericClassMapper
from cato_server.mappers.internal.datetime_value_mapper import DateTimeValueMapper
from cato_server.mappers.mapper_registry import MapperRegistry
from cato_api_models.catoapimodels import (
    ApiSuccess,
)


@dataclass
class SimpleDataClass:
    my_int: int
    my_string: str


@dataclass
class SimpleDataClassWithStringList:
    my_int: int
    my_string_list: List[str]


@dataclass
class ListedClass:
    my_int: int
    my_string: str


@dataclass
class SimpleDataClassWithListedClassList:
    my_int: int
    my_list: List[ListedClass]


@dataclass
class DataClassWithDatetime:
    my_int: int
    my_datetime: datetime.datetime


@dataclass
class NestedClass:
    my_int: int
    my_string: str


@dataclass
class DataClassWithNestedClass:
    my_nested_class: NestedClass


@dataclass
class DataClassWithNestedOptionalClass:
    my_nested_class: Optional[NestedClass]


@dataclass
class DataClassWithOptionalNestedClass:
    my_string: str
    my_nested_class: Optional[NestedClass]


class TestMapToDict:
    def test_map_simple_dataclass(self):

        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            SimpleDataClass(my_int=1, my_string="my_string")
        )

        assert result == {"my_int": 1, "my_string": "my_string"}

    def test_map_dataclass_with_simple_list(self):

        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            SimpleDataClassWithStringList(
                my_int=1, my_string_list=["my", "string", "list"]
            )
        )

        assert result == {"my_int": 1, "my_string_list": ["my", "string", "list"]}

    def test_map_dataclass_with_list_of_dataclasses(self):

        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            SimpleDataClassWithListedClassList(
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
        class CustomMapper(AbstractClassMapper[SimpleDataClass]):
            def map_to_dict(self, test_result: SimpleDataClass) -> Dict:
                return {"my_int": 42, "my_string": test_result.my_string}

        registry = MapperRegistry()
        registry.register_class_mapper(SimpleDataClass, CustomMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_to_dict(SimpleDataClass(my_int=1, my_string="my_test"))

        assert result == {"my_int": 42, "my_string": "my_test"}

    def test_map_conjure_type(self):
        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            ApiSuccess(success=True)
        )

        assert result == {"success": True}


class TestMapFromDict:
    def test_simple_class(self):

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"my_int": 1, "my_string": "my_string"}, SimpleDataClass
        )

        assert result == SimpleDataClass(my_int=1, my_string="my_string")

    def test_simple_class_with_simple_list(self):

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"my_int": 1, "my_string_list": ["my", "test", "list"]},
            SimpleDataClassWithStringList,
        )

        assert result == SimpleDataClassWithStringList(
            my_int=1, my_string_list=["my", "test", "list"]
        )

    def test_simple_class_with_dataclass_list(self):

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {
                "my_int": 1,
                "my_list": [
                    {"my_int": 1, "my_string": "my1"},
                    {"my_int": 2, "my_string": "my2"},
                    {"my_int": 3, "my_string": "my3"},
                ],
            },
            SimpleDataClassWithListedClassList,
        )

        assert result == SimpleDataClassWithListedClassList(
            my_int=1,
            my_list=[
                ListedClass(my_int=1, my_string="my1"),
                ListedClass(my_int=2, my_string="my2"),
                ListedClass(my_int=3, my_string="my3"),
            ],
        )

    def test_simple_dataclass_with_nested_dataclass(self):

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {
                "my_nested_class": {"my_int": 1, "my_string": "test"},
            },
            DataClassWithNestedClass,
        )
        assert result == DataClassWithNestedClass(
            my_nested_class=NestedClass(my_int=1, my_string="test")
        )

    def test_map_dataclass_with_custom_class_mapper_for_field(self):
        class CustomMapper(AbstractClassMapper[NestedClass]):
            def map_from_dict(self, json_data: Dict) -> T:
                return NestedClass(my_int=42, my_string=json_data["my_string"])

        registry = MapperRegistry()
        registry.register_class_mapper(NestedClass, CustomMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_from_dict(
            {"my_nested_class": {"my_int": 1, "my_string": "my_test"}},
            DataClassWithNestedClass,
        )

        assert result == DataClassWithNestedClass(
            my_nested_class=NestedClass(my_int=42, my_string="my_test")
        )

    def test_map_dataclass_with_custom_mapper(self):
        class CustomMapper(AbstractClassMapper[SimpleDataClass]):
            def map_from_dict(self, json_data: Dict) -> T:
                return SimpleDataClass(my_int=42, my_string=json_data["my_string"])

        registry = MapperRegistry()
        registry.register_class_mapper(SimpleDataClass, CustomMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_from_dict(
            {"my_int": 1, "my_string": "my_test"}, SimpleDataClass
        )

        assert result == SimpleDataClass(my_int=42, my_string="my_test")

    def test_map_dataclass_with_custom_mapper_for_value(self):

        registry = MapperRegistry()
        registry.register_value_mapper(datetime.datetime, DateTimeValueMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_from_dict(
            {"my_datetime": "2021-07-31T09:31:00", "my_int": 1}, DataClassWithDatetime
        )

        assert result == DataClassWithDatetime(
            my_int=1, my_datetime=datetime.datetime(2021, 7, 31, 9, 31)
        )

    @pytest.mark.parametrize("json_value,parsed_value", [(None, None), (0, 0), (1, 1)])
    def test_map_simple_class_with_optional_int_field(self, json_value, parsed_value):
        @dataclass
        class SimpleDataClassWithOptionalField:
            my_optional: Optional[int]

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"my_optional": json_value}, SimpleDataClassWithOptionalField
        )

        assert result == SimpleDataClassWithOptionalField(parsed_value)

    @pytest.mark.parametrize(
        "json_value,parsed_value", [(None, None), ("", ""), ("1", "1")]
    )
    def test_map_simple_class_with_optional_str_field(self, json_value, parsed_value):
        @dataclass
        class SimpleDataClassWithOptionalField:
            my_optional: Optional[str]

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"my_optional": json_value}, SimpleDataClassWithOptionalField
        )

        assert result == SimpleDataClassWithOptionalField(parsed_value)

    def test_map_dataclass_nested_optional_class(self):

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {},
            DataClassWithNestedOptionalClass,
        )
        assert result == DataClassWithNestedOptionalClass(my_nested_class=None)

    def test_map_dataclass_nested_optional_class_and_other_value(self):

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"my_string": "test"},
            DataClassWithOptionalNestedClass,
        )
        assert result == DataClassWithOptionalNestedClass(
            my_nested_class=None, my_string="test"
        )

    def test_map_dataclass_nested_optional_class_with_custom_mapper(self):
        @dataclass
        class ClassWithCustomMapper:
            my_int: int
            my_nested_class: Optional[NestedClass]

        class CustomMapper(AbstractClassMapper[ClassWithCustomMapper]):
            def map_from_dict(self, json_data: Dict) -> T:
                return ClassWithCustomMapper(my_int=42, my_nested_class=None)

        registry = MapperRegistry()
        registry.register_class_mapper(ClassWithCustomMapper, CustomMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_from_dict(
            {
                "my_int": 1,
            },
            ClassWithCustomMapper,
        )

        assert result == ClassWithCustomMapper(my_int=42, my_nested_class=None)

    def test_map_dataclass_with_custom_class_mapper_for_optional_field(self):
        @dataclass
        class DataClassWithDatetime:
            my_int: int
            my_datetime: Optional[datetime.datetime]

        registry = MapperRegistry()
        registry.register_value_mapper(datetime.datetime, DateTimeValueMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_from_dict({"my_int": 1}, DataClassWithDatetime)

        assert result == DataClassWithDatetime(my_int=1, my_datetime=None)

    def test_map_dataclass_nested_class_with_optional_field(self):
        @dataclass
        class NestedClass:
            my_int: int
            my_string: Optional[str]

        @dataclass
        class ClassWithCustomMapper:
            my_int: int
            my_nested_class: NestedClass

        mapper = GenericClassMapper(MapperRegistry())

        result = mapper.map_from_dict(
            {"my_int": 1, "my_nested_class": {"my_int": 2}}, ClassWithCustomMapper
        )

        assert result == ClassWithCustomMapper(
            my_int=1, my_nested_class=NestedClass(my_int=2, my_string=None)
        )

    def test_map_with_list_of_optional_values(self):
        @dataclass
        class ClassWithListOfOptionals:
            my_list: List[Optional[int]]

        mapper = GenericClassMapper(MapperRegistry())

        result = mapper.map_from_dict(
            {"my_list": [1, 0, 2, 3, None]}, ClassWithListOfOptionals
        )

        assert result == ClassWithListOfOptionals(my_list=[1, 0, 2, 3, None])

    def test_map_with_list_of_optional_nested_class(self):
        @dataclass
        class ClassWithListOfOptionals:
            my_list: List[Optional[NestedClass]]

        mapper = GenericClassMapper(MapperRegistry())

        result = mapper.map_from_dict(
            {
                "my_list": [
                    {"my_int": 1, "my_string": "2"},
                    None,
                    {"my_int": 2, "my_string": "3"},
                ]
            },
            ClassWithListOfOptionals,
        )

        assert result == ClassWithListOfOptionals(
            my_list=[
                NestedClass(my_int=1, my_string="2"),
                None,
                NestedClass(my_int=2, my_string="3"),
            ]
        )

    def test_map_non_optional_from_none(self):

        with pytest.raises(KeyError):
            GenericClassMapper(MapperRegistry()).map_from_dict(None, SimpleDataClass)

    def test_simple_dataclass_with_nested_dataclass_not_present(self):

        with pytest.raises(KeyError):
            GenericClassMapper(MapperRegistry()).map_from_dict(
                {},
                DataClassWithNestedClass,
            )

    def test_map_conjure_type(self):
        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"success": True}, ApiSuccess
        )

        assert result == ApiSuccess(success=True)
