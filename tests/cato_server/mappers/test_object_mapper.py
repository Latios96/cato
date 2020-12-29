import pytest

from cato_server.domain.project import Project
from cato_server.mappers.mapper_registry import MapperRegistry
from cato_server.mappers.mapper_registry_factory import MapperRegistryFactory
from cato_server.mappers.object_mapper import ObjectMapper, NoMapperFoundException
from cato_api_models.catoapimodels import MachineInfoDto


@pytest.fixture
def object_mapper():
    registry = MapperRegistryFactory().create_mapper_registry()
    return ObjectMapper(registry)


class TestMapToDict:
    def test_no_mapper_found_for_cls_should_raise(self):
        mapper_registry = MapperRegistry()
        object_mapper = ObjectMapper(mapper_registry)

        with pytest.raises(NoMapperFoundException):
            object_mapper.to_dict(Project(id=1, name="test"))

    def test_should_map_conjure_type_to_dict(self, object_mapper):
        object = MachineInfoDto(cpu_name="test", cores=8, memory=4)

        result = object_mapper.to_dict(object)

        assert result == {"cores": 8, "cpu_name": "test", "memory": 4}

    def test_should_map_with_dedicated_mapper_to_dict(self, object_mapper):
        object = Project(id=1, name="test")

        result = object_mapper.to_dict(object)

        assert result == {"id": 1, "name": "test"}


class TestMapFromDict:
    def test_no_mapper_found_for_cls_should_raise(self):
        mapper_registry = MapperRegistry()
        object_mapper = ObjectMapper(mapper_registry)

        with pytest.raises(NoMapperFoundException):
            object_mapper.from_dict({"id": 1, "name": "test"}, Project)

    def test_should_map_conjure_type_to_dict(self, object_mapper):
        the_dict = {"cores": 8, "cpu_name": "test", "memory": 4}

        result = object_mapper.from_dict(the_dict, MachineInfoDto)

        assert result == MachineInfoDto(cpu_name="test", cores=8, memory=4)

    def test_should_map_with_dedicated_mapper_to_dict(self, object_mapper):
        the_dict = {"id": 1, "name": "test"}

        result = object_mapper.from_dict(the_dict, Project)

        assert result == Project(id=1, name="test")

    def test_missing_key(self, object_mapper):
        the_dict = {"id": 1}

        with pytest.raises(KeyError):
            object_mapper.from_dict(the_dict, Project)


class TestMapToJson:
    def test_success(self, object_mapper):
        object = Project(id=1, name="test")

        result = object_mapper.to_json(object)

        assert result == '{"id": 1, "name": "test"}'


class TestMapFromJson:
    def test_success(self, object_mapper):
        json_str = '{"id": 1, "name": "test"}'

        result = object_mapper.from_json(json_str, Project)

        assert result == Project(id=1, name="test")


class TestManyVariants:
    def test_many_to_dict(self, object_mapper):
        objects = [Project(id=1, name="test1"), Project(id=2, name="test2")]

        dicts = object_mapper.many_to_dict(objects)

        assert dicts == [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]

    def test_many_to_json(self, object_mapper):
        objects = [Project(id=1, name="test1"), Project(id=2, name="test2")]

        dicts = object_mapper.many_to_json(objects)

        assert dicts == '[{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]'

    def test_many_from_dict(self, object_mapper):
        the_dicts = [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]

        objects = object_mapper.many_from_dict(the_dicts, Project)

        assert objects == [Project(id=1, name="test1"), Project(id=2, name="test2")]

    def test_many_from_json(self, object_mapper):
        json_str = '[{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]'

        objects = object_mapper.many_from_json(json_str, Project)

        assert objects == [Project(id=1, name="test1"), Project(id=2, name="test2")]
