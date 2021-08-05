import datetime

from cato_common.mappers.mapper_registry import MapperRegistry
from cato_common.domain.project import Project
from cato_common.mappers.abstract_class_mapper import AbstractClassMapper
from cato_common.mappers.abstract_value_mapper import AbstractValueMapper


class MyTestMapper(AbstractClassMapper):
    pass


class DateTimeValueMapper(AbstractValueMapper[datetime.datetime, str]):
    pass


def test_register_class_mapper_and_get():
    mapper_registry = MapperRegistry()
    mapper = MyTestMapper()

    mapper_registry.register_class_mapper(Project, mapper)
    returned_mapper = mapper_registry.class_mapper_for_cls(Project)

    assert returned_mapper is mapper


def test_no_class_mapper_exists():
    mapper_registry = MapperRegistry()

    assert not mapper_registry.class_mapper_for_cls(Project)


def test_register_value_mapper_and_get():
    mapper_registry = MapperRegistry()
    mapper = DateTimeValueMapper()

    mapper_registry.register_value_mapper(datetime.datetime, mapper)
    returned_mapper = mapper_registry.value_mapper_for_cls(datetime.datetime)

    assert returned_mapper is mapper


def test_no_value_mapper_exists():
    mapper_registry = MapperRegistry()

    assert not mapper_registry.value_mapper_for_cls(datetime.datetime)
