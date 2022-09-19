import inspect
from collections import defaultdict
from typing import Type, TypeVar, List, Set, cast

JSON_TYPE_INFO_PROPERTY_NAME = "__json_type_info_attribute__"

T = TypeVar("T")


class TypeInfo:
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError(f"A TypeInfo has to be str, was {value.__class__}.")
        value = value.strip()
        if not value:
            raise ValueError("A TypeInfo can not be empty or blank.")
        self._value = value

    def __repr__(self):
        return self._value

    def __str__(self):
        return self._value

    def __eq__(self, other):
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)


class PolymorphicInspectionException(Exception):
    pass


class NoTypeInfoAttributeValue(PolymorphicInspectionException):
    def __init__(self, type: Type, type_info_attribute: str) -> None:
        super(NoTypeInfoAttributeValue, self).__init__(
            f"The class '{type}' has no attribute '{type_info_attribute}'. Check {type}.{JSON_TYPE_INFO_PROPERTY_NAME}"
        )


class NoTypeInfoAttributeName(PolymorphicInspectionException):
    def __init__(self, type: Type) -> None:
        super(NoTypeInfoAttributeName, self).__init__(
            f"The class '{type}' has no attribute '{JSON_TYPE_INFO_PROPERTY_NAME}'."
        )


class DuplicatedTypeInfo(PolymorphicInspectionException):
    def __init__(self, cls_list: List[Type], type_info: TypeInfo) -> None:
        super(DuplicatedTypeInfo, self).__init__(
            f"The classes {' '.join([x.__name__ for x in cls_list])} have the same type info, '{type_info}'"
        )


class PolymorphicInspector:
    def is_polymorphic_mapped_class(self, cls: Type[T]) -> bool:
        return hasattr(cls, JSON_TYPE_INFO_PROPERTY_NAME)

    def get_type_info(self, cls: Type[T]) -> TypeInfo:
        type_info = self._read_type_info_for_cls(cls)
        self._verify_no_duplicated_type_info_in_hierarchy(cls)
        return type_info

    def get_type_info_property(self, cls: Type) -> str:
        return cast(str, getattr(cls, JSON_TYPE_INFO_PROPERTY_NAME))

    def _read_type_info_for_cls(self, cls: Type) -> TypeInfo:
        try:
            type_info_attribute = self.get_type_info_property(cls)
        except AttributeError:
            raise NoTypeInfoAttributeName(cls)
        try:
            type_info_str = getattr(cls, type_info_attribute)
        except AttributeError:
            raise NoTypeInfoAttributeValue(cls, type_info_attribute)
        type_info = TypeInfo(type_info_str)
        return type_info

    def _verify_no_duplicated_type_info_in_hierarchy(self, cls: Type) -> None:
        classes = self._get_classes_in_tree(cls)
        type_infos = defaultdict(list)
        for cl in classes:
            try:
                type_info = self._read_type_info_for_cls(cl)
                type_infos[type_info].append(cl)
            except PolymorphicInspectionException:
                pass

        for type_info, classes_with_type_info in type_infos.items():
            if len(classes_with_type_info) > 1:
                raise DuplicatedTypeInfo(classes_with_type_info, type_info)

    def _get_classes_in_tree(self, cls: Type) -> Set[Type]:
        parents = inspect.getmro(cls)
        childs = self._get_child_classes(cls)
        return {*parents, *childs}

    def _get_child_classes(self, cls: Type) -> Set[Type]:
        classes = set()
        for cl in cls.__subclasses__():
            classes.add(cl)
            classes.update(self._get_child_classes(cl))
        return classes
