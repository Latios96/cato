import datetime
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional

import pytest

from cato_common.mappers.abstract_class_mapper import AbstractClassMapper, T
from cato_common.mappers.abstract_value_mapper import AbstractValueMapper
from cato_common.mappers.generic_class_mapper import GenericClassMapper
from cato_common.mappers.mapper_registry import MapperRegistry


class DateTimeValueMapper(AbstractValueMapper[datetime.datetime, str]):
    def map_from(self, data: Optional[str]) -> Optional[datetime.datetime]:
        if data:
            return datetime.datetime(2021, 8, 5)

    def map_to(self, date: datetime.datetime) -> str:
        return "my datetime string"


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
class DataClassWithUnderscoreMembers:
    my_int_: int


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


class MyEnum(Enum):
    VALUE = "VALUE"


@dataclass
class DataClassWithEnum:
    enum_value: MyEnum


@dataclass
class PolymorphicDataClassBase:
    my_int: int
    my_string: str
    __json_type_info_attribute__ = "type_info"
    type_info = "BASE"


@dataclass
class PolymorphicDataClassChild(PolymorphicDataClassBase):
    my_child_int: int
    my_child_string: str
    type_info = "CHILD"


class TestMapToDict:
    def test_map_simple_dataclass(self):

        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            SimpleDataClass(my_int=1, my_string="my_string")
        )

        assert result == {"myInt": 1, "myString": "my_string"}

    def test_map_dataclass_with_simple_list(self):

        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            SimpleDataClassWithStringList(
                my_int=1, my_string_list=["my", "string", "list"]
            )
        )

        assert result == {"myInt": 1, "myStringList": ["my", "string", "list"]}

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
            "myInt": 1,
            "myList": [
                {"myInt": 1, "myString": "my_string1"},
                {"myInt": 2, "myString": "my_string2"},
                {"myInt": 3, "myString": "my_string3"},
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

        assert result == {"myDatetime": "my datetime string", "myInt": 1}

    def test_map_dataclass_with_custom_class_mapper_for_field(self):
        class CustomMapper(AbstractClassMapper[NestedClass]):
            def map_to_dict(self, test_result: NestedClass) -> Dict:
                return {"myInt": 42, "myString": test_result.my_string}

        registry = MapperRegistry()
        registry.register_class_mapper(NestedClass, CustomMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_to_dict(
            DataClassWithNestedClass(
                my_nested_class=NestedClass(my_int=1, my_string="my_test")
            )
        )

        assert result == {"myNestedClass": {"myInt": 42, "myString": "my_test"}}

    def test_map_dataclass_with_custom_mapper_for_dataclass(self):
        class CustomMapper(AbstractClassMapper[SimpleDataClass]):
            def map_to_dict(self, test_result: SimpleDataClass) -> Dict:
                return {"myInt": 42, "myString": test_result.my_string}

        registry = MapperRegistry()
        registry.register_class_mapper(SimpleDataClass, CustomMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_to_dict(SimpleDataClass(my_int=1, my_string="my_test"))

        assert result == {"myInt": 42, "myString": "my_test"}

    def test_map_enum(self):
        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            DataClassWithEnum(enum_value=MyEnum.VALUE)
        )

        assert result == {"enumValue": "VALUE"}

    def test_map_datetime(self):
        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            DataClassWithDatetime(
                my_int=1, my_datetime=datetime.datetime(2021, 8, 5, 9, 53)
            )
        )

        assert result == {"myInt": 1, "myDatetime": "2021-08-05T09:53:00"}

    def test_map_class_with_fields_ending_with_underscore(self):
        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            DataClassWithUnderscoreMembers(my_int_=1)
        )

        assert result == {"myInt_": 1}

    def test_map_polymorphic_dataclass_parent(self):
        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            PolymorphicDataClassBase(my_string="test", my_int=42)
        )

        assert result == {"myString": "test", "myInt": 42, "typeInfo": "BASE"}

    def test_map_polymorphic_dataclass_child(self):
        result = GenericClassMapper(MapperRegistry()).map_to_dict(
            PolymorphicDataClassChild(
                my_string="test", my_int=42, my_child_string="test", my_child_int=42
            )
        )

        assert result == {
            "myString": "test",
            "myInt": 42,
            "myChildString": "test",
            "myChildInt": 42,
            "typeInfo": "CHILD",
        }


class TestMapFromDict:
    def test_simple_class(self):

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"myInt": 1, "myString": "my_string"}, SimpleDataClass
        )

        assert result == SimpleDataClass(my_int=1, my_string="my_string")

    def test_simple_class_with_simple_list(self):

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"myInt": 1, "myStringList": ["my", "test", "list"]},
            SimpleDataClassWithStringList,
        )

        assert result == SimpleDataClassWithStringList(
            my_int=1, my_string_list=["my", "test", "list"]
        )

    def test_simple_class_with_dataclass_list(self):

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {
                "myInt": 1,
                "myList": [
                    {"myInt": 1, "myString": "my1"},
                    {"myInt": 2, "myString": "my2"},
                    {"myInt": 3, "myString": "my3"},
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
                "myNestedClass": {"myInt": 1, "myString": "test"},
            },
            DataClassWithNestedClass,
        )
        assert result == DataClassWithNestedClass(
            my_nested_class=NestedClass(my_int=1, my_string="test")
        )

    def test_map_dataclass_with_custom_class_mapper_for_field(self):
        class CustomMapper(AbstractClassMapper[NestedClass]):
            def map_from_dict(self, json_data: Dict) -> T:
                return NestedClass(my_int=42, my_string=json_data["myString"])

        registry = MapperRegistry()
        registry.register_class_mapper(NestedClass, CustomMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_from_dict(
            {"myNestedClass": {"myInt": 1, "myString": "my_test"}},
            DataClassWithNestedClass,
        )

        assert result == DataClassWithNestedClass(
            my_nested_class=NestedClass(my_int=42, my_string="my_test")
        )

    def test_map_dataclass_with_custom_mapper(self):
        class CustomMapper(AbstractClassMapper[SimpleDataClass]):
            def map_from_dict(self, json_data: Dict) -> T:
                return SimpleDataClass(my_int=42, my_string=json_data["myString"])

        registry = MapperRegistry()
        registry.register_class_mapper(SimpleDataClass, CustomMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_from_dict(
            {"myInt": 1, "myString": "my_test"}, SimpleDataClass
        )

        assert result == SimpleDataClass(my_int=42, my_string="my_test")

    def test_map_dataclass_with_custom_mapper_for_value(self):

        registry = MapperRegistry()
        registry.register_value_mapper(datetime.datetime, DateTimeValueMapper())
        mapper = GenericClassMapper(registry)

        result = mapper.map_from_dict(
            {"myDatetime": "2021-07-31T09:31:00", "myInt": 1}, DataClassWithDatetime
        )

        assert result == DataClassWithDatetime(
            my_int=1, my_datetime=datetime.datetime(2021, 8, 5, 0, 0)
        )

    @pytest.mark.parametrize("json_value,parsed_value", [(None, None), (0, 0), (1, 1)])
    def test_map_simple_class_with_optional_int_field(self, json_value, parsed_value):
        @dataclass
        class SimpleDataClassWithOptionalField:
            my_optional: Optional[int]

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"myOptional": json_value}, SimpleDataClassWithOptionalField
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
            {"myOptional": json_value}, SimpleDataClassWithOptionalField
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
            {"myString": "test"},
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
                "myInt": 1,
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

        result = mapper.map_from_dict({"myInt": 1}, DataClassWithDatetime)

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
            {"myInt": 1, "myNestedClass": {"myInt": 2}}, ClassWithCustomMapper
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
            {"myList": [1, 0, 2, 3, None]}, ClassWithListOfOptionals
        )

        assert result == ClassWithListOfOptionals(my_list=[1, 0, 2, 3, None])

    def test_map_with_list_of_optional_nested_class(self):
        @dataclass
        class ClassWithListOfOptionals:
            my_list: List[Optional[NestedClass]]

        mapper = GenericClassMapper(MapperRegistry())

        result = mapper.map_from_dict(
            {
                "myList": [
                    {"myInt": 1, "myString": "2"},
                    None,
                    {"myInt": 2, "myString": "3"},
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

    def test_map_enum(self):
        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"enumValue": "VALUE"}, DataClassWithEnum
        )

        assert result == DataClassWithEnum(enum_value=MyEnum.VALUE)

    def test_default_non_optional_int_to_0(self):
        @dataclass
        class DataClassWithOptionalInt:
            my_optional_int: int

        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {}, DataClassWithOptionalInt
        )

        assert result == DataClassWithOptionalInt(my_optional_int=0)

    def test_map_datetime(self):
        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"myInt": 1, "myDatetime": "2021-08-05T09:53:00"}, DataClassWithDatetime
        )

        assert result == DataClassWithDatetime(
            my_int=1, my_datetime=datetime.datetime(2021, 8, 5, 9, 53)
        )

    def test_map_class_with_fields_ending_with_underscore(self):
        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"myInt_": 1}, DataClassWithUnderscoreMembers
        )

        assert result == DataClassWithUnderscoreMembers(my_int_=1)

    def test_map_polymorphic_dataclass_parent(self):
        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {"myString": "test", "myInt": 42, "typeInfo": "BASE"},
            PolymorphicDataClassBase,
        )

        assert result == PolymorphicDataClassBase(my_string="test", my_int=42)

    def test_map_polymorphic_dataclass_child(self):
        result = GenericClassMapper(MapperRegistry()).map_from_dict(
            {
                "myString": "test",
                "myInt": 42,
                "myChildString": "test",
                "myChildInt": 42,
                "typeInfo": "CHILD",
            },
            PolymorphicDataClassBase,
        )

        assert result == PolymorphicDataClassChild(
            my_string="test", my_int=42, my_child_string="test", my_child_int=42
        )
