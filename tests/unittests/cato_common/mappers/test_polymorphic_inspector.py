# get type info for base class, both attr authored
# get type info for child class, both attr authored
# get type info for child class, property attr authored in parent class
import pytest

from cato_common.mappers.polymorphic_inspector import (
    PolymorphicInspector,
    TypeInfo,
    NoTypeInfoAttributeValue,
    NoTypeInfoAttributeName,
    DuplicatedTypeInfo,
)


class TestTypeInfo:
    @pytest.mark.parametrize("invalid_string", ["", "  "])
    def test_create_from_invalid_string(self, invalid_string):
        with pytest.raises(ValueError):
            TypeInfo(invalid_string)

    def test_create_valid_type_info_name(self):
        TypeInfo("type_info")

    def test_to_str(self):
        type_info = TypeInfo("type_info")

        assert str(type_info) == "type_info"

    def test_type_info_with_same_str_should_be_equal(self):
        a = TypeInfo("type_info")
        b = TypeInfo("type_info")

        assert a == b

    def test_type_info_with_different_str_should_not_be_equal(self):
        a = TypeInfo("type_info")
        b = TypeInfo("type_info_")

        assert a != b

    def test_should_hash_correctly(self):
        assert {
            TypeInfo("type_info"),
            TypeInfo("type_info"),
            TypeInfo("type_info_"),
        } == {
            TypeInfo("type_info"),
            TypeInfo("type_info_"),
        }


class TestIsPolymorphicMappedClass:
    def test_should_return_true_for_base_class(self):
        class Base:
            __json_type_info_attribute__ = "type"

        inspector = PolymorphicInspector()
        assert inspector.is_polymorphic_mapped_class(Base)

    def test_should_return_true_for_child_class(self):
        class Base:
            __json_type_info_attribute__ = "type"

        class Child(Base):
            pass

        inspector = PolymorphicInspector()
        assert inspector.is_polymorphic_mapped_class(Child)

    def test_should_return_false_for_base_class(self):
        class Base:
            pass

        inspector = PolymorphicInspector()
        assert not inspector.is_polymorphic_mapped_class(Base)

    def test_should_return_false_for_child_class(self):
        class Base:
            pass

        class Child(Base):
            pass

        inspector = PolymorphicInspector()
        assert not inspector.is_polymorphic_mapped_class(Child)


class TestGetTypeInfo:
    def test_should_get_type_info_for_base_class(self):
        class Base:
            __json_type_info_attribute__ = "type"
            type = "BASE"

        inspector = PolymorphicInspector()
        assert inspector.get_type_info(Base) == TypeInfo("BASE")

    def test_should_get_type_info_for_child_class(self):
        class Base:
            __json_type_info_attribute__ = "type"
            type = "BASE"

        class Child(Base):
            type = "CHILD"

        inspector = PolymorphicInspector()
        assert inspector.get_type_info(Child) == TypeInfo("CHILD")

    def test_should_not_get_type_info_missing_info_attribute_name(self):
        class Base:
            pass

        inspector = PolymorphicInspector()
        with pytest.raises(NoTypeInfoAttributeName):
            inspector.get_type_info(Base)

    def test_should_not_get_type_info_missing_info_attribute(self):
        class Base:
            __json_type_info_attribute__ = "type"

        inspector = PolymorphicInspector()
        with pytest.raises(NoTypeInfoAttributeValue):
            inspector.get_type_info(Base)

    def test_should_not_get_type_info_for_base_duplicated_type_info(self):
        class Base:
            __json_type_info_attribute__ = "type"
            type = "BASE"

        class Child(Base):
            type = "BASE"

        inspector = PolymorphicInspector()
        with pytest.raises(DuplicatedTypeInfo):
            inspector.get_type_info(Base)

    def test_should_not_get_type_info_for_child_duplicated_type_info(self):
        class Base:
            __json_type_info_attribute__ = "type"
            type = "BASE"

        class Child(Base):
            type = "BASE"

        inspector = PolymorphicInspector()
        with pytest.raises(DuplicatedTypeInfo):
            inspector.get_type_info(Base)

    def test_should_not_get_type_info_for_middle_duplicated_type_info(self):
        class Base:
            __json_type_info_attribute__ = "type"
            type = "BASE"

        class Middle(Base):
            type = "BASE"

        class Child(Middle):
            type = "BASE"

        inspector = PolymorphicInspector()
        with pytest.raises(DuplicatedTypeInfo):
            inspector.get_type_info(Middle)
