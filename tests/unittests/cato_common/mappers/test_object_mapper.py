import pytest

from cato_common.domain.project import Project, ProjectStatus
from cato_common.storage.page import Page


class TestMapToDict:
    def test_should_map_with_dedicated_mapper_to_dict(self, object_mapper):
        object = Project(id=1, name="test", status=ProjectStatus.ACTIVE)

        result = object_mapper.to_dict(object)

        assert result == {
            "id": 1,
            "name": "test",
            "status": "ACTIVE",
            "thumbnailFileId": None,
        }

    def test_called_with_dict_should_work(self, object_mapper):
        the_dict = {"key": "value"}

        the_dict = object_mapper.to_dict(the_dict)

        assert the_dict == {"key": "value"}


class TestMapFromDict:
    def test_should_map_with_dedicated_mapper_to_dict(self, object_mapper):
        the_dict = {"id": 1, "name": "test", "status": "ACTIVE"}

        result = object_mapper.from_dict(the_dict, Project)

        assert result == Project(id=1, name="test", status=ProjectStatus.ACTIVE)

    def test_missing_key(self, object_mapper):
        the_dict = {"id": 1}

        with pytest.raises(KeyError):
            object_mapper.from_dict(the_dict, Project)


class TestMapToJson:
    def test_success(self, object_mapper):
        object = Project(id=1, name="test", status=ProjectStatus.ACTIVE)

        result = object_mapper.to_json(object)

        assert (
            result
            == '{"id": 1, "name": "test", "status": "ACTIVE", "thumbnailFileId": null}'
        )


class TestMapFromJson:
    def test_success(self, object_mapper):
        json_str = '{"id": 1, "name": "test", "status": "ACTIVE"}'

        result = object_mapper.from_json(json_str, Project)

        assert result == Project(id=1, name="test", status=ProjectStatus.ACTIVE)


class TestManyVariants:
    def test_many_to_dict(self, object_mapper):
        objects = [
            Project(id=1, name="test1", status=ProjectStatus.ACTIVE),
            Project(id=2, name="test2", status=ProjectStatus.ACTIVE),
        ]

        dicts = object_mapper.many_to_dict(objects)

        assert dicts == [
            {"id": 1, "name": "test1", "status": "ACTIVE", "thumbnailFileId": None},
            {"id": 2, "name": "test2", "status": "ACTIVE", "thumbnailFileId": None},
        ]

    def test_many_to_json(self, object_mapper):
        objects = [
            Project(id=1, name="test1", status=ProjectStatus.ACTIVE),
            Project(id=2, name="test2", status=ProjectStatus.ACTIVE),
        ]

        dicts = object_mapper.many_to_json(objects)

        assert (
            dicts
            == '[{"id": 1, "name": "test1", "status": "ACTIVE", "thumbnailFileId": null}, {"id": 2, "name": "test2", "status": "ACTIVE", "thumbnailFileId": null}]'
        )

    def test_many_from_dict(self, object_mapper):
        the_dicts = [
            {"id": 1, "name": "test1", "status": "ACTIVE"},
            {"id": 2, "name": "test2", "status": "ACTIVE"},
        ]

        objects = object_mapper.many_from_dict(the_dicts, Project)

        assert objects == [
            Project(id=1, name="test1", status=ProjectStatus.ACTIVE),
            Project(id=2, name="test2", status=ProjectStatus.ACTIVE),
        ]

    def test_many_from_json(self, object_mapper):
        json_str = '[{"id": 1, "name": "test1", "status": "ACTIVE"}, {"id": 2, "name": "test2", "status": "ACTIVE"}]'

        objects = object_mapper.many_from_json(json_str, Project)

        assert objects == [
            Project(id=1, name="test1", status=ProjectStatus.ACTIVE),
            Project(id=2, name="test2", status=ProjectStatus.ACTIVE),
        ]


def test_no_page_instances(object_mapper):
    with pytest.raises(RuntimeError):
        object_mapper.to_dict(
            Page(
                page_number=1,
                page_size=10,
                total_entity_count=1,
                entities=[Project(id=0, name="test", status=ProjectStatus.ACTIVE)],
            )
        )
